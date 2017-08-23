import re
import shlex
from itertools import groupby
from typing import Iterable, Dict, List, Any


def _parse_job(batch_name: str, row: str)->Dict[str, Any]:
    num, batch, command, arguments, wd = row
    arguments = [a.strip('"') for a in shlex.split(arguments)]

    job_name = re.sub(r'\W', '_', arguments[4])
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
