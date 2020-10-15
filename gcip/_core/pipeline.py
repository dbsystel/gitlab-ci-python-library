from typing import Any, Dict

from . import OrderedSetType
from .job_sequence import JobSequence


class Pipeline(JobSequence):
    def render(self) -> Dict[str, Any]:
        stages: OrderedSetType = {}
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
        import yaml
        print(yaml.dump(self.render(), default_flow_style=False, sort_keys=False))
