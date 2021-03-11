"""Testdocumentation

for job
"""

from __future__ import annotations

import copy
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    Set,
    Dict,
    List,
    Union,
    AnyStr,
    Mapping,
    Optional,
)
from operator import itemgetter

from . import OrderedSetType
from .need import Need
from .rule import Rule
from .cache import Cache
from .image import Image
from .include import Include

if TYPE_CHECKING:
    from .job_sequence import JobSequence

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


class Job():
    """Represents a Gitlab CI Job

    Attributes:
        script: The script to be executed.
        name: The name of the job.
    """
    def __init__(
        self,
        *args: Any,
        script: Union[AnyStr, List[str]],
        name: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        self._stage = ""
        self._name = ""
        self._image: Optional[Image] = None
        self._variables: Dict[str, str] = {}
        self._tags: OrderedSetType = {}
        self._rules: List[Rule] = []
        self._needs: List[Union[Need, Job, JobSequence]] = []
        self._scripts: List[str]
        self._artifacts_paths: OrderedSetType = {}
        self._cache: Optional[Cache] = None
        self._parents: List[JobSequence] = list()
        self._original: Optional[Job]
        """Only set if you get a :meth:`copy()` of this job"""

        if namespace and name:
            self._name = f"{namespace}-{name}"
            self._stage = namespace
        elif namespace:
            self._name = namespace
            self._stage = namespace
        elif name:
            self._name = name
            # default for unset stages is 'test' -> https://docs.gitlab.com/ee/ci/yaml/#stages
            self._stage = "test"
        else:
            raise ValueError("At least one of the parameters `name` or `namespace` have to be set.")

        self._name = self._name.replace("_", "-")
        self._stage = self._stage.replace("-", "_")

        if isinstance(script, str):
            self._scripts = [script]
        elif isinstance(script, list):
            self._scripts = script
        else:
            raise AttributeError("script parameter must be of type string or list of strings")

    @property
    def name(self) -> str:
        return self._name

    @property
    def stage(self) -> str:
        return self._stage

    def _extend_name(self, name: Optional[str]) -> None:
        if name:
            self._name += "-" + name.replace("_", "-")

    def _extend_stage(self, stage: Optional[str]) -> None:
        if stage:
            self._stage += "_" + stage.replace("-", "_")

    def _extend_namespace(self, namespace: Optional[str]) -> None:
        if namespace:
            self._extend_name(namespace)
            self._extend_stage(namespace)

    def _add_parent(self, parent: JobSequence) -> None:
        self._parents.append(parent)

    def prepend_scripts(self, *scripts: str) -> Job:
        self._scripts = list(scripts) + self._scripts
        return self

    def append_scripts(self, *scripts: str) -> Job:
        self._scripts.extend(scripts)
        return self

    def add_variables(self, **variables: str) -> Job:
        self._variables.update(variables)
        return self

    def add_tags(self, *tags: str) -> Job:
        for tag in tags:
            self._tags[tag] = None
        return self

    def add_artifacts_paths(self, *paths: str) -> Job:
        for path in paths:
            self._artifacts_paths[path] = None
        return self

    def set_cache(self, cache: Optional[Cache]) -> Job:
        """Sets the cache for the Job.

        Args:
            cache (Cache): Cache to use for this Job.

        Returns:
            JobSequence: Returns the modified :class:`Job` object.
        """
        if cache:
            self._cache = cache
        return self

    def append_rules(self, *rules: Rule) -> Job:
        self._rules.extend(rules)
        return self

    def prepend_rules(self, *rules: Rule) -> Job:
        self._rules = list(rules) + self._rules
        return self

    def add_needs(self, *needs: Union[Need, Job, JobSequence]) -> Job:
        self._needs.extend(needs)
        return self

    def set_image(self, image: Optional[Union[Image, str]]) -> Job:
        """Sets the image of this job.

        For a simple container image you can provide the origin of the image.
        If you want to set the entrypoint, you have to provide an Image object instead.

        Args:
            image (Optional[Union[Image, str]]): Can be either `string` or `Image`.

        Returns:
            Job: Returns the modified :class:`Job` object.
        """
        if image:
            if isinstance(image, str):
                image = Image(image)
            self._image = image
        return self

    def _get_all_instance_names(self) -> Set[str]:
        instance_names: Set[str] = set()
        for parent in self._parents:
            for postfix in parent._get_all_instance_names(self):
                if postfix:
                    instance_names.add(f"{self._name}-{postfix}".replace("-#unset#", ""))
                else:
                    instance_names.add(self._name)
        return instance_names

    def copy(self) -> Job:
        return self._copy_into(Job(name=".", script=copy.deepcopy(self._scripts)))

    def _copy_into(self, job: Job) -> Job:
        job._original = self
        job._name = self._name
        job._stage = self._stage

        job.set_image(self._image)
        job.add_variables(**copy.deepcopy(self._variables))
        job.add_tags(*list(self._tags.keys()))
        job.add_artifacts_paths(*list(self._artifacts_paths.keys()))
        job.set_cache(self._cache)
        job.append_rules(*self._rules)
        job.add_needs(*self._needs)
        job._parents = self._parents.copy()

        return job

    def render(self) -> Dict[str, Any]:
        from .job_sequence import \
            JobSequence  # late import to avoid circular dependencies

        rendered_job: Dict[str, Any] = {}

        if self._image:
            rendered_job.update({"image": self._image.render()})

        if self._needs:
            need_jobs: List[Job] = list()
            rendered_needs: List[Dict[str, Union[str, bool]]] = list()
            for need in self._needs:
                if isinstance(need, Job):
                    need_jobs.append(need)
                elif isinstance(need, JobSequence):
                    for job in need.last_jobs_executed:
                        need_jobs.append(job)
                elif isinstance(need, Need):
                    rendered_needs.append(need.render())
                else:
                    raise TypeError(f"Need '{need}' is of type {type(need)}.")

            job_names: Set[str] = set()
            for job in need_jobs:
                job_names.update(job._get_all_instance_names())

            for name in job_names:
                rendered_needs.append(Need(name).render())

            # sort needs by the name of the referenced job
            rendered_needs = sorted(rendered_needs, key=itemgetter("job"))

            rendered_job.update({"needs": rendered_needs})

        rendered_job.update({
            "stage": self._stage,
            "script": self._scripts,
        })

        if self._variables:
            rendered_job["variables"] = self._variables

        if self._rules:
            rendered_rules = []
            for rule in self._rules:
                rendered_rules.append(rule.render())
            rendered_job.update({"rules": rendered_rules})

        if self._artifacts_paths.keys():
            rendered_job.update({"artifacts": {
                "paths": list(self._artifacts_paths.keys()),
            }})

        if self._cache:
            rendered_job.update({"cache": self._cache.render()})

        if self._tags.keys():
            rendered_job["tags"] = list(self._tags.keys())

        return rendered_job


class TriggerStrategy(Enum):
    """Class with static values for ``TriggerStrategy`` used together with :class:`gcip.core.job.TriggerJob`. To construct an object."""
    DEPEND = "depend"


class TriggerJob(Job):
    def __init__(
        self,
        *args: Any,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        project: Optional[str] = None,
        branch: Optional[str] = None,
        includes: Union[Include, List[Include], None] = None,
        strategy: Optional[TriggerStrategy] = None,
        **kwargs: Mapping[Any, Any],
    ) -> None:
        """
        Class to create a Gitlab CI Trigger.

        You can create either a "Parent-child" or a "Multi-project" pipeline trigger.


        Args:
            project (Optional[str]): Used to create Multi-project pipeline trigger, exclusive to ``includes`` given Gitlab project name.
                e.g 'team1/project1'. Defaults to None.
            branch (Optional[str]): If ``project`` is given, you can specify which branch of ``project`` to trigger. Defaults to None.
            includes (Optional[List[Include]]): Used to create Parent-child pipeline trigger, exclusiv to ``project``. Defaults to None.
            strategy (Optional[TriggerStrategy]): Strategy of how the job behaves from the upstream pipeline.
                If :class:`TriggerStrategy.DEPEND`, any triggered job failed this job failed as well. Defaults to None.

        Raises:
            ValueError: If ``project`` and ``includes`` is given at the same time.
            ValueError: There is a Gitlab CI limitation, in "Parent-child" pipelines it is only allowed to add max. three includes.
        """

        if includes and project:
            raise ValueError(("You cannot specify 'include' and 'project' together. Either 'include' or 'project' is possible."))
        if not includes and not project:
            raise ValueError("Neither 'includes' nor 'project' is given.")

        super().__init__(name=name, namespace=namespace, script="none")

        self._project = project
        self._branch = branch
        self._strategy = strategy

        if not includes:
            self._includes = None
        elif isinstance(includes, Include):
            self._includes = [includes]
        elif isinstance(includes, list):
            if len(includes) > 3:
                raise ValueError(
                    (
                        "The length of 'includes' is limited to three."
                        "See https://docs.gitlab.com/ee/ci/parent_child_pipelines.html for more information."
                    )
                )
            self._includes = includes
        else:
            raise AttributeError("script parameter must be of type string or list of strings")

    def copy(self) -> TriggerJob:
        job_copy = TriggerJob(name=".", project=".")
        super()._copy_into(job_copy)

        job_copy._project = self._project
        job_copy._branch = self._branch
        job_copy._includes = self._includes
        job_copy._strategy = self._strategy
        return job_copy

    def render(self) -> Dict[Any, Any]:
        rendered_job = super().render()

        # remove unsupported keywords from TriggerJob
        rendered_job.pop("script")

        if "image" in rendered_job:
            rendered_job.pop("image")

        if "tags" in rendered_job:
            rendered_job.pop("tags")

        if "artifacts" in rendered_job:
            rendered_job.pop("artifacts")

        if "cache" in rendered_job:
            rendered_job.pop("cache")

        trigger: Dict[str, Union[str, List[Dict[str, str]]]] = {}

        # Child pipelines
        if self._includes:
            trigger.update({
                "include": [include.render() for include in self._includes],
            })

        # Multiproject pipelines
        if self._project:
            trigger.update({
                "project": self._project,
            })
            if self._branch:
                trigger.update({"branch": self._branch})

        if self._strategy:
            trigger.update({"strategy": self._strategy.value})

        rendered_job = {
            "trigger": trigger,
            **rendered_job
        }

        return rendered_job
