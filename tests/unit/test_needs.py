import pytest

from gcip import Job, Need, Pipeline
from tests import conftest


@pytest.fixture
def testjob():
    return Job(namespace="testjob", script="foobar")


def test_simple_need():
    conftest.check(Need("testjob").render())


def test_no_artifacts():
    conftest.check(Need("testjob", artifacts=False).render())


def test_other_project_need():
    conftest.check(Need("testjob", project="foo/bar").render())


def test_other_project_ref_need():
    conftest.check(Need("testjob", project="foo/bar", ref="test").render())


def test_job_with_needs(testjob):
    job = Job(namespace="depending_job", script="bar")
    job.add_needs(testjob, Need("job1"), Need("job2", project="foo/bar"))
    conftest.check(job.render())


def test_sequence_with_needs(testjob):
    pipeline = Pipeline()
    pipeline.add_jobs(Job(namespace="firstjob", script="foo"), Job(namespace="secondjob", script="bar"))
    pipeline.add_needs(testjob, Need("job1"), Need("job2"))
    conftest.check(pipeline.render())


def test_sequence_with_parallel_jobs_and_needs(testjob):
    pipeline = Pipeline()
    pipeline.add_jobs(
        Job(namespace="job", name="first", script="foo"),
        Job(namespace="secondjob", script="bar"),
        Job(namespace="job", name="third", script="baz"),
        Job(namespace="fourthjob", script="maz"),
    )
    pipeline.add_needs(testjob)
    conftest.check(pipeline.render())
