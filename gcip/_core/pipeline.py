from typing import Any, Dict, List, Union, Optional

from . import OrderedSetType
from .include import _Include
from .job_sequence import JobSequence

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


class Pipeline(JobSequence):
    def __init__(self, *, includes: Optional[Union[_Include, List[_Include]]] = None):
        """
        Pipeline class creates an empty Gitlab pipeline.

        Args:
            includes (Optional[Union[_Include, List[_Include]]]): You can add global Gitlab includes.
                See `Gitlab CI Reference include`_. Defaults to None.

        Raises:
            ValueError: If ``includes`` is not of type :class:`list` or :class:`list` of :class:`_Includes`

        .. _Gitlab CI Reference include:
           https://docs.gitlab.com/ee/ci/yaml/#include
        """
        if not includes:
            self._includes = []
        elif isinstance(includes, _Include):
            self._includes = [includes]
        elif isinstance(includes, list):
            self._includes = includes
        else:
            raise ValueError("Parameter include must of type gcip._Include or List[gcip._Include]")
        super().__init__()

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
            pipline[job.name] = job.render()
        return pipline

    def add_include(self, include: _Include) -> None:
        self._includes.append(include)

    def print_yaml(self) -> None:
        import yaml
        print(yaml.dump(self.render(), default_flow_style=False, sort_keys=False))
