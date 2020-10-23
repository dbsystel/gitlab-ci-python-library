from __future__ import annotations

import copy
from typing import Dict, List, Union, Optional

from . import OrderedSetType
from .job import Job, Need
from .rule import Rule

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


class JobSequence():
    def __init__(self) -> None:
        super().__init__()
        self._jobs: List[Union[Job, JobSequence]] = list()
        self._name_extension: Optional[str] = None
        self._namespace: Optional[str] = None
        self._image: Optional[str] = None
        self._variables: Dict[str, str] = {}
        self._tags: OrderedSetType = {}
        self._artifacts_paths: OrderedSetType = {}
        self._prepend_scripts: List[str] = []
        self._append_scripts: List[str] = []
        self._append_rules: List[Rule] = []
        self._prepend_rules: List[Rule] = []
        self._needs: List[Need] = []

    def _extend_name(self, name: Optional[str]) -> None:
        if name:
            if self._name_extension:
                self._name_extension += "_" + name
            else:
                self._name_extension = name

    def _extend_namespace(self, namespace: Optional[str]) -> None:
        if namespace:
            if self._namespace:
                self._namespace += namespace
            else:
                self._namespace = namespace

    def add_sequences(self, *job_sequences: JobSequence, namespace: Optional[str] = None, name: Optional[str] = None) -> None:
        for sequence in job_sequences:
            sequence._extend_namespace(namespace)
            sequence._extend_name(name)
            self._jobs.append(sequence)

    def add_jobs(self, *jobs: Job, namespace: Optional[str] = None, name: Optional[str] = None) -> None:
        for job in jobs:
            job._extend_namespace(namespace)
            job._extend_name(name)
            self._jobs.append(job)

    def add_variables(self, **variables: str) -> None:
        self._variables.update(variables)

    def add_tags(self, *tags: str) -> None:
        for tag in tags:
            self._tags[tag] = None

    def add_artifacts_paths(self, *paths: str) -> None:
        for path in paths:
            self._artifacts_paths[path] = None

    def append_rules(self, *rules: Rule) -> None:
        self._append_rules.extend(rules)

    def prepend_rules(self, *rules: Rule) -> None:
        self._prepend_rules = list(rules) + self._prepend_rules

    def add_needs(self, *needs: Need) -> None:
        self._needs.extend(needs)

    def prepend_scripts(self, *scripts: str) -> None:
        self._prepend_scripts = list(scripts) + self._prepend_scripts

    def append_scripts(self, *scripts: str) -> None:
        self._append_scripts.extend(scripts)

    def set_image(self, image: str) -> None:
        if image:
            self._image = image

    @property
    def populated_jobs(self) -> List[Job]:
        all_jobs: List[Job] = []
        for job in self._jobs:
            if isinstance(job, JobSequence):
                all_jobs += job.populated_jobs
            elif isinstance(job, Job):
                all_jobs.append(job.copy())

        for job in all_jobs:
            job._extend_namespace(self._namespace)
            job._extend_name(self._name_extension)
            job.set_image(self._image)
            job.add_variables(**copy.deepcopy(self._variables))
            job.add_tags(*list(self._tags.keys()))
            job.add_artifacts_paths(*list(self._artifacts_paths.keys()))
            job.append_rules(*self._append_rules)
            job.prepend_rules(*self._prepend_rules)
            job.add_needs(*self._needs)
            job.prepend_scripts(*self._prepend_scripts)
            job.append_scripts(*self._append_scripts)

        return all_jobs
