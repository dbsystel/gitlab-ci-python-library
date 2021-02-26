import pytest

from gcip import Job, Pipeline
from tests import conftest


@pytest.fixture
def testjob():
    return Job(namespace="testjob", script="foobar")


def test_init_empty_variables(testjob):
    pipeline = Pipeline()
    pipeline.initialize_variables(variable1="foo", variable2="bar")
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())


def test_init_non_empty_variables(testjob):
    pipeline = Pipeline()
    pipeline.initialize_variables(variable1="foo", variable2="bar")
    testjob.add_variables(variable1="keep", variable2="those", variable3="variables")
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())


def test_override_variables(testjob):
    pipeline = Pipeline()
    pipeline.override_variables(variable1="new", variable2="values")
    testjob.add_variables(variable1="replace", variable2="those", variable3="variables")
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())
