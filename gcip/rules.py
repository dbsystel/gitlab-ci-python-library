import gcip


def not_on_merge_request_events() -> gcip.Rule:
    return gcip.Rule(if_statement='$CI_PIPELINE_SOURCE == "merge_request_event"', when=gcip.WhenStatement.NEVER)


def only_branch(branch_name: str) -> gcip.Rule:
    return gcip.Rule(if_statement=f'$CI_COMMIT_REF_NAME == "branch_name"')


def only_master() -> gcip.Rule:
    return only_branch("master")


def only_tags() -> gcip.Rule:
    return gcip.Rule(if_statement='$CI_COMMIT_TAG')
