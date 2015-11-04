#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import subprocess
import re
import csv
import operator
import argparse
import collections

def clean_log(log_filename):
    """
    Clean existing logs.
    """
    if os.path.isfile(log_filename):
        os.remove(log_filename)

def run_vim(exe, log_filename):
    """
    Run vim/nvim to generate startup logs.
    """
    print("Running %s to generate startup logs..." % exe, end="")
    clean_log(log_filename)
    cmd = [exe, "--startuptime", log_filename, "-c", "q"]
    subprocess.call(cmd, shell=False)
    print(" done.")

def guess_plugin_dir(log_txt):
    """
    Try to guess the vim directory containing plugins.
    """
    candidates = list()
    user_dir = os.path.expanduser("~")

    # Get common plugin dir if any
    matches = re.findall("^\d+.\d+\s+\d+.\d+\s+\d+.\d+: sourcing (.+?)/[^/]+/plugin/[^/]+", log_txt, re.MULTILINE)
    for plugin_dir in matches:
        # Ignore system plugins
        if user_dir in plugin_dir:
            candidates.append(plugin_dir)

    return collections.Counter(candidates).most_common(1)[0][0]

def load_data(exe, log_filename):
    """
    Load log and extract relevant data.
    """
    data = {}

    # Load log file and process it
    with open(log_filename, 'r') as log:
        print("Loading and processing logs...", end="")

        log_txt = log.read()

        # Try to guess the folder based on the logs themselves
        plugin_dir = guess_plugin_dir(log_txt)

        matches = re.findall("^\d+.\d+\s+\d+.\d+\s+(\d+.\d+): sourcing %s/([^/]+)/" % plugin_dir, log_txt, re.MULTILINE)
        for res in matches:
            time = res[0]
            plugin = res[1]
            if plugin in data:
                data[plugin] += float(time)
            else:
                data[plugin] = float(time)
    print(" done.")

    return data

def plot_data(data):
    """
    Plot startup data.
    """
    import matplotlib
    matplotlib.use('Qt5Agg')
    import pylab

    print("Plotting result...", end="")
    pylab.barh(range(len(data)), data.values(), align='center')
    pylab.yticks(range(len(data)), list(k for k in data.keys()))
    pylab.xlabel("Startup time (ms)")
    pylab.ylabel("Plugins")
    pylab.show()
    print(" done.")

def export_result(data, output_filename="result.csv"):
    """
    Write sorted result to file
    """
    print("Writing result to %s..." % output_filename, end="")
    with open(output_filename, 'w') as fp:
        writer = csv.writer(fp, delimiter='\t')
        # Sort by time
        for name, time in sorted(data.items(), key=operator.itemgetter(1), reverse=True):
            writer.writerow(["%.3f" % time, name])
    print(" done.")

def print_summary(data, exe, n):
    """
    Print summary of startup times for plugins.
    """
    title = "Top %i plugins slowing %s's startup" % (n, exe)
    length = len(title)
    print(''.center(length, '='))
    print(title)
    print(''.center(length, '='))

    # Sort by time
    rank = 0
    for name, time in sorted(data.items(), key=operator.itemgetter(1), reverse=True)[:n]:
        rank += 1
        print("%i\t%.3f\t%s" % (rank, time, name))

    print(''.center(length, '='))

def main():
    parser = argparse.ArgumentParser(description='Analyze startup times of vim/neovim plugins.')
    parser.add_argument("-o", dest="csv", type=str,
                        help="Export result to a csv file")
    parser.add_argument("-p", dest="plot", action='store_true',
                        help="Plot result as a bar chart")
    parser.add_argument(dest="exe", nargs='?', const=1, type=str, default="vim",
                        help="vim or neovim executable")
    parser.add_argument("-n", dest="n", type=int, default=10,
                        help="Number of plugins to list in the summary")

    # Parse CLI arguments
    args = parser.parse_args()
    exe = args.exe
    log_filename = "vim.log"
    output_filename = args.csv
    n = args.n

    # Run analysis
    run_vim(exe, log_filename)
    data = load_data(exe, log_filename)
    if n > 0:
        print_summary(data, exe, n)
    if output_filename is not None:
        export_result(data, output_filename)
    if args.plot:
        plot_data(data)

    # Cleanup
    clean_log(log_filename)

if __name__ == "__main__":
    main()
