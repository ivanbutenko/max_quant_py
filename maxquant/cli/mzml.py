import argparse

from maxquant.mzml_filter import process_file


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    fix_parser = subparsers.add_parser('filter')
    fix_parser.add_argument('-m', '--threshold-multiplier', default=3, type=int)
    # fix_parser.add_argument('--precision', '-p', choices=(64, 32), type=int, default=64)
    fix_parser.add_argument('in_file')
    fix_parser.add_argument('out_file')

    # validate_parser = subparsers.add_parser('validate')
    # validate_parser.add_argument('in_file')

    args = parser.parse_args()
    if args.command == 'filter':
        process_file(args.in_file, args.out_file, args.threshold_multiplier)


if __name__ == '__main__':
    main()
