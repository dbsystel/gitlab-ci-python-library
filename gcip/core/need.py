"""This module represents the Gitlab CI [needs](https://docs.gitlab.com/ee/ci/yaml/#needs) keyword.

Needs are to create relationships between `gcip.core.job.Job`s and `gcip.core.sequence.Sequence`s, which will
then be executed as early as all preceding required jobs finished. This relationship ignores the common ordering by stages.

The `Need` class is mostly for internal use, as you can link `gcip.core.job.Job`s as well as `gcip.core.sequence.Sequence`s
directly together:

```
my_job = Job(stage="example", script="do-something.sh")
my_sequence = Sequence()
...
my_next_job = Job(stage="example", script="do-anything.sh")
my_next_job.add_needs(my_job, my_sequence)

my_next_sequence = Sequence()
my_next_sequence.add_needs(my_job, my_sequence)
```

In this example `my_next_job` and `my_next_sequence` start as soon as

* `my_job` has finished
* all jobs within the last stage of `my_sequence` have finished

That also mean that stages are ignored, as the `example` stage for example.

However you can use the `Need` class directly when depending on other pipelines jobs or you don't want to [download
artifacts](https://docs.gitlab.com/ee/ci/yaml/#artifact-downloads-with-needs) from preceding jobs:

```
my_job.add_needs(
    Need("awesome-job", project="master-pipeline"),
    Need(my_job, artifacts=False),
    )
```
"""
from __future__ import annotations

from typing import Dict, Union, Optional


class Need(object):
    def __init__(
        self,
        job: str,
        *,
        project: Optional[str] = None,
        ref: Optional[str] = None,
        artifacts: bool = True,
    ):
        """This class represents the Gitlab CI [needs](https://docs.gitlab.com/ee/ci/yaml/#needs) keyword.

        The `needs` key-word adds a possibility to allow out-of-order Gitlab CI jobs.
        A job which needed another job runs directly after the other job as finished successfully.

        Args:
            job (str): The name of the job to depend on.
            project (Optional[str]): If the `job` resides in another pipeline you have to give its project name here. Defaults to None.
            ref (Optional[str]): Branch of the remote project to depend on. Defaults to None.
            artifacts (bool): Download artifacts from the `job` to depend on. Defaults to True.

        Raises:
            ValueError: If `ref` is set but `project` is missing.
        """
        if ref and not project:
            raise ValueError("'ref' parameter requires the 'project' parameter.")

        self._job = job
        self._project = project
        self._ref = ref
        self._artifacts = artifacts

        if self._project and not self._ref:
            self._ref = "main"

    def render(self) -> Dict[str, Union[str, bool]]:
        """Return a representation of this Need object as dictionary with static values.

        The rendered representation is used by the gcip to dump it
        in YAML format as part of the .gitlab-ci.yml pipeline.

        Returns:
            Dict[str, Any]: A dictionary representing the need object in Gitlab CI.
        """
        rendered_need: Dict[str, Union[str, bool]] = {
            "job": self._job,
            "artifacts": self._artifacts,
        }
        if self._project and self._ref:
            rendered_need.update({"project": self._project, "ref": self._ref})
        return rendered_need
