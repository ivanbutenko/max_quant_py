import argparse
from os.path import abspath, exists

import sys
import ujson as json
from maxquant.batch import parse_batches
from maxquant.maxquant import run_maxquant
from maxquant.mqpar import write_mqpar_config


def validate(args):
    def print_and_exit(message):
        print(message)
        exit(1)

    if not exists(args.database):
        print_and_exit('Database fasta file {}  does not exist'.format(args.database))

    if not exists(args.max_quant_template):
        print_and_exit('mqpar template file {} does not exist'.format(args.max_quant_template))

    if not exists(args.max_quant_cmd):
        print_and_exit('MaxQuant command binary {} does not exist'.format(args.max_quant_cmd))


def main():
    parser = argparse.ArgumentParser(
        prog='maxquant',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('-c', '--mqpar-generated', default='mqpar.gen.xml', help='Generated mqpar path')
    parser.add_argument('-T', '--mqpar-template', default='mqpar.base.xml', help='Template mqpar')
    parser.add_argument('-d', '--database', default='database.fasta', help='Database')
    parser.add_argument('-t', '--threads', default=1, type=int, help='Num of threads, do not use on cluster')
    parser.add_argument('-C', '--max-quant-cmd', default='MaxQuant/bin/CommandLine.exe', help='MaxQuant Commandline.exe binary')
    parser.add_argument('-p', '--custom-params')
    parser.add_argument('files', nargs='+', help='*.wiff files')

    args = parser.parse_args()

    args.files = [
        abspath(f)
        for f in args.files
    ]

    args.mqpar_generated = abspath(args.mqpar_generated)

    write_mqpar_config(
        tpl_file=args.mqpar_template,
        out_file=args.mqpar_generated,
        files=args.files,
        database=args.database,
        threads=args.threads,
    )

    if args.custom_params:
        custom_params = args.custom_params.split(' ')
    else:
        custom_params = []

    # config = read_config()

    res = run_maxquant(
        max_quant_cmd=args.max_quant_cmd,
        options=['-c', args.mqpar_generated, '-D'] + custom_params
    )

    batches = parse_batches(res)
    json.dump(batches, sys.stdout, indent=2)


if __name__ == '__main__':
    main()


