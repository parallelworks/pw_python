"""
    Uploader.py

    Uploads a file to Parallel Works using a chunked and resumable method.
    http://www.grid.net.ru/nginx/resumable_uploads.en.html

    Python 3.x

"""
import json
import os
import time

import requests

ACK_STATUS = 201
EOF_STATUS = 200
FORBIDDEN_STATUS = 403


class Data(object):
    """Data is a method-less object representing a chunk of file data"""
    def __init__(self, content, start):
        self.content = content
        self.size = len(content)
        self.start = start
        self.end = start + self.size - 1


class File(object):
    """File is an object implementing a Reader interface"""
    def __init__(self, filename, max_read_size):
        self.name = filename
        self.loaded = 0
        self.size = os.path.getsize(self.name)
        self.pointer = open(self.name, 'rb')
        self.max_read_size = max_read_size

    def has_unloaded_data(self):
        return self.loaded < self.size - 1

    def get_progress(self):
        return self.loaded / self.size

    def read(self):
        window = self.size - self.loaded
        if window > self.max_read_size:
            window = self.max_read_size

        self.pointer.seek(self.loaded)
        content = self.pointer.read(window)
        return Data(content, self.loaded)

    def load(self, loaded):
        if not isinstance(loaded, int):
            loaded = int(loaded)
        self.loaded = loaded


class Upload(object):
    """Upload is an object that handles uploading a file to a remote nginx server"""
    def __init__(self, filename, workspace_id, key, datatype, max_read_size, max_retries, retry_timeout):
        self.file = File(filename, max_read_size)
        self.workspace_id = workspace_id
        self.key = key
        self.datatype = datatype
        self.max_retries = max_retries
        self.retry_timeout = retry_timeout
        self.retry_count = 0
        self.read_times = []
        self.res = None

    def _measure_read(self, data, start_time):
        end_time = time.time()
        pt = (data.start, data.end, data.end - data.start + 1, start_time, end_time, end_time - start_time)
        self.read_times.append(pt)

    def _generate_session_id(self):
        basename = os.path.basename(self.file.name).replace('.', '')
        parts = [basename, str(int(time.time()))]
        return '_'.join(parts)

    def _parse_range_header(self, res):
        header = res.headers.get('range')
        if header is None:
            err = 'Parsing Response: {}'.format(res.content)
            raise Exception(err)

        # Replace following with a Regex
        parts = header.split('/')
        if len(parts) != 2:
            err = 'Parsing Response: {}'.format(res.content)
            raise Exception(err)
        loaded = parts[0].split('-')
        if len(loaded) != 2:
            err = 'Parsing Response: {}'.format(res.content)
            raise Exception(err)

        return int(loaded[1])

    def _handle_nginx_res(self, res, data):
        if res.status_code == ACK_STATUS:
            loaded = self._parse_range_header(res)
            print('Server acknowledged: bytes {}-{}/{}'.format(
                data.start, loaded, self.file.size))
            self.file.load(loaded+1)
            return True

        elif res.status_code == EOF_STATUS:
            print('Server acknowledged: EOF')
            self.file.load(data.end)
            self.res = json.loads(res.content.decode('utf-8'))
            return True

        elif res.status_code == FORBIDDEN_STATUS:
            err = 'Error: API is invalid for this workspace'
            raise Exception(err)

        else:
            print('Error: no ack for bytes {}-{}/{} (code {})'.format(
                data.start, data.end, self.file.size, res.status_code))

            if self.retry_count < self.max_retries:
                self.retry_count += 1
                time.sleep(self.retry_timeout)
                return False
            else:
                err = 'Submit Failed: exceeded retry count'
                raise Exception(err)

    def submit(self, url):
        session_id = self._generate_session_id()
        print('Session ID: ' + session_id)

        while self.file.has_unloaded_data():
            start_time = time.time()
            data = self.file.read()

            basename = os.path.basename(self.file.name)
            disposition = 'attachment; filename="{}"'.format(basename)
            content_range = 'bytes {}-{}/{}'.format(
                data.start, data.end, self.file.size
            )
            headers = {
                'Connection': 'keep-alive',
                'Content-Length': str(data.size),
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': disposition,
                'Content-Range': content_range,
                'Session-ID': session_id
            }
            params = {
                'workspaceId': self.workspace_id,
                'key': self.key,
                'datatype': self.datatype
            }

            res = requests.post(url, data=data.content, params=params, headers=headers)
            ok = self._handle_nginx_res(res, data)

            if ok:
                self._measure_read(data, start_time)

        self.file.pointer.close()
        if self.res:
            return self.res
        else:
            return None
