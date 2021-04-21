import gcip
from tests import conftest
from gcip.addons.gitlab import job_scripts as scripts


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_children(gcip.Job(stage="print_date", script=scripts.clone_repository("path/to/group")))

    conftest.check(pipeline.render())
