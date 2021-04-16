import pytest

from gcip import Job, Pipeline
from tests import conftest


@pytest.fixture
def testjob():
    return Job(stage="testjob", script="foobar")


def test_init_empty_tags(testjob):
    pipeline = Pipeline()
    pipeline.initialize_tags("foo", "bar")
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())


def test_init_non_empty_tags(testjob):
    pipeline = Pipeline()
    pipeline.initialize_tags("foo", "bar")
    testjob.add_tags("keep", "those", "tags")
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())


def test_override_tags(testjob):
    pipeline = Pipeline()
    pipeline.override_tags("new", "values")
    testjob.add_tags("replace", "those", "tags")
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())
