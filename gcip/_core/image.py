from typing import Dict, List, Union, Optional


class Image():
    def __init__(self, name: str, *, entrypoint: Optional[List[str]] = None) -> None:
        """Creates an object which represents an `image` for a job inside a pipeline.

        Args:
            name (str): URL where to pull image from incl. image tag.
            entrypoint (Optional[List[str]]): If set, overwrites the containers entrypoint. Defaults to None.
        """
        self._name = name
        self._entrypoint = entrypoint

    @property
    def name(self) -> str:
        """Image name"""
        return self._name

    @property
    def entrypoint(self) -> Optional[List[str]]:
        """Container `entrypoint`"""
        return self._entrypoint

    def render(self) -> Dict[str, Union[str, List[str]]]:
        """Returns the rendered object to be attached to the job.

        Returns:
            Dict[str, str]: The dictionary representation of the image
        """
        rendered: Dict[str, Union[str, List[str]]] = {}
        rendered["name"] = self._name

        if self._entrypoint:
            rendered["entrypoint"] = self._entrypoint

        return rendered
