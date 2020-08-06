from typing import Any

import gcip
from gcip.jobs import cdk


def diff_deploy(
    *args: Any,
    stack: str,
    toolkit_stack_name: str,
) -> gcip.JobSequence:
    sequence = gcip.JobSequence()
    sequence.add_jobs(
        cdk.diff(stack),
        cdk.deploy(stack, toolkit_stack_name),
    )
    return sequence
