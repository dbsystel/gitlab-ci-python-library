import gcip
from tests import conftest


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(gcip.Job(namespace="print_date", script="date"))

    conftest.check(pipeline.render())
