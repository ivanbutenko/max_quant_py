import argparse
from os.path import abspath

from maxquant.mqpar import write_mqpar_config


def main():
    parser = argparse.ArgumentParser(
        prog='mqpar',
    )
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-m', '--max-quant-template', required=True)
    parser.add_argument('-d', '--database', required=True)
    parser.add_argument('-t', '--threads', default=1, type=int)
    parser.add_argument('files', nargs='+', help='*.wiff files')

    args = parser.parse_args()

    args.files = [
        abspath(f)
        for f in args.files
    ]

    write_mqpar_config(
        tpl_file=args.max_quant_template,
        out_file=args.output,
        files=args.files,
        database=args.database,
        threads=args.threads,
    )


if __name__ == '__main__':
    main()


