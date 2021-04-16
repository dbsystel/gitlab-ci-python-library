"""This module represents the Gitlab CI [Include](https://docs.gitlab.com/ee/ci/yaml/#include) keyword.

Use include to include external YAML files in your CI/CD configuration.

----

[include:local](https://docs.gitlab.com/ee/ci/yaml/#includelocal) example:

```
pipeline.add_include(IncludeLocal("/templates/.gitlab-ci-template.yml"))
```

----

[include:file](https://docs.gitlab.com/ee/ci/yaml/#includefile) example:

```
pipeline.add_include(IncludeFile(
        project="my-group/my-project",
        ref="master",
        file="/templates/.gitlab-ci-template.yml"
    ))
```

----

[include:remote](https://docs.gitlab.com/ee/ci/yaml/#includeremote) example:

```
pipeline.add_include(IncludeRemote("https://gitlab.com/example-project/-/raw/master/.gitlab-ci.yml"))
```

----

[include:template](https://docs.gitlab.com/ee/ci/yaml/#includetemplate) example:

```
pipeline.add_include(IncludeTemplate("Auto-DevOps.gitlab-ci.yml"))
```

----

Special type of include: Use a `gcip.core.job.TriggerJob` with `IncludeArtifact` to run [a child pipeline with a generated
configuration file from a previous job](https://docs.gitlab.com/ee/ci/yaml/README.html#trigger-child-pipeline-with-generated-configuration-file):

```
TriggerJob(includes=IncludeArtifact(job="generate-config", artifact="generated-config.yml"))
```

Note: The `IncludeArtifact` isn't implemented very well as it currently cannot handle `gcip.core.job.Job` objects. You need to know the jobs final name,
which is not very handy. This could be implemented much better in future.
"""
from abc import ABCMeta
from typing import Dict, Optional

from ..tools.url import is_valid_url

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


class Include(metaclass=ABCMeta):
    """
    This is just an abstract superclass.

    Please use one of the subclasses:

    * `IncludeLocal`
    * `IncludeFile`
    * `IncludeRemote`
    * `IncludeTemplate`
    * `IncludeArtifact`
    """

    _rendered_include: Dict[str, str]

    def render(self) -> Dict[str, str]:
        """Returns a representation of this Include object as dictionary with static values.

        The rendered representation is used by the gcip to dump it
        in YAML format as part of the .gitlab-ci.yml pipeline.

        Returns:
            Dict[str, str]: A dictionary representing the include object in Gitlab CI.
        """
        return self._rendered_include


class IncludeLocal(Include):
    """This module represents the Gitlab CI [include:local](https://docs.gitlab.com/ee/ci/yaml/#includelocal) keyword.

    Args:
        local (str): Relative path to the file within this repository to include.
    """

    def __init__(self, local: str) -> None:
        self._rendered_include = {"local": local}


class IncludeFile(Include):
    """This module represents the Gitlab CI [include:file](https://docs.gitlab.com/ee/ci/yaml/#includefile) keyword.

    Args:
        file (str): Relative path to the file to include.
        project (str): Project to include the file from.
        ref (Optional[str], optional): Project branch to include the file from. Defaults to None.
    """

    def __init__(
        self,
        file: str,
        project: str,
        ref: Optional[str] = None,
    ) -> None:
        self._rendered_include = {"file": file, "project": project}
        if ref:
            self._rendered_include["ref"] = ref


class IncludeRemote(Include):
    """This module represents the Gitlab CI [include:remote](https://docs.gitlab.com/ee/ci/yaml/#includeremote) keyword.

    Args:
        remote (str): URL to include the file from.

    Raises:
        ValueError: If `remote` is not a valid URL.
    """

    def __init__(self, remote: str) -> None:
        if not is_valid_url(remote):
            raise ValueError(f"`remote` is not a valid URL: {remote}")

        self._rendered_include = {"remote": remote}


class IncludeTemplate(Include):
    """This class represents the Gitlab CI [include:template](https://docs.gitlab.com/ee/ci/yaml/#includetemplate) keyword.

    Args:
        template (str): Gitlab template pipeline to include.
    """

    def __init__(self, template: str) -> None:
        self._rendered_include = {"template": template}


class IncludeArtifact(Include):
    """A special type of include: Use a `gcip.core.job.TriggerJob` with `IncludeArtifact` to run [a child pipeline with a generated configuration
    file from a previous job](https://docs.gitlab.com/ee/ci/yaml/README.html#trigger-child-pipeline-with-generated-configuration-file):

    Args:
        job (str): Job name to include the artifact from.
        artifact (str): Relative path to the artifact which is produced by `job`.
    """

    def __init__(self, job: str, artifact: str) -> None:
        self._rendered_include = {"job": job, "artifact": artifact}
