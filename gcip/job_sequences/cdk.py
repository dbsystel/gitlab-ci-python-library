import gcip
from gcip.jobs import cdk


def diff_deploy(
    *args,
    stack: str,
    toolkit_stack_name: str,
) -> gcip.JobSequence:
    sequence = gcip.JobSequence()
    sequence.add_job(cdk.diff(stack))
    sequence.add_job(cdk.deploy(stack, toolkit_stack_name))
    return sequence
