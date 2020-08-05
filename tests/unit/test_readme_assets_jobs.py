import gcip
from gcip import jobs


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_job(jobs.cdk_diff("my-cdk-stack"))
    pipeline.print_yaml()
