from enum import Enum
from typing import Any, Dict, Mapping, Optional

from .core import Core


class IncludeMethod(Enum):
    """Class with static values for ``include_methods`` used together with :class:`gcip.Include` class. To construct an object."""
    LOCAL = "local"
    FILE = "project"
    TEMPLATE = "template"
    REMOTE = "remote"


class Include(object):
    def __init__(
        self,
        *args: Any,
        file: str,
        include_method: IncludeMethod,
        project: Optional[str] = None,
        ref: Optional[str] = None,
        **kwargs: Mapping[Any, Any],
    ) -> None:
        """
        :class:`Include` class to create Gitlab includes.

        You can create different types of :class:`Includes` see :class:`IncludeMethods` for types.
        If :class:`IncludeMethod` is one of LOCAL, TEMPLATE OR REMOTE, you can only use ``file`` as parameter,
        ``project`` and ``ref`` are not allowed.

        Args:
            file (str): Absolute or relative path to file to include.
            include_method (IncludeMethod): IncludeMethod used to determine which include to produce.
            project (Optional[str]): Remote project only available if :class:`IncludeMethod`.FILE. Defaults to None.
            ref (Optional[str]): Branch of remote ``project`` to include ``file`` from. Defaults to None.

        Raises:
            TypeError: If ``file`` is not of type :class:`str`.
            TypeError: If ``include_method`` is not of type :class:`IncludeMethod`
            ValueError: If ``project`` is given but ``include_method`` is not :class:`IncludeMethod.FILE`
            AttributeError: If :class:`IncludeMethod.FILE` but ``project`` is missing.
            ValueError: If :class:`IncludeMethod.REMOTE` and ``file`` is not a valid URL.
        """
        self._file = file
        self._include_method = include_method
        self._project = project
        self._ref = ref

        if not isinstance(self._file, str):
            raise TypeError("'file' must be of type str.")

        if not isinstance(self._include_method, IncludeMethod):
            raise TypeError("'include_method' must be of type IncludeMethod")

        if self._include_method in (IncludeMethod.LOCAL, IncludeMethod.TEMPLATE, IncludeMethod.REMOTE):
            if self._project or self._ref:
                raise ValueError(f"Parameter project nor ref are not allowed for include_method: {self._include_method}")
        elif self._include_method == IncludeMethod.FILE:
            if not self._project:
                raise AttributeError("Missing parameter 'project'.")

        if self._include_method == IncludeMethod.REMOTE:
            if not Core.validate_url(file):
                raise ValueError(f"URL is not valid. URL: {file}")

    def render(self) -> Dict[Any, Optional[str]]:
        rendered_include = {}
        if self._include_method is IncludeMethod.FILE:
            rendered_include.update({self._include_method.value: self._project})
            rendered_include.update({"file": self._file})
            if self._ref:
                rendered_include.update({"ref": self._ref})
        else:
            rendered_include.update({self._include_method.value: self._file})
        return rendered_include
