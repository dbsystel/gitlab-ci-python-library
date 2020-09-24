import gcip
from tests import conftest
from gcip.job_sequences import cdk


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(cdk.diff_deploy(stack="my-cdk-stack", toolkit_stack_name="cdk-toolkit"))

    conftest.check(pipeline.render())
