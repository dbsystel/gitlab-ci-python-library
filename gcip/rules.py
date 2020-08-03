from gcip import gcip


def not_on_merge_request_events() -> gcip.Rule:
    return gcip.Rule(if_statement='$CI_PIPELINE_SOURCE == "merge_request_event"', when=gcip.WhenStatement.NEVER)
