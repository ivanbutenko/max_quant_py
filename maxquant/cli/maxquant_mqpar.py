import argparse
from os.path import abspath, exists

from maxquant import version
from maxquant.cli.misc import print_and_exit
from maxquant.mqpar import write_mqpar_config


def validate(args):
    if not exists(args.database):
        print_and_exit('FASTA database does not exist: {}'.format(args.database))

    if not exists(args.mqpar_template):
        print_and_exit('mqpar template file does not exist: {}'.format(args.mqpar_template))

    for file_path in args.files:
        if not exists(file_path):
            print_and_exit('Raw file does not exist: {}'.format(file_path))


def main():
    parser = argparse.ArgumentParser(
        prog='maxquant-mqpar',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('-T', '--mqpar-template', default='mqpar.base.xml', help='Template mqpar')
    parser.add_argument('-d', '--database', default='database.fasta', help='FASTA Database')
    parser.add_argument('-t', '--threads', default=1, type=int, help='Num of threads')
    parser.add_argument('-o', '--output', help='Output mqpar file', default='mqpar.gen.xml')
    parser.add_argument('--version', '-V', action='version', version="%(prog)s " + version.get_version())

    parser.add_argument('files', nargs='+', help='*.wiff files')

    args = parser.parse_args()

    args.files = [
        abspath(f)
        for f in args.files
    ]

    args.output = abspath(args.output)
    args.database = abspath(args.database)

    validate(args)
    write_mqpar_config(
        tpl_file=args.mqpar_template,
        out_file=args.output,
        files=args.files,
        database=args.database,
        threads=args.threads,
    )


if __name__ == '__main__':
    main()


