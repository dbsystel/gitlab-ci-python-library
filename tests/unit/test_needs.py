import pytest

from gcip import Job, Need, Pipeline, Sequence
from tests import conftest


@pytest.fixture
def testjob():
    return Job(stage="testjob", script="foobar")


def test_simple_need():
    conftest.check(Need("testjob").render())


def test_no_artifacts():
    conftest.check(Need("testjob", artifacts=False).render())


def test_other_project_need():
    conftest.check(Need("testjob", project="foo/bar").render())


def test_other_project_ref_need():
    conftest.check(Need("testjob", project="foo/bar", ref="test").render())


def test_job_with_needs(testjob):
    job = Job(stage="depending_job", script="bar")
    job.add_needs(testjob, Need("job1"), Need("job2", project="foo/bar"))
    conftest.check(Pipeline().add_children(testjob, job).render())


def test_sequence_with_needs(testjob):
    sequence = Sequence()
    pipeline = Pipeline()
    pipeline.add_children(testjob).add_children(sequence)
    sequence.add_children(Job(stage="firstjob", script="foo"), Job(stage="secondjob", script="bar"))
    sequence.add_needs(testjob, Need("job1"), Need("job2"))
    conftest.check(pipeline.render())


def test_sequence_with_parallel_jobs_and_needs(testjob):
    sequence = Sequence()
    pipeline = Pipeline()
    pipeline.add_children(testjob).add_children(sequence)
    sequence.add_children(
        Job(stage="job", name="first", script="foo"),
        Job(stage="secondjob", script="bar"),
        Job(stage="job", name="third", script="baz"),
        Job(stage="fourthjob", script="maz"),
    )
    sequence.add_needs(testjob)
    conftest.check(pipeline.render())


def test_add_sequence_as_need(testjob):
    sequence = Sequence()
    sequence.add_children(
        Job(stage="first", name="A", script="firstDateA"),
        Job(stage="second", name="A", script="secondDateA"),
        Job(stage="last", name="A", script="lastDateA"),
        Job(stage="second", name="B", script="secondDateB"),
        Job(stage="last", name="B", script="lastDateB"),
        Job(stage="first", name="B", script="firstDateB"),
    )

    testjob.add_needs(sequence)

    pipeline = Pipeline()
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())


def test_needs_will_be_staged():
    job1 = Job(stage="first", script="foobar")
    sequence = Sequence().add_children(Job(stage="second", script="foobar"), stage="SSS")

    targetJob = Job(stage="target1", script="foobar").add_needs(job1, sequence)
    targetSequence = Sequence().add_children(Job(stage="target2", script="foobar"), stage="TTT").add_needs(job1, sequence)

    sequenceWithoutStage = Sequence()
    sequenceWithoutStage.add_children(job1)
    sequenceWithoutStage.add_children(sequence)

    parentSequence = Sequence().add_children(sequenceWithoutStage, stage="abc")

    parentSequence2 = Sequence()
    parentSequence2.add_children(targetJob, stage="xyz")
    parentSequence2.add_children(targetSequence, stage="xyz")

    parentParentSequence = Sequence().add_children(parentSequence, stage="123")

    pipeline = Pipeline().add_children(parentParentSequence, parentSequence2, stage="final")
    conftest.check(pipeline.render())
