#!/usr/bin/env python3
from argparse import ArgumentParser
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from pw.uploader import Upload
from pw.utils import BIN_SIZES

def get_parser():
    parser = ArgumentParser(description='run upload benchmarks')
    parser.add_argument('-w', '--workspace', help='workspace id for uploaded file', type=str)
    parser.add_argument('-k', '--key', help='API key to authenticate with', type=str)
    parser.add_argument('-e', '--endpoint', help='endpoint to upload to', type=str)
    parser.add_argument('-r', '--retry', help='max retries to send all failing chunks', type=int, default=15)
    parser.add_argument('-t', '--timeout', help='time between retry attempts', type=int, default=5)

    return parser


def main():
    p = get_parser()
    args = vars(p.parse_args())

    # Read sizes to benchmark

    mb = BIN_SIZES['M']
    read_sizes = [8 * mb, 16 * mb, 64 * mb, 128 * mb]

    # Files to benchmark

    filedir = 'files/'
    filenames = ['1K.bin', '1M.bin', '100M.bin', '2G.bin', '4G.bin', '10G.bin']
    files = [filedir + name for name in filenames]

    # Args

    wid = args['workspace']
    key = args['key']
    max_retries = args['retry']
    retry_timeout = args['timeout']
    endpoint = args['endpoint']

    # Write results for plotting

    results_file = 'results.csv'

    with open(results_file, 'a+') as fp:
        fp.write('filename, filesize, window, total_transmit_time, throughput\n')
        fp.flush()

        for file in files:
            for window in read_sizes:
                upload = Upload(file, wid, key, window, max_retries, retry_timeout)
                res = upload.submit(endpoint)
                print(res)

                total_time = sum([pt[5] for pt in upload.read_times])
                file_size = os.path.getsize(file)
                fp.write('{}, {}, {}, {}, {}\n'.format(file, file_size, window, total_time, file_size / total_time))
                fp.flush()


if __name__ == '__main__':
    main()
