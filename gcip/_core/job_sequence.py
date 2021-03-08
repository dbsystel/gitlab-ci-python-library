from __future__ import annotations

import copy
from typing import (
    Set,
    Dict,
    List,
    Union,
    Optional,
    TypedDict,
)

from . import OrderedSetType
from .job import Job
from .need import Need
from .rule import Rule
from .cache import Cache
from .image import Image

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


class ChildDict(TypedDict):
    object: Union[Job, JobSequence]
    namespace: Optional[str]
    name: Optional[str]


class JobSequence():
    def __init__(self) -> None:
        super().__init__()
        self._children: List[ChildDict] = list()
        self._image_for_initialization: Optional[Union[Image, str]] = None
        self._image_for_replacement: Optional[Union[Image, str]] = None
        self._variables: Dict[str, str] = {}
        self._variables_for_initialization: Dict[str, str] = {}
        self._variables_for_replacement: Dict[str, str] = {}
        self._tags: OrderedSetType = {}
        self._tags_for_initialization: OrderedSetType = {}
        self._tags_for_replacement: OrderedSetType = {}
        self._artifacts_paths: OrderedSetType = {}
        self._cache: Optional[Cache] = None
        self._cache_for_initialization: Optional[Cache] = None
        self._scripts_to_prepend: List[str] = []
        self._scripts_to_append: List[str] = []
        self._rules_to_append: List[Rule] = []
        self._rules_to_prepend: List[Rule] = []
        self._rules_for_initialization: List[Rule] = []
        self._rules_for_replacement: List[Rule] = []
        self._needs: List[Union[Job, Need]] = []
        self._parents: List[JobSequence] = list()

    def _add_parent(self, parent: JobSequence) -> None:
        self._parents.append(parent)

    def add_children(
        self, *jobs_or_sequences: Union[Job, JobSequence], namespace: Optional[str] = None, name: Optional[str] = None
    ) -> JobSequence:
        for child in jobs_or_sequences:
            child._add_parent(self)
            self._children.append({
                "object": child,
                "namespace": namespace,
                "name": name
            })
        return self

    def add_variables(self, **variables: str) -> JobSequence:
        self._variables.update(variables)
        return self

    def initialize_variables(self, **variables: str) -> JobSequence:
        """
        Works like :meth:`initialize_tags` but for variales.

        Args:
            variables (str): A keyword argument list which key-value-pairs will be applied as variable-value-pairs
                             to all downstream :class:`Job` s without variables already set.
        """
        self._variables_for_initialization.update(variables)
        return self

    def override_variables(self, **variables: str) -> JobSequence:
        """
        Works like :meth:`override_tags` but for variables.

        Args:
            variables (str): A keyword argument list which key-value-pairs will be set as variable-value-pairs
                             to all downstream :class:`Job` s.
        """
        self._variables_for_replacement.update(variables)
        return self

    def set_cache(self, cache: Cache) -> JobSequence:
        """Sets the cache for the corresponding JobSequence.
        This will override any previously set chaches on this sequence or child sequences/jobs.

        Args:
            cache (Cache): Cache to use for the JobSequence and its Jobs.

        Returns:
            JobSequence: Returns the modified Sequence object.
        """
        self._cache = cache
        return self

    def initialize_cache(self, cache: Cache) -> JobSequence:
        """Sets the cache of child sequences/jobs only  if not set before.

        Args:
            cache (Cache): Cache to use for the JobSequence and its Jobs.

        Returns:
            JobSequence: Returns the modified Sequence object.
        """
        self._cache_for_initialization = cache
        return self

    def add_tags(self, *tags: str) -> JobSequence:
        for tag in tags:
            self._tags[tag] = None
        return self

    def initialize_tags(self, *tags: str) -> JobSequence:
        """
        Adds tags to downstream :class:`Job` s only if they haven't tags added yet.

        :meth:`initialize_tags` would be extended by :meth:`add_tags` and overridden
        by :meth:`override_tags` if one of the other methods is called too.

        Args:
            tags (str): One or more strings that will be applied to :class:`Job` s with empty tag list.
        """
        for tag in tags:
            self._tags_for_initialization[tag] = None
        return self

    def override_tags(self, *tags: str) -> JobSequence:
        """
        Will replace all tags from downstream :class:`Job` s.

        :meth:`override_tags` will also override tags set by :meth:`initialize_tags`
        but be extended by :meth:`add_tags` when one of the other methods is called too.

        Args:
            tags (str): One or more strings that will be set as tags to all downstream :class:`Job` s.
        """
        for tag in tags:
            self._tags_for_replacement[tag] = None
        return self

    def add_artifacts_paths(self, *paths: str) -> JobSequence:
        for path in paths:
            self._artifacts_paths[path] = None
        return self

    def append_rules(self, *rules: Rule) -> JobSequence:
        self._rules_to_append.extend(rules)
        return self

    def prepend_rules(self, *rules: Rule) -> JobSequence:
        self._rules_to_prepend = list(rules) + self._rules_to_prepend
        return self

    def initialize_rules(self, *rules: Rule) -> JobSequence:
        """
        Works like :meth:`initialize_tags` but for rules.

        Args:
            rules (Rule): A list of :class:`Rule` s that will be applied to :class:`Job` s with empty rules list.
        """
        self._rules_for_initialization.extend(rules)
        return self

    def override_rules(self, *rules: Rule) -> JobSequence:
        """
        Works like :meth:`override_tags` but for rules.

        Args:
            rules (Rule): A list of :class:`Rule` s that will be replace all downstream :class:`Job` s rules.
        """
        self._rules_for_replacement.extend(rules)
        return self

    def add_needs(self, *needs: Union[Job, Need]) -> JobSequence:
        """
        Only the first job of the sequence get the ``need`` appended to, as well as all following jobs with
        the same stage.
        """
        self._needs.extend(needs)
        return self

    def prepend_scripts(self, *scripts: str) -> JobSequence:
        self._scripts_to_prepend = list(scripts) + self._scripts_to_prepend
        return self

    def append_scripts(self, *scripts: str) -> JobSequence:
        self._scripts_to_append.extend(scripts)
        return self

    def initialize_image(self, image: Union[Image, str]) -> JobSequence:
        """Initializes given `image` to all downstream `Job`s which do not have
        an `image` set.

        Args:
            image (Union[Image, str]): The image to set to all downstream :class:`Job`'s.

        Returns:
            JobSequence: Modified `sequence` object.
        """
        if image:
            self._image_for_initialization = image
        return self

    def override_image(self, image: Union[Image, str]) -> JobSequence:
        """Initializes and override's `image` to all downstream `Job`s.
        In consequence, all downstream `Job`s will be started with `image`.

        Args:
            image (str): The image to set for all downstream :class:`Job`'s.

        Returns:
            JobSequence: Modified `sequence` object.
        """
        if image:
            self._image_for_replacement = image
        return self

    def _get_all_instance_names(self, child: Union[Job, JobSequence]) -> Set[str]:
        instance_names: Set[str] = set()
        for parent in self._parents:
            instance_names.update(parent._get_all_instance_names(self))

        child_instance_names: Set[str] = set()
        child_instance_name: str
        for item in self._children:
            if item["object"] == child:
                if item["namespace"] is not None:
                    if item["name"]:
                        child_instance_name = f"{item['namespace']}-{item['name']}"
                    else:
                        child_instance_name = item["namespace"]
                elif item["name"] is not None:
                    child_instance_name = item["name"]
                else:
                    child_instance_name = "#unset#"

                # all job names have '-' instead of '_'
                child_instance_names.add(child_instance_name.replace("_", "-"))

        return_values: Set[str] = set()
        # add instane names of this sequence to all instance
        # names of its children
        if instance_names:
            for child_instance_name in child_instance_names:
                for instance_name in instance_names:
                    return_values.add(f"{child_instance_name}-{instance_name}")
        else:
            return_values = child_instance_names

        return return_values

    @property
    def last_jobs_executed(self) -> List[Job]:
        all_jobs = self.populated_jobs
        stages: Dict[str, None] = {}
        for job in all_jobs:
            # use the keys of dictionary as ordered set
            stages[job.stage] = None

        last_stage = list(stages.keys())[-1]
        last_executed_jobs: List[Job] = list()
        for job in all_jobs:
            if job._stage == last_stage:
                if job._original:
                    last_executed_jobs.append(job._original)
                else:
                    raise AttributeError("job._original is None, because the job is not a copy of another job")

        return last_executed_jobs

    @property
    def populated_jobs(self) -> List[Job]:
        all_jobs: List[Job] = []
        for child in self._children:
            if isinstance(child["object"], JobSequence):
                for job_copy in child["object"].populated_jobs:
                    job_copy._extend_namespace(child["namespace"])
                    job_copy._extend_name(child["name"])
                    all_jobs.append(job_copy)
            elif isinstance(child["object"], Job):
                job_copy = child["object"].copy()
                job_copy._extend_namespace(child["namespace"])
                job_copy._extend_name(child["name"])
                all_jobs.append(job_copy)

        if len(all_jobs) > 0:
            first_job = all_jobs[0]
            first_job.add_needs(*self._needs)
            for job in all_jobs[1:]:
                if job._stage == first_job.stage:
                    job.add_needs(*self._needs)

        for job in all_jobs:

            if self._image_for_initialization and not job._image:
                job.set_image(self._image_for_initialization)
            if self._image_for_replacement:
                job.set_image(self._image_for_replacement)

            if self._variables_for_initialization and not job._variables:
                job._variables = copy.deepcopy(self._variables_for_initialization)
            if self._variables_for_replacement:
                job._variables = copy.deepcopy(self._variables_for_replacement)
            job.add_variables(**copy.deepcopy(self._variables))

            if self._cache_for_initialization and not job._cache:
                job._cache = copy.deepcopy(self._cache_for_initialization)
            job.set_cache(copy.deepcopy(self._cache))

            if self._tags_for_initialization and not job._tags:
                job._tags = copy.deepcopy(self._tags_for_initialization)
            if self._tags_for_replacement:
                job._tags = copy.deepcopy(self._tags_for_replacement)
            job.add_tags(*list(self._tags.keys()))

            job.add_artifacts_paths(*list(self._artifacts_paths.keys()))

            if self._rules_for_initialization and not job._rules:
                job._rules = copy.deepcopy(self._rules_for_initialization)
            if self._rules_for_replacement:
                job._rules = copy.deepcopy(self._rules_for_replacement)
            job.append_rules(*self._rules_to_append)
            job.prepend_rules(*self._rules_to_prepend)

            job.prepend_scripts(*self._scripts_to_prepend)
            job.append_scripts(*self._scripts_to_append)

        return all_jobs
