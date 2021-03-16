import pytest

from gcip import Job, Need, Pipeline, Sequence
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
    conftest.check(Pipeline().add_children(testjob, job).render())


def test_sequence_with_needs(testjob):
    sequence = Sequence()
    pipeline = Pipeline()
    pipeline.add_children(testjob).add_children(sequence)
    sequence.add_children(Job(namespace="firstjob", script="foo"), Job(namespace="secondjob", script="bar"))
    sequence.add_needs(testjob, Need("job1"), Need("job2"))
    conftest.check(pipeline.render())


def test_sequence_with_parallel_jobs_and_needs(testjob):
    sequence = Sequence()
    pipeline = Pipeline()
    pipeline.add_children(testjob).add_children(sequence)
    sequence.add_children(
        Job(namespace="job", name="first", script="foo"),
        Job(namespace="secondjob", script="bar"),
        Job(namespace="job", name="third", script="baz"),
        Job(namespace="fourthjob", script="maz"),
    )
    sequence.add_needs(testjob)
    conftest.check(pipeline.render())


def test_add_sequence_as_need(testjob):
    sequence = Sequence()
    sequence.add_children(
        Job(namespace="first", name="A", script="firstDateA"),
        Job(namespace="second", name="A", script="secondDateA"),
        Job(namespace="last", name="A", script="lastDateA"),
        Job(namespace="second", name="B", script="secondDateB"),
        Job(namespace="last", name="B", script="lastDateB"),
        Job(namespace="first", name="B", script="firstDateB"),
    )

    testjob.add_needs(sequence)

    pipeline = Pipeline()
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())


def test_needs_will_be_namespaced():
    job1 = Job(namespace="first", script="foobar")
    sequence = Sequence().add_children(Job(namespace="second", script="foobar"), namespace="SSS")

    targetJob = Job(namespace="target1", script="foobar").add_needs(job1, sequence)
    targetSequence = Sequence().add_children(Job(namespace="target2", script="foobar"), namespace="TTT").add_needs(job1, sequence)

    sequenceWithoutNamespace = Sequence()
    sequenceWithoutNamespace.add_children(job1)
    sequenceWithoutNamespace.add_children(sequence)

    parentSequence = Sequence().add_children(sequenceWithoutNamespace, namespace="abc")

    parentSequence2 = Sequence()
    parentSequence2.add_children(targetJob, namespace="xyz")
    parentSequence2.add_children(targetSequence, namespace="xyz")

    parentParentSequence = Sequence().add_children(parentSequence, namespace="123")

    pipeline = Pipeline().add_children(parentParentSequence, parentSequence2, namespace="final")
    conftest.check(pipeline.render())
