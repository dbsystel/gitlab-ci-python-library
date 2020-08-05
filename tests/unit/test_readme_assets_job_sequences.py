import gcip
from gcip import job_sequences


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_job(job_sequences.cdk_diff_deploy(stack="my-cdk-stack", toolkit_stack_name="cdk-toolkit"))
    pipeline.print_yaml()
