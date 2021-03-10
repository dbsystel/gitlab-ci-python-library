from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Union, Optional


class WhenStatement(Enum):
    ALWAYS = "always"
    DELAYED = "delayed"
    MANUAL = "manual"
    NEVER = "never"
    ON_FAILURE = "on_failure"
    ON_SUCCESS = "on_success"


class Rule():
    def __init__(
        self,
        *args: Any,
        if_statement: Optional[str] = None,
        when: WhenStatement = WhenStatement.ON_SUCCESS,
        allow_failure: bool = False,
    ) -> None:
        self._if = if_statement
        self._when = when
        self._allow_failure = allow_failure

    def never(self) -> Rule:
        self._when = WhenStatement.NEVER
        return self

    def render(self) -> Dict[str, Union[str, bool]]:
        rendered_rule: Dict[str, Union[str, bool]] = {}
        if self._if:
            rendered_rule.update({"if": self._if})

        rendered_rule.update({
            "when": self._when.value,
            "allow_failure": self._allow_failure,
        })
        return rendered_rule
