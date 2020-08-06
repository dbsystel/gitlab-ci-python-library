import gcip
from gcip.jobs import python


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_job(python.flake8())
    pipeline.print_yaml()
