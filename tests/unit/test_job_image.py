import pytest

from gcip import Job, Image, Pipeline
from tests import conftest


@pytest.fixture
def testjob() -> Job:
    return Job(namespace="testjob", script="foobar")


def test_init_unset_image(testjob):
    pipeline = Pipeline()
    pipeline.initialize_image("foobar")
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())


def test_init_set_image(testjob):
    pipeline = Pipeline()
    pipeline.initialize_image("unwanted-image")
    testjob.set_image("keep-this-image")
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())


def test_override_image(testjob):
    pipeline = Pipeline()
    pipeline.override_image("wanted-image")
    testjob.set_image("replace-this-image")
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())


def test_job_with_image_object(testjob):
    pipeline = Pipeline()
    pipeline.add_children(testjob.set_image(Image("awsome/image:123")))
    conftest.check(pipeline.render())
