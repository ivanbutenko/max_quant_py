import argparse
import sys
from itertools import groupby
import shlex
import yaml


def _parse_job(row):
    num, batch, command, arguments, wd = row
    arguments = [a.strip('"') for a in shlex.split(arguments)]

    return {
        'command': command,
        'args': arguments,
    }


def _parse_batch(name, rows):
    jobs = [
        _parse_job(row)
        for row in rows
    ]
    return {
        'name': name.split('.')[-1],
        'jobs': jobs,
    }


def parse_config(rows):
    rows = [
        r.split('\t')
        for r in rows
    ]
    batches = [
        _parse_batch(batch, group)
        for batch, group in groupby(rows, lambda r: r[1])
    ]
    return batches


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-o', '--out-batch')

    args = p.parse_args()

    lines = iter(sys.stdin)
    batches = parse_config(lines)

    if args.out_batch:
        f = open(args.out_batch, 'w')
    else:
        f = sys.stdout

    yaml.dump(batches, f)
    f.close()


if __name__ == '__main__':
    main()