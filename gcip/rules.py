import gcip


def on_branch(branch_name: str) -> gcip.Rule:
    return gcip.Rule(if_statement=f'$CI_COMMIT_REF_NAME == "{branch_name}"')


def on_master() -> gcip.Rule:
    return on_branch("master")


def on_merge_request_events() -> gcip.Rule:
    return gcip.Rule(if_statement='$CI_PIPELINE_SOURCE == "merge_request_event"')


def on_success() -> gcip.Rule:
    return gcip.Rule()


def on_pipeline_trigger() -> gcip.Rule:
    """
    ```
    if: '$CI_PIPELINE_SOURCE == "pipeline" || $CI_PIPELINE_SOURCE == "parent_pipeline"'
    ```

    From https://docs.gitlab.com/ee/ci/yaml/

    |pipeline|For multi-project pipelines created by using the API with CI_JOB_TOKEN, or the trigger keyword.|
    |parent_pipeline|For pipelines triggered by a parent/child pipeline with rules, use this in the child pipeline
      configuration so that it can be triggered by the parent pipeline.|
    """
    return gcip.Rule(if_statement='$CI_PIPELINE_SOURCE == "pipeline" || $CI_PIPELINE_SOURCE == "parent_pipeline"')


def on_tags() -> gcip.Rule:
    return gcip.Rule(if_statement='$CI_COMMIT_TAG')
