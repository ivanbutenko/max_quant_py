import argparse
import sys
from os.path import basename, abspath, dirname, join
from xml.etree import ElementTree


def write_config(tpl_file, out_file, files, threads, fasta_file):
    def add_strings(node_path, values, node_type='string'):
        node = tree.find(node_path)
        for e in node.findall(node_type):
            node.remove(e)

        for value in values:
            e = ElementTree.Element(node_type)
            e.text = str(value)
            node.append(e)

    tree = ElementTree.parse(tpl_file)
    tree.find('numThreads').text = str(threads)

    add_strings('filePaths', files)

    add_strings('experiments', [
        basename(f)
        for f in files
    ])

    add_strings('fractions', [32767]*len(files), node_type='short')

    add_strings('paramGroupIndices', [0]*len(files), node_type='int')

    add_strings('fastaFiles', [fasta_file], node_type='string')

    tree.write(out_file)


def main():
    script_dir = dirname(abspath(__file__))

    p = argparse.ArgumentParser()
    p.add_argument('--config-tpl', '-c',
                   help='mqpar.xml', default=join(script_dir, 'mqpar.base.xml'))
    p.add_argument('--threads', '-t', default=1, type=int)
    p.add_argument('--fasta-file', '-f',
                   default=join(script_dir, 'contaminants.fasta'))
    p.add_argument('--config-out', '-o', help='"-" - means stdout', default=sys.stdout.buffer)
    p.add_argument('files', nargs='+', help='*.wiff files')

    args = p.parse_args()

    args.files = [
        abspath(f)
        for f in args.files
    ]

    args.fasta_file = abspath(args.fasta_file)

    if args.config_out == '-':
        args.config_out = sys.stdout

    write_config(
        tpl_file=args.config_tpl,
        out_file=args.config_out,
        files=args.files,
        threads=args.threads,
        fasta_file=args.fasta_file,
    )


if __name__ == '__main__':
    main()
