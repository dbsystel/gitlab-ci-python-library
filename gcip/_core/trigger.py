from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Mapping, Optional

from .include import Include


class TriggerStrategy(Enum):
    """Class with static values for ``TriggerStrategy`` used together with :class:`gcip.Trigger`. To construct an object."""
    DEPEND = "depend"


class Trigger(object):
    def __init__(
        self,
        *args: Any,
        project: Optional[str] = None,
        branch: Optional[str] = None,
        includes: Optional[List[Include]] = None,
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

        self._project = project
        self._branch = branch
        self._includes = includes or []
        self._strategy = strategy

        if len(self._includes) > 3:
            raise ValueError(
                (
                    "The length of 'includes' is limited to three."
                    "See https://docs.gitlab.com/ee/ci/parent_child_pipelines.html for more information."
                )
            )

    def render(self) -> Dict[Any, Any]:
        rendered_trigger = {}
        # Child pipelines
        if len(self._includes):
            rendered_trigger.update({
                "include": [include.render() for include in self._includes],
            })
        # Multiproject pipelines
        if self._project:
            rendered_trigger.update({
                "project": self._project,
            })
            if self._branch:
                rendered_trigger.update({"branch": self._branch})

        if self._strategy:
            rendered_trigger.update({"strategy": self._strategy.value})
        return rendered_trigger
