import argparse
from os.path import abspath, exists
from typing import List, Tuple
import re

from maxquant import version
from maxquant.cli.misc import print_and_exit
from maxquant.mqpar import write_mqpar_config, get_file_actions
from maxquant.xml_mod import set_text


def validate(args):
    if args.database and not exists(args.database):
        print_and_exit('FASTA database does not exist: {}'.format(args.database))

    if not exists(args.mqpar_template):
        print_and_exit('mqpar template file does not exist: {}'.format(args.mqpar_template))

    for file_path in args.files:
        if not exists(file_path):
            print_and_exit('Raw file does not exist: {}'.format(file_path))
        if not file_path.endswith('.wiff'):
            print_and_exit('Raw file is not a wiff file {}'.format(file_path))


def parse_set_text(set_text_args: List[str])->List[Tuple]:
    split_pattern = re.compile(r'([^:]+):([^:]+)')
    return [
        (set_text, *split_pattern.match(arg).groups())
        for arg in set_text_args
    ]


def main():
    parser = argparse.ArgumentParser(
        prog='maxquant-mqpar',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('-T', '--mqpar-template', default='mqpar.base.xml', help='Template mqpar')
    parser.add_argument('-d', '--database', help=argparse.SUPPRESS)
    parser.add_argument('-t', '--threads', type=int, help=argparse.SUPPRESS)
    parser.add_argument('-o', '--output', help='Output mqpar file', default='mqpar.gen.xml')
    # parser.add_argument('-l', '--set-list', nargs='+', help='')
    parser.add_argument('-s', '--set-text', action='append', help='xpath:value')
    parser.add_argument('--version', '-V', action='version', version="%(prog)s " + version.get_version())

    parser.add_argument('files', nargs='+', help='*.wiff files')

    args = parser.parse_args()

    args.files = [
        abspath(f)
        for f in args.files
    ]

    args.output = abspath(args.output)

    validate(args)

    actions = [
        *parse_set_text(args.set_text or []),
        *get_file_actions(args.files)
    ]
    if args.database:
        args.database = abspath(args.database)
        actions.append((set_text, 'fastaFiles/string', args.database))

    if args.threads:
        actions.append((set_text, 'numThreads', str(args.threads)))

    write_mqpar_config(
        tpl_file=args.mqpar_template,
        out_file=args.output,
        actions=actions,
    )


if __name__ == '__main__':
    main()


