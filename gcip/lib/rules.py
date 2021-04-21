from gcip.core.rule import Rule

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


def on_branch(branch_name: str) -> Rule:
    return Rule(if_statement=f'$CI_COMMIT_BRANCH == "{branch_name}"')


def not_on_branch(branch_name: str) -> Rule:
    return Rule(if_statement=f'$CI_COMMIT_BRANCH != "{branch_name}"')


def on_main() -> Rule:
    return on_branch("main")


def not_on_main() -> Rule:
    return not_on_branch("main")


def on_master() -> Rule:
    return on_branch("master")


def not_on_master() -> Rule:
    return not_on_branch("master")


def on_merge_request_events() -> Rule:
    return Rule(if_statement='$CI_PIPELINE_SOURCE == "merge_request_event"')


def on_success() -> Rule:
    return Rule()


def on_pipeline_trigger() -> Rule:
    """
    ```
    if: '$CI_PIPELINE_SOURCE == "pipeline"'
    ```

    From https://docs.gitlab.com/ee/ci/yaml/

    |pipeline|For multi-project pipelines created by using the API with CI_JOB_TOKEN, or the trigger keyword.|
    """
    return Rule(if_statement='$CI_PIPELINE_SOURCE == "pipeline"')


def on_tags() -> Rule:
    return Rule(if_statement="$CI_COMMIT_TAG")
