import re
import shlex
from itertools import groupby, zip_longest
from os.path import basename
from typing import Iterable, Dict, List, Any

from maxquant.const import BATCHES_WITH_FILENAME_BINDING


class MaxQuantParser:
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths

    @staticmethod
    def _parse_job(batch_name: str, row: str, job_name: str) -> Dict[str, Any]:
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

    def _parse_batch(self, batch_number: int, name: str, rows: List[str]) -> Dict[str, Any]:
        batch_name = name.split('.')[-1]

        # TODO: fix this
        if batch_name in BATCHES_WITH_FILENAME_BINDING:
            names = [
                basename(f)
                for f in self.file_paths
            ]
        else:
            names = tuple()

        batch_name = '{0:02d}-{}'.format(batch_number + 1, batch_name)

        jobs = [
            self._parse_job(batch_name, row, name)
            for row, name in zip_longest(rows, names)
        ]
        return {
            'name': batch_name,
            'jobs': jobs,
        }

    def parse_batches(self, rows: Iterable[str]) -> List[Dict]:
        rows = [
            r.split('\t')
            for r in rows
        ]

        batches = [
            self._parse_batch(i, batch, list(group))
            for i, (batch, group) in enumerate(groupby(rows, lambda r: r[1]))
        ]
        return batches


def parse_batches(rows: Iterable[str], filepaths: List[str]) -> List[Dict]:
    return MaxQuantParser(filepaths).parse_batches(rows)


