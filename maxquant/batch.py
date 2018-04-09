import re
import shlex
from itertools import groupby, zip_longest
from os.path import basename
from typing import Iterable, Dict, List, Any

import sys
from scheduler.job import JobSpec, Batch

from maxquant import const
from maxquant.const import BATCHES_WITH_FILENAME_BINDING


class MaxQuantParser:
    def __init__(self, file_paths: List[str], threads: int):
        self.threads = threads or 1
        self.file_paths = file_paths

    @staticmethod
    def _parse_job(batch_name: str, row: str, job_name: str, threads: int) -> JobSpec:
        _num, batch, command, arguments, *_ = row
        arguments = [a.strip('"') for a in shlex.split(arguments)]

        if job_name is None:
            job_name = re.sub(r'\W+', '_', arguments[3]).strip("_")

        if threads > 1:
            sys.stderr.write('Patching threads={threads} for job {name}\n'.format(
                name=job_name,
                threads=threads
            ))

        return JobSpec(
            command=command,
            args=arguments,
            name='{}-{}'.format(batch_name, job_name),
            num_slots=threads,
        )

    def _parse_batch(self, batch_number: int, name: str, rows: List[str]) -> Batch:
        batch_name = name.split('.')[-1]

        batch_threads = 1
        if batch_name in const.SINGLE_MULTICORE_BATCHES:
            batch_threads = self.threads

        # TODO: fix this
        if batch_name in BATCHES_WITH_FILENAME_BINDING:
            names = [
                basename(f)
                for f in self.file_paths
            ]
        else:
            names = tuple()

        batch_name = '{:02d}-{}'.format(batch_number + 1, batch_name)

        jobs = [
            self._parse_job(batch_name, row, name, batch_threads)
            for row, name in zip_longest(rows, names)
        ]
        return Batch(
            name=batch_name,
            jobs=jobs,
        )

    def parse_batches(self, rows: Iterable[str]) -> List[Batch]:
        rows = [
            r.split('\t')
            for r in rows
        ]

        batches = [
            self._parse_batch(i, batch, list(group))
            for i, (batch, group) in enumerate(groupby(rows, lambda r: r[1]))
        ]
        return batches


def parse_batches(rows: Iterable[str], filepaths: List[str], threads: int) -> List[Batch]:
    return MaxQuantParser(filepaths, threads).parse_batches(rows)


