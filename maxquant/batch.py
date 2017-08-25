import re
import shlex
from itertools import groupby
from os.path import basename
from typing import Iterable, Dict, List, Any


def _parse_job(batch_name: str, row: str)->Dict[str, Any]:
    num, batch, command, arguments, wd = row
    arguments = [a.strip('"') for a in shlex.split(arguments)]

    job_name = re.sub(r'\W', '_', arguments[4])
    wiff_file = next(
        (arg for arg in arguments if arg.endswith('.wiff')), None
    )
    if wiff_file is not None:
        job_name = basename(wiff_file)
    return {
        'command': command,
        'args': arguments,
        'name': '{}-{}'.format(batch_name, job_name)
    }


def _parse_batch(name: str, rows: List[str])->Dict[str, Any]:
    batch_name = name.split('.')[-1]
    jobs = [
        _parse_job(batch_name, row)
        for row in rows
    ]
    return {
        'name': batch_name,
        'jobs': jobs,
    }


def parse_batches(rows: Iterable[str])->List[Dict]:
    rows = [
        r.split('\t')
        for r in rows
    ]
    batches = [
        _parse_batch(batch, group)
        for batch, group in groupby(rows, lambda r: r[1])
    ]
    return batches
