import copy
from enum import Enum
from typing import Dict, List

import yaml
from pkg_resources import (
    DistributionNotFound,
    get_distribution,
)

try:
    _distribution = get_distribution("custom-cdk")
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
        *args,
        if_statement: str,
        when: WhenStatement = WhenStatement.ON_SUCCESS,
        allow_failure: bool = False,
    ):
        self._if = if_statement
        self._when = when.value
        self._allow_failure = allow_failure

    def render(self):
        return {
            "if": self._if,
            "when": self._when,
            "allow_failure": self._allow_failure,
        }


class Job():
    def __init__(
        self,
        *args,
        name: str,
        script: List[str],
    ):
        self._basename = name
        self._name = name
        self._namespace = None
        self._image = None
        self._variables = {}
        self._tags = set()
        self._rules = []

        if type(script) == str:
            self._script = [script]
        elif type(script) == list:
            self._script = script
        else:
            raise AttributeError("script parameter must be of type string or list of strings")

    @property
    def name(self):
        return self._name + (f"_{self._namespace}" if self._namespace is not None else "")

    @property
    def stage(self):
        return self._basename + (f"_{self._namespace}" if self._namespace is not None else "")

    def add_to_name(self, name: str):
        if name is None:
            return
        self._name += "_" + name

    def prepend_script(self, script: str):
        if type(script) == str:
            script = [script]
        self._script = script + self._script

    def append_script(self, script: str):
        if type(script) == str:
            script = [script]
        self._script += script

    def add_variables(self, **variables: Dict[str, str]):
        self._variables.update(variables)

    def add_tags(self, tags: set):
        self._tags.update(tags)

    def add_rules(self, rules: dict):
        if type(rules) != list:
            rules = [rules]
        self._rules += rules

    def add_namespace(self, namespace: str):
        if namespace is None:
            return
        if self._namespace is None:
            self._namespace = namespace
        else:
            self._namespace += "_" + namespace

    def set_image(self, image: str):
        self._image = image

    def copy(self):
        job_copy = Job(
            name=self._name,
            script=copy.deepcopy(self._script),
        )
        job_copy.set_image(self._image)
        job_copy.add_variables(**copy.deepcopy(self._variables))
        job_copy.add_namespace(self._namespace)
        job_copy.add_tags(self._tags)
        job_copy.add_rules(self._rules)
        return job_copy

    def render(self):
        rendered_job = {
            "script": self._script,
            "variables": self._variables,
            "tags": list(self._tags),
        }

        if len(self._rules) > 0:
            rendered_rules = []
            for rule in self._rules:
                rendered_rules.append(rule.render())
            rendered_job = {
                **{
                    "rules": rendered_rules
                },
                **rendered_job
            }

        if self._image is not None:
            rendered_job = {
                **{
                    "image": self._image
                },
                **rendered_job
            }
        return rendered_job


class JobSequence():
    def __init__(self, namespace: str = None):
        self._jobs = []
        self._name = None
        self._namespace = namespace
        self._image = None
        self._variables = {}
        self._tags = set()
        self._prepend_scripts = []
        self._append_scripts = []
        self._rules = []

    def add_job(self, job: Job, *args, namespace: str = None):
        job.add_namespace(namespace)
        self._jobs.append(job)

    def add_to_name(self, name: str):
        if name is None:
            return
        if self._name is None:
            self._name = name
        else:
            self._name += "_" + name

    def add_variables(self, **variables: Dict[str, str]):
        self._variables.update(variables)

    def add_tags(self, tags: set):
        if type(tags) == str:
            tags = [tags]
        self._tags.update(tags)

    def add_rules(self, rules: dict):
        if type(rules) != list:
            rules = [rules]
        self._rules += rules

    def add_sequence(self, job_sequence, *args, namespace: str = None, name: str = None):
        job_sequence.add_namespace(namespace)
        job_sequence.add_to_name(name)
        self._jobs.append(job_sequence)

    def prepend_script(self, script: str):
        if type(script) == str:
            script = [script]
        self._prepend_scripts = script + self._prepend_scripts

    def append_script(self, script: str):
        if type(script) == str:
            script = [script]
        self._append_scripts += script

    def set_image(self, image: str):
        self._image = image

    def add_namespace(self, namespace: str):
        if namespace is None:
            return
        if self._namespace is None:
            self._namespace = namespace
        else:
            self._namespace += namespace

    @property
    def populated_jobs(self) -> list:
        all_jobs = []
        for job in self._jobs:
            if type(job) == JobSequence:
                all_jobs += job.populated_jobs
            elif type(job) == Job:
                all_jobs.append(job.copy())

        for job in all_jobs:
            job.add_namespace(self._namespace)
            job.add_to_name(self._name)
            job.set_image(self._image)
            job.add_variables(**copy.deepcopy(self._variables))
            job.add_tags(self._tags)
            job.add_rules(self._rules)
            job.prepend_script(self._prepend_scripts)
            job.append_script(self._append_scripts)

        return all_jobs


class Pipeline(JobSequence):
    def __init__(
        self,
        *args,
        namespace: str = None,
    ):
        super().__init__(namespace)
        self._pipeline = {}

    def render(self):
        stages = {}
        job_copies = self.populated_jobs
        for job in job_copies:
            # use the keys of dictionary as ordered set
            stages[job.stage] = None
        pipe_copy = copy.deepcopy(self._pipeline)
        pipe_copy["stages"] = list(stages.keys())
        for job in job_copies:
            rendered_job = job.render()
            rendered_job["stage"] = job.stage
            pipe_copy[job.name] = rendered_job
        return pipe_copy

    def print_yaml(self):
        print(yaml.dump(self.render(), default_flow_style=False, sort_keys=False))
