"""A Sequence collects multiple `gcip.core.job.Job`s and/or other `gcip.core.sequence.Sequence`s into a group.

This concept is no official representation of a Gitlab CI keyword. But it is such a powerful
extension of the Gitlab CI core funtionality and an essential building block of the gcip, that
it is conained in the `gcip.core` module.

A Sequence offers a mostly similar interface like `gcip.core.job.Job`s that allows to modify
all Jobs and child Sequences contained into that parent Sequence. For example: Instad of calling
`add_tag()` on a dozens of Jobs you can call `add_tag()` on the sequence that contain those Jobs.
The tag will then be applied to all Jobs in that Sequence and recursively to all Jobs within child
Sequenes of that Sequence.

Sequences must be added to a `gcip.core.pipeline.Pipeline`, either directly or as part of other Sequences.
That means Sequences are not meant to be a throw away configuration container for a bunch ob Jobs.
This is because adding a Job to a Sequence creates a copy of that Job, which will be inderectly added to
the `Pipeline` by that Sequence. Not adding that Sequence to a Pipeline means also not adding its Jobs
to the Pipeline. If other parts of the Pipeline have dependencies to those Jobs, they will be broken.

As said before, adding a Job to a Sequence creates copies of that Job. To void conflicts between Jobs,
you should set `name` and/or `stage` when adding the job (or child sequence). The sequence will add
the `name`/`stage` to the ones of the Job, when rendering the pipeline. If you do not set those
identifiers, or you set equal name/stages for jobs and sequences, you provoke having two or more
jobs having the same name in the pipeline. The gcip will raise a ValueError, to avoid unexpected
pipeline behavior. You can read more information in the chapter "Stages allow reuse of jobs
and sequences" of the user documantation.
"""
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
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


class ChildDict(TypedDict):
    """This data structure is supposed to store one child of a `Sequence` with all required information about that child."""

    child: Union[Job, Sequence]
    """The child to store - a `gcip.core.job.Job` or `Sequence`."""
    stage: Optional[str]
    """The stage with whom the `child` was added to the `Sequence`."""
    name: Optional[str]
    """The name with whom the `child` was added to the `Sequence`."""


