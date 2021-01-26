import gcip
from tests import conftest
from gcip.addons.cdk import sequences as cdk


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(cdk.diff_deploy("my-cdk-stack", toolkit_stack_name="cdk-toolkit"))

    conftest.check(pipeline.render())
