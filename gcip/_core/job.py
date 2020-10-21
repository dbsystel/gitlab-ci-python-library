from __future__ import annotations

import copy
from typing import Any, Dict, List, Union, AnyStr, Optional

from . import OrderedSetType
from .rule import Rule


class _JobCommons():
    def __init__(
        self,
        *args: Any,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        self._stage = ""
        self._name = ""
        self._rules: List[Rule] = []
        self._needs: List[Need] = []

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

    def append_rules(self, *rules: Rule) -> None:
        self._rules.extend(rules)

    def prepend_rules(self, *rules: Rule) -> None:
        self._rules = list(rules) + self._rules

    def add_needs(self, *needs: Need) -> None:
        self._needs.extend(needs)

    def copy(self, job_copy: Job) -> Job:
        job_copy._name = self._name
        job_copy._stage = self._stage
        job_copy.append_rules(*self._rules)
        job_copy.add_needs(*self._needs)
        return job_copy

    def render(self) -> Dict[str, Any]:
        rendered_job: Dict[str, Any] = {}

        if self._needs:
            rendered_needs = []
            for need in self._needs:
                rendered_needs.append(need.render())
            rendered_job.update({"needs": rendered_needs})

        if self._rules:
            rendered_rules = []
            for rule in self._rules:
                rendered_rules.append(rule.render())
            rendered_job.update({"rules": rendered_rules})

        return rendered_job


class Job(_JobCommons):
    def __init__(
        self,
        *args: Any,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        script: Union[AnyStr, List[str]],
    ):
        super().__init__(name=name, namespace=namespace)

        self._image: Optional[str] = None
        self._variables: Dict[str, str] = {}
        self._tags: OrderedSetType = {}
        self._scripts: List[str]
        self._artifacts_paths: OrderedSetType = {}

        if isinstance(script, str):
            self._scripts = [script]
        elif isinstance(script, list):
            self._scripts = script
        else:
            raise AttributeError("script parameter must be of type string or list of strings")

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

    def set_image(self, image: Optional[str]) -> None:
        if image:
            self._image = image

    def copy(self) -> Job:
        job_copy = Job(
            name=".",
            script=copy.deepcopy(self._scripts),
        )
        super().copy(job_copy)
        job_copy.set_image(self._image)
        job_copy.add_variables(**copy.deepcopy(self._variables))
        job_copy.add_tags(*list(self._tags.keys()))
        job_copy.add_artifacts_paths(*list(self._artifacts_paths.keys()))
        return job_copy

    def render(self) -> Dict[str, Any]:
        rendered_job = super().render()

        rendered_job = {
            "script": self._scripts,
            **rendered_job
        }

        if self._image:
            rendered_job = {
                "image": self._image,
                **rendered_job
            }

        if self._variables:
            rendered_job["variables"] = self._variables

        if self._artifacts_paths.keys():
            rendered_job.update({"artifacts": {
                "paths": list(self._artifacts_paths.keys()),
            }})

        if self._tags.keys():
            rendered_job["tags"] = list(self._tags.keys())

        return rendered_job


# This class is implemented within the job module to solve circular
# import dependencies between Job and Need
class Need(object):
    def __init__(
        self,
        job: Union[str, Job],
        project: Optional[str] = None,
        ref: Optional[str] = None,
        artifacts: bool = True,
    ):
        """
        Class to add `needs` to :class:`Job`

        The `needs` key-word adds a possibility to allow out-of-order Gitlab CI jobs.
        A job which needed another job runs directly after `another job` as finished successfully.
        For more in depth information see `Gitlab CI Reference needs`_, `Directed Acyclic Graph`_.

        Args:
            job (Union[str, Job]): Either a :class:`Job` or a job's name in as :class:`str`.
            project (Optional[str]): Remote Gitlab Project to add the `dependency` from. Defaults to None.
            ref (Optional[str]): Branch of the remote project to depend on. Defaults to None.
            artifacts (bool): Download artifacts generated by ``job``. Defaults to True.

        Raises:
            ValueError: If ``ref`` is set but ``project`` is missing.

        .. _Gitlab CI Reference needs:
           https://docs.gitlab.com/ee/ci/yaml/#needs
        .. _Directed Acyclic Graph:
           https://docs.gitlab.com/ee/ci/directed_acyclic_graph/index.html
        """
        if ref and not project:
            raise ValueError("'ref' parameter requires the 'project' parameter.")

        self._project = project
        self._ref = ref
        self._artifacts = artifacts

        if isinstance(job, Job):
            self._job = job.name
        elif isinstance(job, str):
            self._job = job
        else:
            raise ValueError(f"The 'job' parameter is of unsupported type {type(job)}")

        if self._project and not self._ref:
            self._ref = "master"

    def render(self) -> Dict[str, object]:
        """
        Renders the :class:`Need` object. Returns the :obj:`dict` representation of the object
        """
        rendered_need = {
            "job": self._job,
            "artifacts": self._artifacts
        }
        if self._project:
            rendered_need.update({
                "project": self._project,
                "ref": self._ref
            })
        return rendered_need
