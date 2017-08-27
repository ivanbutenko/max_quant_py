from os.path import basename
from typing import List, Any, Dict
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


def read_mqpar_config(filename: str)->Dict[str, Any]:
    tree = ElementTree.parse(filename)
    filepaths_elems = tree.getroot().find('filePaths').findall('string')
    filepaths = [
        e.text
        for e in filepaths_elems
    ]
    return {
        'filepaths': filepaths,
    }
