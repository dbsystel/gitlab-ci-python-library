from __future__ import annotations

import copy
from typing import Any, Dict, List, Union, AnyStr, Optional

from . import OrderedSetType
from .rule import Rule


class Job():
    def __init__(
        self,
        *args: Any,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        script: Union[AnyStr, List[str]],
    ):
        self._stage = ""
        self._name = ""
        self._image: Optional[str] = None
        self._variables: Dict[str, str] = {}
        self._tags: OrderedSetType = {}
        self._rules: List[Rule] = []
        self._scripts: List[str]
        self._artifacts_paths: OrderedSetType = {}

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

    def prepend_scripts(self, *scripts: str) -> None:
        self._scripts = list(scripts) + self._scripts

    def append_scripts(self, *scripts: str) -> None:
        self._scripts.extend(scripts)

    def add_variables(self, **variables: str) -> None:
        self._variables.update(variables)

    def add_tags(self, *tags: str) -> None:
        for tag in tags:
            self._tags[tag] = None

    def add_artifacts_paths(self, *paths: str) -> None:
        for path in paths:
            self._artifacts_paths[path] = None

    def append_rules(self, *rules: Rule) -> None:
        self._rules.extend(rules)

    def prepend_rules(self, *rules: Rule) -> None:
        self._rules = list(rules) + self._rules

    def set_image(self, image: Optional[str]) -> None:
        if image:
            self._image = image

    def copy(self) -> Job:
        job_copy = Job(
            name=".",
            script=copy.deepcopy(self._scripts),
        )
        job_copy._name = self._name
        job_copy._stage = self._stage

        job_copy.set_image(self._image)
        job_copy.add_variables(**copy.deepcopy(self._variables))
        job_copy.add_tags(*list(self._tags.keys()))
        job_copy.add_artifacts_paths(*list(self._artifacts_paths.keys()))
        job_copy.append_rules(*self._rules)
        return job_copy

    def render(self) -> Dict[str, Any]:
        rendered_job: Dict[str, Any] = {
            "script": self._scripts,
        }

        if self._variables:
            rendered_job["variables"] = self._variables

        if self._tags.keys():
            rendered_job["tags"] = list(self._tags.keys())

        if self._rules:
            rendered_rules = []
            for rule in self._rules:
                rendered_rules.append(rule.render())
            rendered_job.update({"rules": rendered_rules})

        if self._artifacts_paths.keys():
            rendered_job.update({"artifacts": {
                "paths": list(self._artifacts_paths.keys()),
            }})

        if self._image:
            rendered_job.update({"image": self._image})

        return rendered_job
