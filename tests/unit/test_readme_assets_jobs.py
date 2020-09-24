import gcip
from tests import conftest
from gcip.jobs import python


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(python.flake8())

    conftest.check(pipeline.render())
