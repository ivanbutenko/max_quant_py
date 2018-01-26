from os.path import basename
from typing import List, Any, Dict, Tuple
from xml.etree import ElementTree

from maxquant.xml_mod import apply, set_list


def write_mqpar_config(tpl_file: str, out_file: str, actions: List[Tuple]):
    tree = ElementTree.parse(tpl_file)
    apply(tree, actions)
    tree.write(out_file)


def get_file_actions(files: List[str])->List[Tuple]:
    def crop_name(name):
        return basename(name).replace('.wiff', '')
    return [
        (set_list, 'filePaths', files, 'string'),
        (set_list, 'experiments', map(crop_name, files), 'string'),
        (set_list, 'fractions', [32767]*len(files), 'short'),
        (set_list, 'paramGroupIndices', [0]*len(files), 'int'),
    ]


def read_mqpar_config(filename: str)->Dict[str, Any]:
    tree = ElementTree.parse(filename)
    root = tree.getroot()

    filepaths = [
        e.text
        for e in root.find('filePaths').findall('string')
    ]

    threads = int(root.find('numThreads').text)
    database = root.find('fastaFiles').find('string').text

    return {
        'filepaths': filepaths,
        'threads': threads,
        'database': database,
    }
