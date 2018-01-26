from xml.etree import ElementTree
from typing import *


def set_list(tree: ElementTree.ElementTree, path: str, values: List[Any], type_name='string'):
    node = tree.find(path)
    for e in node.findall(type_name):
        node.remove(e)

    for value in values:
        e = ElementTree.Element(type_name)
        e.text = str(value)
        node.append(e)


def set_text(tree: ElementTree.ElementTree, path: str, value: str):
    node = tree.find(path)
    if node is None:
        raise ValueError('path not found: {}'.format(path))

    node.text = value


def apply(tree: ElementTree.ElementTree, actions: List[Tuple]):
    for func, *args in actions:
        func(tree, *args)
