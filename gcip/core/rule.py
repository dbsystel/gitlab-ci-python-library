"""This module represents the Gitlab CI [rules](https://docs.gitlab.com/ee/ci/yaml/#rules) keyword.

Use rules to include or exclude jobs in pipelines.

```
my_job.prepend_rules(
    Rule(
        if_statement='$CI_COMMIT_BRANCH == "master"',
        when=WhenStatement.ON_FAILURE,
        allow_failure: True,
        )
    )
```
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Union, Optional

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


class WhenStatement(Enum):
    """This enum holds different [when](https://docs.gitlab.com/ee/ci/yaml/#when) statements for `Rule`s."""

    ALWAYS = "always"
    DELAYED = "delayed"
    MANUAL = "manual"
    NEVER = "never"
    ON_FAILURE = "on_failure"
    ON_SUCCESS = "on_success"


class Rule:
    """This module represents the Gitlab CI [rules](https://docs.gitlab.com/ee/ci/yaml/#rules) keyword.

    Use `rules` to include or exclude jobs in pipelines.

    Args:
        if_statement (Optional[str], optional): The [rules:if clause](https://docs.gitlab.com/ee/ci/yaml/#when) which decides when
            a job to the pipeline. Defaults to None.
        when (WhenStatement, optional): The [when](https://docs.gitlab.com/ee/ci/yaml/#when) attribute which decides when to run a job.
            Defaults to WhenStatement.ON_SUCCESS.
        allow_failure (bool, optional): The [allow_failure](https://docs.gitlab.com/ee/ci/yaml/#allow_failure) attribute which let a
            job fail without impacting the rest of the CI suite. Defaults to False.
    """

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
        """
        This method returns a copy of this rule with the `when` attribute set to `WhenStatement.NEVER`.

        This method is intended to be used for predefined rules. For instance you have defined an
        often used rule `on_master` whose if statement checks if the pipeline is executed on branch
        `master`. Then you can either run a job, if on master...

        ```
        my_job.append_rules(on_master)
        ```

        ... or do not run a job if on master...

        ```
        my_job.append_rules(on_master.never())
        ```

        Returns:
            Rule: A new rule object with `when` set to `WhenStatement.NEVER`.
        """
        self._when = WhenStatement.NEVER
        return self

    def copy(self) -> Rule:
        """
        Returns an identical copy of that rule.

        Returns:
            Rule: A new rule object with identical configuration.
        """
        return Rule(self._if, self._when, self._allow_failure)

    def render(self) -> Dict[str, Union[str, bool]]:
        """Return a representation of this Rule object as dictionary with static values.

        The rendered representation is used by the gcip to dump it
        in YAML format as part of the .gitlab-ci.yml pipeline.

        Returns:
            Dict[str, Any]: A dictionary representing the rule object in Gitlab CI.
        """
        rendered_rule: Dict[str, Union[str, bool]] = {}
        if self._if:
            rendered_rule.update({"if": self._if})

        rendered_rule.update(
            {
                "when": self._when.value,
                "allow_failure": self._allow_failure,
            }
        )
        return rendered_rule
