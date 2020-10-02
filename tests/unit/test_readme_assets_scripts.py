import gcip
from gcip import scripts
from tests import conftest


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(gcip.Job(namespace="print_date", script=scripts.clone_repository("path/to/group")))

    conftest.check(pipeline.render())
