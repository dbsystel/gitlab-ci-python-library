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
        self._variables_for_initialization: Dict[str, str] = {}
        self._variables_for_replacement: Dict[str, str] = {}
        self._tags: OrderedSetType = {}
        self._tags_for_initialization: OrderedSetType = {}
        self._tags_for_replacement: OrderedSetType = {}
        self._artifacts_paths: OrderedSetType = {}
        self._scripts_to_prepend: List[str] = []
        self._scripts_to_append: List[str] = []
        self._rules_to_append: List[Rule] = []
        self._rules_to_prepend: List[Rule] = []
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

    def initialize_variables(self, **variables: str) -> None:
        """
        Works like :meth:`initialize_tags` but for variales.

        Args:
            variables (str): A keyword argument list which key-value-pairs will be applied as variable-value-pairs
                             to all downstream :class:`Job` s without variables already set.
        """
        self._variables_for_initialization.update(variables)

    def override_variables(self, **variables: str) -> None:
        """
        Works like :meth:`override_tags` but for variables.

        Args:
            variables (str): A keyword argument list which key-value-pairs will be set as variable-value-pairs
                             to all downstream :class:`Job` s.
        """
        self._variables_for_replacement.update(variables)

    def add_tags(self, *tags: str) -> None:
        for tag in tags:
            self._tags[tag] = None

    def initialize_tags(self, *tags: str) -> None:
        """
        Adds tags to downstream :class:`Job` s only if they haven't tags added yet.

        :meth:`initialize_tags` would be extended by :meth:`add_tags` and overridden
        by :meth:`override_tags` if one of the other methods is called too.

        Args:
            tags (str): One or more strings that will be applied to :class:`Job` s with empty tag list.
        """
        for tag in tags:
            self._tags_for_initialization[tag] = None

    def override_tags(self, *tags: str) -> None:
        """
        Will replace all tags from downstream :class:`Job` s.

        :meth:`override_tags` will also override tags set by :meth:`initialize_tags`
        but be extended by :meth:`add_tags` when one of the other methods is called too.

        Args:
            tags (str): One or more strings that will be set as tags to all downstream :class:`Job` s.
        """
        for tag in tags:
            self._tags_for_replacement[tag] = None

    def add_artifacts_paths(self, *paths: str) -> None:
        for path in paths:
            self._artifacts_paths[path] = None

    def append_rules(self, *rules: Rule) -> None:
        self._rules_to_append.extend(rules)

    def prepend_rules(self, *rules: Rule) -> None:
        self._rules_to_prepend = list(rules) + self._rules_to_prepend

    def add_needs(self, *needs: Need) -> None:
        self._needs.extend(needs)

    def prepend_scripts(self, *scripts: str) -> None:
        self._scripts_to_prepend = list(scripts) + self._scripts_to_prepend

    def append_scripts(self, *scripts: str) -> None:
        self._scripts_to_append.extend(scripts)

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

            if self._variables_for_initialization and not job._variables:
                job._variables = copy.deepcopy(self._variables_for_initialization)
            if self._variables_for_replacement:
                job._variables = copy.deepcopy(self._variables_for_replacement)
            job.add_variables(**copy.deepcopy(self._variables))

            if self._tags_for_initialization and not job._tags:
                job._tags = copy.deepcopy(self._tags_for_initialization)
            if self._tags_for_replacement:
                job._tags = copy.deepcopy(self._tags_for_replacement)
            job.add_tags(*list(self._tags.keys()))

            job.add_artifacts_paths(*list(self._artifacts_paths.keys()))
            job.append_rules(*self._rules_to_append)
            job.prepend_rules(*self._rules_to_prepend)
            job.add_needs(*self._needs)
            job.prepend_scripts(*self._scripts_to_prepend)
            job.append_scripts(*self._scripts_to_append)

        return all_jobs
