import gcip
from tests import conftest


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(
        gcip.Job(name="job1", namespace="single-stage", script="date"),
        gcip.Job(name="job2", namespace="single-stage", script="date"),
    )

    conftest.check(pipeline.render())
