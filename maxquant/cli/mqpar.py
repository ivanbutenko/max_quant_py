import argparse
import os
from os.path import join, exists, abspath

from maxquant.config import read_config
from maxquant.mqpar import write_mqpar_config


def main():
    config = read_config()

    # home = os.getenv('HOME')
    parser = argparse.ArgumentParser(
        prog='mqpar',
    )
    parser.add_argument('-o', '--output', required=True)
    # parser.add_argument('-m', '--max-quant-template', default=join(home, '.max_quant', 'mqpar.base.xml'))
    # parser.add_argument('-d', '--database', default=join(home, '.max_quant', 'database.fasta'))
    parser.add_argument('-t', '--threads', default=1, type=int)
    parser.add_argument('files', nargs='+', help='*.wiff files')

    args = parser.parse_args()

    args.files = [
        abspath(f)
        for f in args.files
    ]

    write_mqpar_config(
        tpl_file=config['mqpar.template'],
        out_file=args.output,
        files=args.files,
        database=config['database.fasta'],
        threads=args.threads,
    )


if __name__ == '__main__':
    main()


