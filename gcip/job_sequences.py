import gcip
from gcip import jobs


def cdk_diff_deploy(
    *args,
    stack: str,
    toolkit_stack_name: str,
) -> gcip.JobSequence:
    sequence = gcip.JobSequence()
    sequence.add_job(jobs.cdk_diff(stack))
    sequence.add_job(jobs.cdk_deploy(stack, toolkit_stack_name))
    return sequence
