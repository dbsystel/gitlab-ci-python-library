from typing import Any, Dict, List, Union, Optional

from . import OrderedSetType
from .include import Include
from .job_sequence import JobSequence


class Pipeline(JobSequence):
    def __init__(
        self,
        *args,
        includes: Optional[Union[Include, List[Include]]] = None,
        **kwargs,
    ):
        """
        Pipeline class creates an empty Gitlab pipeline.

        Args:
            includes (Optional[Union[Include, List[Include]]]): You can add global Gitlab includes.
                See `Gitlab CI Reference include`_. Defaults to None.

        Raises:
            ValueError: If ``includes`` is not of type :class:`list` or :class:`list` of :class:`Includes`

        .. _Gitlab CI Reference include:
           https://docs.gitlab.com/ee/ci/yaml/#include
        """
        if not includes:
            self._includes = []
        elif isinstance(includes, Include):
            self._includes = [includes]
        elif isinstance(includes, list):
            self._includes = includes
        else:
            raise ValueError("Parameter include must of type gcip.Include or List[gcip.Include]")
        super().__init__(
            *args,
            **kwargs,
        )

    def render(self) -> Dict[str, Any]:
        stages: OrderedSetType = {}
        pipline: Dict[str, Any] = {}
        job_copies = self.populated_jobs

        for job in job_copies:
            # use the keys of dictionary as ordered set
            stages[job.stage] = None

        if self._includes:
            pipline["include"] = [include.render() for include in self._includes]

        pipline["stages"] = list(stages.keys())
        for job in job_copies:
            rendered_job = job.render()
            rendered_job["stage"] = job.stage
            pipline[job.name] = rendered_job
        return pipline

    def add_include(self, include: Include):
        self._includes.append(include)

    def print_yaml(self) -> None:
        import yaml
        print(yaml.dump(self.render(), default_flow_style=False, sort_keys=False))
