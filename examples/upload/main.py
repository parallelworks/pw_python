#!/usr/bin/env python3
from pw.uploader import Upload

MB = 1024 * 1024


def main():
    filename = 'files/1mb.txt'
    workspace_id = '<WORKSPACE ID>'  # Note: takes ID not workspace name
    key = '<API KEY>'
    max_read_size = 8 * MB
    max_retries = 15
    retry_timeout = 5
    endpoint = 'https://go.parallel.works/api/upload'

    upload = Upload(filename, workspace_id, key, max_read_size, max_retries, retry_timeout)
    res = upload.submit(endpoint)
    print('Decoded Job ID: %d' % res['decoded_job_id'])


if __name__ == '__main__':
    main()
