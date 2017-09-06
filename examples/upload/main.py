#!/usr/bin/env python3
from argparse import ArgumentParser
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from pw.uploader import Upload
from pw.utils import BIN_SIZES
from pw.types import DATATYPES


def get_parser():
    parser = ArgumentParser(description='upload a file to Parallel Works')
    parser.add_argument('-f', '--file', help='path to file to upload', type=str, required=True)
    parser.add_argument('-w', '--workspace', help='workspace id for uploaded file', type=str, required=True)
    parser.add_argument('-k', '--key', help='API key to authenticate with', type=str, required=True)
    parser.add_argument('-d', '--datatype', help='datatype of the file', type=str, default=DATATYPES['binary'])
    parser.add_argument('-e', '--endpoint', help='endpoint to upload to', type=str, required=True)
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
    datatype = args['datatype']
    max_read_size = args['size']
    max_retries = args['retry']
    retry_timeout = args['timeout']
    endpoint = args['endpoint']

    upload = Upload(filename, workspace_id, key, datatype, max_read_size, max_retries, retry_timeout)
    res = upload.submit(endpoint)
    print('Decoded Job ID: %d' % res['decoded_job_id'])


if __name__ == '__main__':
    main()
