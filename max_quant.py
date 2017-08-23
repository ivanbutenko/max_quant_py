#!/usr/bin/env python

from __future__ import absolute_import, print_function

import argparse
import subprocess
import sys
from os.path import abspath, join, dirname

import yaml


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line.strip()
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def run_max_quant(max_quant_cmd, options):
    # type: (str, list) -> list[str]
    args = ['mono', max_quant_cmd] + options
    return execute(args)


def echo_stdout(outs):
    for line in outs:
        print(line)


def main():
    script_dir = dirname(abspath(__file__))

    p = argparse.ArgumentParser()
    p.add_argument('--config', '-c', required=True)
    p.add_argument('--dump-batch', '-D')
    p.add_argument('--custom-params', '-p')
    p.add_argument('--threads', '-t', default=1, type=int)
    p.add_argument('--max-quant-cmd', '-m', default=join(script_dir, 'bin', 'CommandLine.exe'))

    args = p.parse_args()

    args.max_quant_cmd = abspath(args.max_quant_cmd)

    if args.custom_params:
        custom_params = args.custom_params.split(' ')
    else:
        custom_params = []

    if not args.dump_batch:
        echo_stdout(run_max_quant(args.max_quant_cmd, ['-c', args.config] + custom_params))
    else:
        rows = run_max_quant(args.max_quant_cmd,  ['-c', args.config, '-D'] + custom_params)
        data = parse_config(rows)

        if args.dump_batch != '-':
            f = open(args.dump_batch, 'w')
        else:
            f = sys.stdout
        yaml.dump(data, f)
        f.close()

if __name__ == '__main__':
    main()
