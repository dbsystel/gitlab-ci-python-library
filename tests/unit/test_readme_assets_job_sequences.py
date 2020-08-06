import gcip
from gcip.job_sequences import cdk


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_job(cdk.diff_deploy(stack="my-cdk-stack", toolkit_stack_name="cdk-toolkit"))
    pipeline.print_yaml()
