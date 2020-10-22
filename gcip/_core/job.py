from __future__ import annotations

import copy
from enum import Enum
from typing import Any, Dict, List, Union, AnyStr, Optional, Mapping

from . import OrderedSetType
from .rule import Rule
from .include import Include


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
        self._needs: List[Need] = []
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

    def add_needs(self, *needs: Need) -> None:
        self._needs.extend(needs)

    def set_image(self, image: Optional[str]) -> None:
        if image:
            self._image = image

    def copy(self) -> Job:
        return self._copy_into(Job(name=".", script=copy.deepcopy(self._scripts)))

    def _copy_into(self, job: Job) -> Job:
        job._name = self._name
        job._stage = self._stage

        job.set_image(self._image)
        job.add_variables(**copy.deepcopy(self._variables))
        job.add_tags(*list(self._tags.keys()))
        job.add_artifacts_paths(*list(self._artifacts_paths.keys()))
        job.append_rules(*self._rules)
        job.add_needs(*self._needs)

        return job

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

        if self._needs:
            rendered_needs = []
            for need in self._needs:
                rendered_needs.append(need.render())
            rendered_job.update({"needs": rendered_needs})

        if self._artifacts_paths.keys():
            rendered_job.update({"artifacts": {
                "paths": list(self._artifacts_paths.keys()),
            }})

        if self._image:
            rendered_job.update({"image": self._image})

        rendered_job["stage"] = self._stage

        return rendered_job


class TriggerStrategy(Enum):
    """Class with static values for ``TriggerStrategy`` used together with :class:`gcip.Trigger`. To construct an object."""
    DEPEND = "depend"


class TriggerJob(Job):
    def __init__(
        self,
        *args: Any,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        project: Optional[str] = None,
        branch: Optional[str] = None,
        includes: Optional[Include, List[Include]] = None,
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
        self._includes = includes or []
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

        trigger = {}

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
