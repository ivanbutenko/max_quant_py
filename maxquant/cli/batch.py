import argparse
import sys

import ujson as json

from maxquant.batch import parse_batches
# from maxquant.config import read_config
from maxquant.maxquant import run_maxquant


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mqpar', '-c', required=True)
    p.add_argument('--maxquant-cmd', '-m', required=True)
    p.add_argument('--custom-params', '-p')

    args = p.parse_args()

    if args.custom_params:
        custom_params = args.custom_params.split(' ')
    else:
        custom_params = []

    # config = read_config()

    res = run_maxquant(
        max_quant_cmd=args.maxquant_cmd,
        options=['-c', args.mqpar, '-D'] + custom_params
    )

    batches = parse_batches(res)
    json.dump(batches, sys.stdout, indent=2)


if __name__ == '__main__':
    main()
