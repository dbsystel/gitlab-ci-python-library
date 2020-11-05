import pytest

from gcip import Job, Pipeline
from tests import conftest


@pytest.fixture
def testjob():
    return Job(namespace="testjob", script="foobar")


def test_init_empty_tags(testjob):
    pipeline = Pipeline()
    pipeline.set_tags("foo", "bar", override=False)
    pipeline.add_jobs(testjob)
    conftest.check(pipeline.render())


def test_init_set_tags(testjob):
    pipeline = Pipeline()
    pipeline.set_tags("foo", "bar", override=False)
    testjob.add_tags("keep", "those", "tags")
    pipeline.add_jobs(testjob)
    conftest.check(pipeline.render())


def test_override_tags(testjob):
    pipeline = Pipeline()
    pipeline.set_tags("new", "values")
    testjob.add_tags("replace", "those", "tags")
    pipeline.add_jobs(testjob)
    conftest.check(pipeline.render())
