#!/usr/bin/env python3
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pw.utils import BIN_SIZES


mb = BIN_SIZES['M']
windows = [8 * mb, 16 * mb, 64 * mb, 128 * mb]
runs = 2

filedir = 'files/'
filenames = ['2G.txt', '4G.txt', '10G.txt']
files = [filedir + name for name in filenames]
colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3']


def make_plot(data):
    n_groups = len(windows)
    group_times = []

    for pt in data:
        pts = pt[1]
        times = [float(row[3].replace(' ', '')) / 60 for row in pts]
        if len(times) >= len(windows * runs) and len(times) % 2 == 0:
            m = len(times) / 2
            head, rest = times[0:m], times[m:]
            avgs = [(h + r) / 2 for h, r in zip(head, rest)]
            group_times.append(avgs)

    fig, ax = plt.subplots(figsize=(7.5, 6))
    index = np.arange(n_groups)
    bar_width = 0.10
    opacity = 1

    def autolabel(rects):
        for r in rects:
            height = r.get_height()
            ax.text(r.get_x() + r.get_width() / 2., 1.01 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    for file, color, group, n in zip(files, colors, group_times, range(len(files))):
        pos = [p + bar_width * n for p in index]
        rect = plt.bar(pos, group, bar_width,
                       alpha=opacity,
                       color=color,
                       label=file)

        autolabel(rect)

    plt.xlabel('Window Size (MiB)')
    plt.ylabel('Upload Time (min)')
    plt.title('Upload Time by Window Size')
    plt.xticks(index + bar_width, ('8', '16', '64', '128'))
    plt.legend()

    plt.tight_layout()
    plt.savefig('results/times.png')


def main():
    data = []
    data_file = 'results.csv'

    with open(data_file, 'r') as fp:
        lines = fp.readlines()[1:]
        lines = [line.split(',') for line in lines]

        for file in files:
            pts = [line for line in lines if line[0] == file]
            data.append((file, pts))

    make_plot(data)


if __name__ == '__main__':
    main()
