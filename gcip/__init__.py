from __future__ import annotations

import copy
from enum import Enum
from typing import (
    Any,
    Set,
    Dict,
    List,
    Union,
    AnyStr,
    Optional,
)

import yaml
from pkg_resources import (
    DistributionNotFound,
    get_distribution,
)

try:
    _distribution = get_distribution("gcip")
    __version__ = _distribution.version
    __doc__ = _distribution.project_name
except DistributionNotFound:
    __version__ = "unknown"


class WhenStatement(Enum):
    ALWAYS = "always"
    DELAYED = "delayed"
    MANUAL = "manual"
    NEVER = "never"
    ON_FAILURE = "on_failure"
    ON_SUCCESS = "on_success"


class Rule():
    def __init__(
        self,
        *args: Any,
        if_statement: str,
        when: WhenStatement = WhenStatement.ON_SUCCESS,
        allow_failure: bool = False,
    ) -> None:
        self._if = if_statement
        self._when = when.value
        self._allow_failure = allow_failure

    def render(self) -> Dict[str, Union[str, bool]]:
        return {
            "if": self._if,
            "when": self._when,
            "allow_failure": self._allow_failure,
        }


class Job():
    def __init__(
        self,
        *args: Any,
        name: str,
        script: Union[AnyStr, List[str]],
        stage: Optional[str] = None,
    ):
        self._name = name
        self._stage = stage if stage is not None else name
        self._image: Optional[str] = None
        self._variables: Dict[str, str] = {}
        self._tags: Set[str] = set()
        self._rules: List[Rule] = []
        self._script: List[str]

        if isinstance(script, str):
            self._script = [script]
        elif isinstance(script, list):
            self._script = script
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
            self._name += "_" + name

    def _extend_stage(self, stage: str) -> None:
        if stage:
            self._stage += "_" + stage

    def add_namespace(self, namespace: Optional[str]) -> None:
        if namespace:
            self._extend_name(namespace)
            self._extend_stage(namespace)

    def prepend_script(self, *script: str) -> None:
        self._script = list(script) + self._script

    def append_script(self, *script: str) -> None:
        self._script.extend(script)

    def add_variables(self, **variables: str) -> None:
        self._variables.update(variables)

    def add_tags(self, *tags: str) -> None:
        self._tags.update(tags)

    def add_rules(self, *rules: Rule) -> None:
        self._rules.extend(rules)

    def set_image(self, image: Optional[str]) -> None:
        if image:
            self._image = image

    def copy(self) -> Job:
        job_copy = Job(
            name=self._name,
            script=copy.deepcopy(self._script),
            stage=self._stage,
        )
        job_copy.set_image(self._image)
        job_copy.add_variables(**copy.deepcopy(self._variables))
        job_copy.add_tags(*self._tags)
        job_copy.add_rules(*self._rules)
        return job_copy

    def render(self) -> Dict[str, Any]:
        rendered_job: Dict[str, Any] = {
            "script": self._script,
            "variables": self._variables,
            "tags": list(self._tags),
        }

        if len(self._rules) > 0:
            rendered_rules = []
            for rule in self._rules:
                rendered_rules.append(rule.render())
            rendered_job.update({"rules": rendered_rules})

        if self._image is not None:
            rendered_job.update({"image": self._image})

        return rendered_job


class JobSequence():
    def __init__(self) -> None:
        super().__init__()
        self._jobs: List[Union[Job, JobSequence]] = list()
        self._name_extension: Optional[str] = None
        self._namespace: Optional[str] = None
        self._image: Optional[str] = None
        self._variables: Dict[str, str] = {}
        self._tags: Set[str] = set()
        self._prepend_scripts: List[str] = []
        self._append_scripts: List[str] = []
        self._rules: List[Rule] = []

    def _extend_name(self, name: Optional[str]) -> None:
        if name:
            if self._name_extension:
                self._name_extension += "_" + name
            else:
                self._name_extension = name

    def add_namespace(self, namespace: Optional[str]) -> None:
        if namespace:
            if self._namespace:
                self._namespace += namespace
            else:
                self._namespace = namespace

    def add_sequence(self, job_sequence: JobSequence, *args: Any, namespace: Optional[str] = None, name: Optional[str] = None) -> None:
        job_sequence.add_namespace(namespace)
        job_sequence._extend_name(name)
        self._jobs.append(job_sequence)

    def add_jobs(self, *jobs: Job, namespace: Optional[str] = None, name: Optional[str] = None) -> None:
        for job in jobs:
            job.add_namespace(namespace)
            job._extend_name(name)
            self._jobs.append(job)

    def add_variables(self, **variables: str) -> None:
        self._variables.update(variables)

    def add_tags(self, *tags: str) -> None:
        self._tags.update(tags)

    def add_rules(self, *rules: Rule) -> None:
        self._rules.extend(rules)

    def prepend_script(self, *script: str) -> None:
        self._prepend_scripts = list(script) + self._prepend_scripts

    def append_script(self, *script: str) -> None:
        self._append_scripts.extend(script)

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
            job.add_namespace(self._namespace)
            job._extend_name(self._name_extension)
            job.set_image(self._image)
            job.add_variables(**copy.deepcopy(self._variables))
            job.add_tags(*self._tags)
            job.add_rules(*self._rules)
            job.prepend_script(*self._prepend_scripts)
            job.append_script(*self._append_scripts)

        return all_jobs


class Pipeline(JobSequence):
    def render(self) -> Dict[str, Any]:
        stages: Dict[str, None] = {}
        pipline: Dict[str, Any] = {}
        job_copies = self.populated_jobs

        for job in job_copies:
            # use the keys of dictionary as ordered set
            stages[job.stage] = None

        pipline["stages"] = list(stages.keys())
        for job in job_copies:
            rendered_job = job.render()
            rendered_job["stage"] = job.stage
            pipline[job.name] = rendered_job
        return pipline

    def print_yaml(self) -> None:
        print(yaml.dump(self.render(), default_flow_style=False, sort_keys=False))
