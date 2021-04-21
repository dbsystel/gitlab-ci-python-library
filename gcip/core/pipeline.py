"""The Pipeline is the root container for all `gcip.core.job.Job`s and `gcip.core.sequence.Sequence`s
"""
from __future__ import annotations

from typing import Any, Dict, List, Union, Optional

from . import OrderedSetType
from .job import Job
from .include import Include
from .service import Service
from .sequence import Sequence

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


class JobNameConflictError(Exception):
    """This exception is used by the `Pipeline` when two rendered jobs have the same name.

    When two or more jobs have the same name within a pipeline means that one job will overwrite
    all those other jobs. This is absolutely nonsense and could (nearly?) never be the intention of
    the user, so he must be informed about that exception.

    Attributes:
        job (Job): A `gcip.core.job.Job` whose name equals to another job already added to the rendered pipeline.
    """

    def __init__(self, job: Job):
        super().__init__(
            f"Two jobs have the same name '{job.name}' when rendering the pipeline."
            "\nPlease fix this by providing a different name and/or stage when adding those jobs to"
            " their sequences/pipeline."
        )


class Pipeline(Sequence):
    def __init__(self, *, includes: Optional[Union[Include, List[Include]]] = None):
        """A Pipeline is the uppermost container of `gcip.core.job.Job`s and `gcip.core.sequence.Sequence`s.

        A Pipeline is a `gcip.core.sequence.Sequence` itself but has the additional method `Pipeline.write_yaml()`.
        This method is responsible for writing the whole Gitlab CI pipeline to a YAML file which could then feed
        the dynamic child pipeline.

        Args:
            includes (Optional[Union[Include, List[Include]]]): You can add global `gcip.core.include.Include`s to the pipeline.
                [Gitlab CI Documentation](https://docs.gitlab.com/ee/ci/yaml/#include): _"Use include to include external YAML files
                in your CI/CD configuration."_ Defaults to None.

        Raises:
            ValueError: If `includes` is not of type `Include` or `list` of `Includes`
        """
        self._services: List[Service] = list()

        if not includes:
            self._includes = []
        elif isinstance(includes, Include):
            self._includes = [includes]
        elif isinstance(includes, list):
            self._includes = includes
        else:
            raise ValueError("Parameter include must of type gcip.Include or List[gcip.Include]")
        super().__init__()

    def add_services(self, *services: Union[str, Service]) -> Pipeline:
        """Add one or more `gcip.core.service.Service`s to the pipeline.

        Gitlab CI Documentation: _"The services keyword defines a Docker image that runs during a job linked to the Docker image
        that the image keyword defines."_

        Args:
            services (Union[str, Service]): Simply use strings to name the services to link to the pipeline.
                Use objects of the `gcip.core.service.Service` class for more complex service configurations.

        Returns:
            `Pipeline`: The modified `Pipeline` object.
        """
        for service in services:
            if isinstance(service, str):
                service = Service(service)
            self._services.append(service)
        return self

    def add_include(self, include: Include) -> Pipeline:
        """Let you add global `gcip.core.include.Include`s to the pipeline.
        [Gitlab CI Documentation](https://docs.gitlab.com/ee/ci/yaml/#include): _"Use include to include external YAML files
        in your CI/CD configuration."_

        Returns:
            `Pipeline`: The modified `Pipeline` object.
        """
        self._includes.append(include)
        return self

    def render(self) -> Dict[str, Any]:
        """Return a representation of this Pipeline object as dictionary with static values.

        The rendered representation is used by the gcip to dump it
        in YAML format as part of the .gitlab-ci.yml pipeline.

        Return:
            Dict[str, Any]: A dictionary prepresenting the pipeline object in Gitlab CI.
        """
        stages: OrderedSetType = {}
        pipeline: Dict[str, Any] = {}
        job_copies = self.populated_jobs

        for job in job_copies:
            # use the keys of dictionary as ordered set
            stages[job.stage] = None

        if self._includes:
            pipeline["include"] = [include.render() for include in self._includes]

        if self._services:
            pipeline["services"] = [service.render() for service in self._services]

        pipeline["stages"] = list(stages.keys())
        for job in job_copies:
            if job.name in pipeline:
                raise JobNameConflictError(job)

            pipeline[job.name] = job.render()
        return pipeline

    def write_yaml(self, filename: str = "generated-config.yml") -> None:
        """
        Create the Gitlab CI YAML file from this pipeline object.

        Use that YAML file to trigger a child pipeline.

        Args:
            filename (str, optional): The file name of the created yaml file. Defaults to "generated-config.yml".
        """
        import yaml

        with open(filename, "w") as generated_config:
            generated_config.write(yaml.dump(self.render(), default_flow_style=False, sort_keys=False))