class Sequence:
    """A Sequence collects multiple `gcip.core.job.Job`s and/or other `gcip.core.sequence.Sequence`s into a group."""

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
        self._artifacts_paths_for_initialization: OrderedSetType = {}
        self._artifacts_paths_for_replacement: OrderedSetType = {}
        self._cache: Optional[Cache] = None
        self._cache_for_initialization: Optional[Cache] = None
        self._scripts_to_prepend: List[str] = []
        self._scripts_to_append: List[str] = []
        self._rules_to_append: List[Rule] = []
        self._rules_to_prepend: List[Rule] = []
        self._rules_for_initialization: List[Rule] = []
        self._rules_for_replacement: List[Rule] = []
        self._needs: List[Union[Job, Need]] = []
        self._parents: List[Sequence] = list()

    def _add_parent(self, parent: Sequence) -> None:
        self._parents.append(parent)

    def add_children(
        self,
        *jobs_or_sequences: Union[Job, Sequence],
        stage: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Sequence:
        """Add `gcip.core.job.Job`s or other `gcip.core.sequence.Sequence`s to this sequence.

        Adding a child creates a copy of that child. You should provide a name or stage
        when adding children, to make them different from other places where they will be used.

        Args:
            jobs_or_sequences (Union[Job, Sequence]): One or more jobs or sequences to be added to this sequence.
            stage (Optional[str], optional): Adds a stages component to all children added. Defaults to None.
            name (Optional[str], optional): Adds a name component to all children added. Defaults to None.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        for child in jobs_or_sequences:
            child._add_parent(self)
            self._children.append({"child": child, "stage": stage, "name": name})
        return self

    def add_variables(self, **variables: str) -> Sequence:
        """Calling `gcip.core.job.Job.add_variables()` to all jobs within this sequence.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._variables.update(variables)
        return self

    def initialize_variables(self, **variables: str) -> Sequence:
        """Calling `gcip.core.job.Job.add_variables()` to all jobs within this sequence that haven't been added variables before.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._variables_for_initialization.update(variables)
        return self

    def override_variables(self, **variables: str) -> Sequence:
        """Calling `gcip.core.job.Job.add_variables()` to all jobs within this sequence and overriding any previously added variables to that jobs.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._variables_for_replacement.update(variables)
        return self

    def set_cache(self, cache: Cache) -> Sequence:
        """Calling `gcip.core.job.Job.set_cache()` to all jobs within this sequence.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._cache = cache
        return self

    def initialize_cache(self, cache: Cache) -> Sequence:
        """Calling `gcip.core.job.Job.set_cache()` to all jobs within this sequence that haven't been set the cache before.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._cache_for_initialization = cache
        return self

    def add_tags(self, *tags: str) -> Sequence:
        """Calling `gcip.core.job.Job.add_tags()` to all jobs within this sequence.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        for tag in tags:
            self._tags[tag] = None
        return self

    def initialize_tags(self, *tags: str) -> Sequence:
        """Calling `gcip.core.job.Job.add_tags()` to all jobs within this sequence that haven't been added tags before.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        for tag in tags:
            self._tags_for_initialization[tag] = None
        return self

    def override_tags(self, *tags: str) -> Sequence:
        """Calling `gcip.core.job.Job.add_tags()` to all jobs within this sequence and overriding any previously added tags to that jobs.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        for tag in tags:
            self._tags_for_replacement[tag] = None
        return self

    def add_artifacts_paths(self, *paths: str) -> Sequence:
        """Calling `gcip.core.job.Job.add_artifacts_paths()` to all jobs within this sequence.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        for path in paths:
            self._artifacts_paths[path] = None
        return self

    def initialize_artifacts_paths(self, *paths: str) -> Sequence:
        """Calling `gcip.core.job.Job.add_artifacts_paths()` to all jobs within this sequence that haven't been added artifacts paths before.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        for path in paths:
            self._artifacts_paths_for_initialization[path] = None
        return self

    def override_artifacts_paths(self, *paths: str) -> Sequence:
        """Calling `gcip.core.job.Job.add_artifacts_paths()` to all jobs within this sequence and overriding any previously added artifacts paths to that jobs.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        for path in paths:
            self._artifacts_paths_for_replacement[path] = None
        return self

    def append_rules(self, *rules: Rule) -> Sequence:
        """Calling `gcip.core.job.Job.append_rules()` to all jobs within this sequence.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._rules_to_append.extend(rules)
        return self

    def prepend_rules(self, *rules: Rule) -> Sequence:
        """Calling `gcip.core.job.Job.prepend_rules()` to all jobs within this sequence.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._rules_to_prepend = list(rules) + self._rules_to_prepend
        return self

    def initialize_rules(self, *rules: Rule) -> Sequence:
        """Calling `gcip.core.job.Job.append_rules()` to all jobs within this sequence that haven't been added rules before.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._rules_for_initialization.extend(rules)
        return self

    def override_rules(self, *rules: Rule) -> Sequence:
        """Calling `gcip.core.job.Job.override_rules()` to all jobs within this sequence and overriding any previously added rules to that jobs.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._rules_for_replacement.extend(rules)
        return self

    def add_needs(self, *needs: Union[Job, Need]) -> Sequence:
        """Calling `gcip.core.job.Job.add_need()` to all jobs within the first stage of this sequence.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._needs.extend(needs)
        return self

    def prepend_scripts(self, *scripts: str) -> Sequence:
        """Calling `gcip.core.job.Job.prepend_scripts()` to all jobs within this sequence.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._scripts_to_prepend = list(scripts) + self._scripts_to_prepend
        return self

    def append_scripts(self, *scripts: str) -> Sequence:
        """Calling `gcip.core.job.Job.append_scripts()` to all jobs within this sequence.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        self._scripts_to_append.extend(scripts)
        return self

    def initialize_image(self, image: Union[Image, str]) -> Sequence:
        """Calling `gcip.core.job.Job.set_image()` to all jobs within this sequence.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        if image:
            self._image_for_initialization = image
        return self

    def override_image(self, image: Union[Image, str]) -> Sequence:
        """Calling `gcip.core.job.Job.set_image()` to all jobs within this sequence that haven't been set the image before.

        Returns:
            `Sequence`: The modified `Sequence` object.
        """
        if image:
            self._image_for_replacement = image
        return self

    def _get_all_instance_names(self, child: Union[Job, Sequence]) -> Set[str]:
        """Return all instance names from the given child.

        That means all combinations of the childs name and stage within this
        sequence and all parent sequences.
        """

        # first get all instance names from parents of this sequence
        own_instance_names: Set[str] = set()
        for parent in self._parents:
            own_instance_names.update(parent._get_all_instance_names(self))

        # second get all instance names of the child within this sequence
        child_instance_names: Set[str] = set()
        child_instance_name: str
        for item in self._children:
            if item["child"] == child:
                child_name = item["name"]
                child_stage = item["stage"]
                if child_stage:
                    if child_name:
                        child_instance_name = f"{child_stage}-{child_name}"
                    else:
                        child_instance_name = child_stage
                elif child_name:
                    child_instance_name = child_name
                else:
                    child_instance_name = ""

                # all job names have '-' instead of '_'
                child_instance_names.add(child_instance_name.replace("_", "-"))

        # third combine all instance names of this sequences
        # with all instance names of the child
        return_values: Set[str] = set()
        if own_instance_names:
            for child_instance_name in child_instance_names:
                for instance_name in own_instance_names:
                    if child_instance_name:
                        return_values.add(f"{child_instance_name}-{instance_name}")
                    else:
                        return_values.add(instance_name)
        else:
            return_values = child_instance_names

        return return_values

    @property
    def last_jobs_executed(self) -> List[Job]:
        """This property returns all Jobs from the last stage of this sequence.

        This is typically be requested from a job which has setup this sequence as need,
        to determine all actual jobs of this sequence as need.
        """
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
        """Returns a list with populated copies of all nested jobs of this sequence.

        Populated means, that all attributes of a Job which depends on its context are resolved
        to their final values. The context is primarily the sequence within the jobs resides but
        also dependencies to other jobs and sequences. Thus this sequence will apply its own
        configuration, like variables to add, tags to set, etc., to all its jobs and sequences.

        Copies means what it says, that the returned job are not the same job objects, originally
        added to this sequence, but copies of them.

        Nested means, that also jobs from sequences within this sequence, are returned, as well
        as jobs from sequences within sequences within this sequence and so on.

        Returns:
            List[Job]: A list of copies of all nested jobs of this sequence with their final attribute values.
        """
        all_jobs: List[Job] = []
        for item in self._children:
            child = item["child"]
            child_name = item["name"]
            child_stage = item["stage"]
            if isinstance(child, Sequence):
                for job_copy in child.populated_jobs:
                    job_copy._extend_stage(child_stage)
                    job_copy._extend_name(child_name)
                    all_jobs.append(job_copy)
            elif isinstance(child, Job):
                job_copy = child.copy()
                job_copy._extend_stage(child_stage)
                job_copy._extend_name(child_name)
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

            if self._artifacts_paths_for_initialization and not job._artifacts_paths:
                job._artifacts_paths = copy.deepcopy(self._artifacts_paths_for_initialization)
            if self._artifacts_paths_for_replacement:
                job._artifacts_paths = copy.deepcopy(self._artifacts_paths_for_replacement)
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
