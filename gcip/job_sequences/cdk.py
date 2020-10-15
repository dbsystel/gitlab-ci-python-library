from typing import Any

from ..jobs import cdk
from .._core.job_sequence import JobSequence


def diff_deploy(
    *args: Any,
    stack: str,
    toolkit_stack_name: str,
) -> JobSequence:
    sequence = JobSequence()
    sequence.add_jobs(
        cdk.diff(stack),
        cdk.deploy(stack, toolkit_stack_name),
    )
    return sequence
