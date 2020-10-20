import pytest

from gcip import Job, Need, Pipeline
from tests import conftest


@pytest.fixture
def testjob():
    return Job(namespace="testjob", script="foobar")


def test_simple_need():
    conftest.check(Need("testjob").render())


def test_default_need(testjob):
    conftest.check(Need(testjob).render())


def test_no_artifacts(testjob):
    conftest.check(Need(testjob, artifacts=False).render())


def test_other_project_need(testjob):
    conftest.check(Need(testjob, project="foo/bar").render())


def test_other_project_ref_need(testjob):
    conftest.check(Need(testjob, project="foo/bar", ref="test").render())


def test_job_with_needs():
    job = Job(namespace="depending_job", script="bar")
    job.add_needs(Need("job1"), Need("job2", project="foo/bar"))
    conftest.check(job.render())


def test_sequence_with_needs():
    pipeline = Pipeline()
    pipeline.add_jobs(Job(namespace="testjob", script="foobar"))
    pipeline.add_needs(Need("job1"), Need("job2"))
    conftest.check(pipeline.render())
