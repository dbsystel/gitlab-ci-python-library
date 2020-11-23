import gcip
from tests import conftest
from gcip.job_sequences import cdk


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(cdk.diff_deploy("my-cdk-stack"))

    conftest.check(pipeline.render())
