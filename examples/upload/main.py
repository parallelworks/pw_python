#!/usr/bin/env python3
from argparse import ArgumentParser

from pw.uploader import Upload
from pw.utils import BIN_SIZES


def get_parser():
    parser = ArgumentParser(description='upload a file to Parallel Works')
    parser.add_argument('-f', '--file', help='path to file to upload', type=str)
    parser.add_argument('-w', '--workspace', help='workspace id for uploaded file', type=str)
    parser.add_argument('-k', '--key', help='API key to authenticate with', type=str)
    parser.add_argument('-e', '--endpoint', help='endpoint to upload to', type=str)
    parser.add_argument('-s', '--size', help='max read size of file', type=int, default=8*BIN_SIZES['M'])
    parser.add_argument('-r', '--retry', help='max retries to send all failing chunks', type=int, default=15)
    parser.add_argument('-t', '--timeout', help='time between retry attempts', type=int, default=5)

    return parser


def main():
    p = get_parser()
    args = vars(p.parse_args())

    filename = args['file']
    workspace_id = args['workspace']
    key = args['key']
    max_read_size = args['size']
    max_retries = args['retry']
    retry_timeout = args['timeout']
    endpoint = args['endpoint']

    upload = Upload(filename, workspace_id, key, max_read_size, max_retries, retry_timeout)
    res = upload.submit(endpoint)
    print('Decoded Job ID: %d' % res['decoded_job_id'])


if __name__ == '__main__':
    main()
