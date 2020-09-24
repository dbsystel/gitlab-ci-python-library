import gcip
from gcip import rules
from tests import conftest


def test_on_success():
    pipeline = gcip.Pipeline()
    job = gcip.Job(name="testjob", script="foo")
    job.append_rules(rules.on_success())
    pipeline.add_jobs(job)

    conftest.check(pipeline.render())


def test_rule_order():
    pipeline = gcip.Pipeline()
    sequence = gcip.JobSequence()
    sequence.prepend_rules(gcip.Rule(if_statement="1"))
    sequence.append_rules(gcip.Rule(if_statement="2"))

    job = gcip.Job(name="testjob", script="foo")
    sequence.add_jobs(job)

    job.append_rules(gcip.Rule(if_statement="a"), gcip.Rule(if_statement="b"))
    job.prepend_rules(gcip.Rule(if_statement="c"), gcip.Rule(if_statement="d"))

    sequence.append_rules(gcip.Rule(if_statement="3"))
    sequence.prepend_rules(gcip.Rule(if_statement="4"))

    job.append_rules(gcip.Rule(if_statement="e"), gcip.Rule(if_statement="f"))
    job.prepend_rules(gcip.Rule(if_statement="g"), gcip.Rule(if_statement="h"))

    sequence.append_rules(gcip.Rule(if_statement="5"))
    sequence.prepend_rules(gcip.Rule(if_statement="6"))

    pipeline.add_sequences(sequence)

    conftest.check(pipeline.render())
