import pytest

from gcip import Job, Rule, Pipeline, JobSequence
from tests import conftest
from gcip.lib import rules


@pytest.fixture
def testjob():
    return Job(namespace="testjob", script="foobar")


def test_on_success():
    pipeline = Pipeline()
    job = Job(namespace="testjob", script="foo")
    job.append_rules(rules.on_success())
    pipeline.add_children(job)

    conftest.check(pipeline.render())


def test_rule_order():
    pipeline = Pipeline()
    sequence = JobSequence()
    sequence.prepend_rules(Rule(if_statement="1"))
    sequence.append_rules(Rule(if_statement="2"))

    job = Job(namespace="testjob", script="foo")
    sequence.add_children(job)

    job.append_rules(Rule(if_statement="a"), Rule(if_statement="b"))
    job.prepend_rules(Rule(if_statement="c"), Rule(if_statement="d"))

    sequence.append_rules(Rule(if_statement="3"))
    sequence.prepend_rules(Rule(if_statement="4"))

    job.append_rules(Rule(if_statement="e"), Rule(if_statement="f"))
    job.prepend_rules(Rule(if_statement="g"), Rule(if_statement="h"))

    sequence.append_rules(Rule(if_statement="5"))
    sequence.prepend_rules(Rule(if_statement="6"))

    pipeline.add_children(sequence)

    conftest.check(pipeline.render())


def test_init_empty_rules(testjob):
    pipeline = Pipeline()
    pipeline.initialize_rules(Rule(if_statement="foo"), Rule(if_statement="bar"))
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())


def test_init_non_empty_rules(testjob):
    pipeline = Pipeline()
    pipeline.initialize_rules(Rule(if_statement="foo"), Rule(if_statement="bar"))
    testjob.append_rules(Rule(if_statement="keep"), Rule(if_statement="those"), Rule(if_statement="rules"))
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())


def test_override_rules(testjob):
    pipeline = Pipeline()
    pipeline.override_rules(Rule(if_statement="new"), Rule(if_statement="values"))
    testjob.append_rules(Rule(if_statement="replace"), Rule(if_statement="those"), Rule(if_statement="rules"))
    pipeline.add_children(testjob)
    conftest.check(pipeline.render())
