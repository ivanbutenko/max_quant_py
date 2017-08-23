import argparse
import sys

import yaml

from maxquant.batch import parse_batches
from maxquant.config import read_config
from maxquant.maxquant import run_maxquant


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mqpar', '-c', required=True)
    p.add_argument('--custom-params', '-p')

    args = p.parse_args()

    if args.custom_params:
        custom_params = args.custom_params.split(' ')
    else:
        custom_params = []

    config = read_config()

    res = run_maxquant(
        max_quant_cmd=config['maxquant_cmd.bin'],
        options=['-c', args.mqpar, '-D'] + custom_params
    )

    batches = parse_batches(res)
    yaml.dump(batches, sys.stdout, default_flow_style=None)


if __name__ == '__main__':
    main()
