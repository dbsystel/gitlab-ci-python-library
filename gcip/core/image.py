"""This module represents the Gitlab CI [Image](https://docs.gitlab.com/ee/ci/yaml/#image) keyword.

Use `Image` to specify a Docker image to use for the `gcip.core.job.Job`.

```
job1.set_image(Image("python"))
job2.set_image(Image("gcr.io/kaniko-project/executor:debug", entrypoint=[""]))
```
"""
from typing import Dict, List, Union, Optional


class Image:
    def __init__(self, name: str, *, entrypoint: Optional[List[str]] = None) -> None:
        """This module represents the Gitlab CI [Image](https://docs.gitlab.com/ee/ci/yaml/#image) keyword.

        Use `Image` to specify a Docker image to use for the `gcip.core.job.Job`.

        Args:
            name (str): The fully qualified image name. Could include repository and tag as usual.
            entrypoint (Optional[List[str]]): Overwrites the containers entrypoint. Defaults to None.
        """
        self._name = name
        self._entrypoint = entrypoint

    @property
    def name(self) -> str:
        """Equals the identical Class argument."""
        return self._name

    @property
    def entrypoint(self) -> Optional[List[str]]:
        """Equals the identical Class argument."""
        return self._entrypoint

    def render(self) -> Dict[str, Union[str, List[str]]]:
        """Return a representation of this Image object as dictionary with static values.

        The rendered representation is used by the gcip to dump it
        in YAML format as part of the .gitlab-ci.yml pipeline.

        Returns:
            Dict[str, Union[str, List[str]]]: A dictionary prepresenting the image object in Gitlab CI.
        """
        rendered: Dict[str, Union[str, List[str]]] = {}
        rendered["name"] = self._name

        if self._entrypoint:
            rendered["entrypoint"] = self._entrypoint

        return rendered
