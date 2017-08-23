from os.path import basename
from typing import List
from xml.etree import ElementTree


def write_mqpar_config(tpl_file: str, out_file: str, files: List[str], threads: int, database: str):
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

    add_strings('fastaFiles', [database], node_type='string')

    tree.write(out_file)
