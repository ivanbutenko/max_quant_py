import re
import shlex
from itertools import groupby, zip_longest
from os.path import basename
from typing import Iterable, Dict, List, Any


def _parse_job(batch_name: str, row: str, job_name: str)->Dict[str, Any]:
    num, batch, command, arguments, wd = row
    arguments = [a.strip('"') for a in shlex.split(arguments)]

    if job_name is None:
        job_name = re.sub(r'\W', '_', arguments[4])

    return {
        'command': command,
        'args': arguments,
        'name': '{}-{}'.format(batch_name, job_name)
    }


def _parse_batch(name: str, rows: List[str], filepaths: List[str])->Dict[str, Any]:
    batch_name = name.split('.')[-1]
    if len(rows) == len(filepaths):
        names = [
            basename(f)
            for f in filepaths
                ]
    else:
        names = tuple()

    jobs = [
        _parse_job(batch_name, row, name)
        for row, name in zip_longest(rows, names)
    ]
    return {
        'name': batch_name,
        'jobs': jobs,
    }


def parse_batches(rows: Iterable[str], filepaths: List[str])->List[Dict]:
    rows = [
        r.split('\t')
        for r in rows
    ]
    batches = [
        _parse_batch(batch, group, filepaths)
        for batch, group in groupby(rows, lambda r: r[1])
    ]
    return batches
