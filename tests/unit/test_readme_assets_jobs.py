import gcip
from tests import conftest
from gcip.addons.python import jobs as python


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_children(python.flake8())

    conftest.check(pipeline.render())
