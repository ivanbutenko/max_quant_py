import re
import shlex
from collections import defaultdict, Counter
from itertools import groupby, zip_longest
from os.path import basename
from typing import Iterable, Dict, List, Any

from traitlets import Set


class MaxQuantParser:
    def __init__(self):
        self.batches_count = defaultdict(int)
        self.batches_with_non_uniq_names = None  # type: Set

    def _parse_job(self, batch_name: str, row: str, job_name: str) -> Dict[str, Any]:
        num, batch, command, arguments, wd = row
        arguments = [a.strip('"') for a in shlex.split(arguments)]

        if job_name is None:
            job_name = re.sub(r'\W', '_', arguments[4])

        job = {
            'command': command,
            'args': arguments,
            'name': '{}-{}'.format(batch_name, job_name)
        }

        return job

    def _parse_batch(self, name: str, rows: List[str], filepaths: List[str]) -> Dict[str, Any]:
        batch_name = name.split('.')[-1]

        if name in self.batches_with_non_uniq_names:
            count = self.batches_count[name]
            batch_name = '{}-{}'.format(batch_name, count + 1)
            self.batches_count[name] += 1

        # TODO: fix this
        if len(rows) == len(filepaths):
            names = [
                basename(f)
                for f in filepaths
            ]
        else:
            names = tuple()

        jobs = [
            self._parse_job(batch_name, row, name)
            for row, name in zip_longest(rows, names)
        ]
        return {
            'name': batch_name,
            'jobs': jobs,
        }

    def parse_batches(self, rows: Iterable[str], filepaths: List[str]) -> List[Dict]:
        rows = [
            r.split('\t')
            for r in rows
        ]

        c = Counter(
            batch for batch, group in groupby(rows, lambda r: r[1])
        )

        self.batches_with_non_uniq_names = {
            batch
            for batch, count in c.items()
            if count > 1
        }

        batches = [
            self._parse_batch(batch, list(group), filepaths)
            for batch, group in groupby(rows, lambda r: r[1])
        ]
        return batches


def parse_batches(rows: Iterable[str], filepaths: List[str]) -> List[Dict]:
    return MaxQuantParser().parse_batches(rows, filepaths)


