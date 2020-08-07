import gcip


def on_merge_request_events() -> gcip.Rule:
    return gcip.Rule(if_statement='$CI_PIPELINE_SOURCE == "merge_request_event"')


def on_branch(branch_name: str) -> gcip.Rule:
    return gcip.Rule(if_statement=f'$CI_COMMIT_REF_NAME == "{branch_name}"')


def on_master() -> gcip.Rule:
    return on_branch("master")


def on_tags() -> gcip.Rule:
    return gcip.Rule(if_statement='$CI_COMMIT_TAG')
