from ._core.rule import Rule


def on_branch(branch_name: str) -> Rule:
    return Rule(if_statement=f'$CI_COMMIT_REF_NAME == "{branch_name}"')


def on_master() -> Rule:
    return on_branch("master")


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
    return Rule(if_statement='$CI_COMMIT_TAG')
