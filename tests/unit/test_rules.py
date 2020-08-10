import gcip
from gcip import rules
from tests import conftest


def test_on_success():
    pipeline = gcip.Pipeline()
    job = gcip.Job(name="testjob", script="foo")
    job.append_rules(rules.on_success())
    pipeline.add_jobs(job)

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['testjob'],
            'testjob': {
                'script': ['foo'],
                'rules': [{
                    'when': 'on_success',
                    'allow_failure': False
                }],
                'stage': 'testjob'
            }
        },
    )


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

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['testjob'],
            'testjob': {
                'script': ['foo'],
                'variables': {},
                'tags': [],
                'rules': [
                    {
                        'if': '6',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': '4',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': '1',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': 'g',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': 'h',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': 'c',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': 'd',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': 'a',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': 'b',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': 'e',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': 'f',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': '2',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': '3',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': '5',
                        'when': 'on_success',
                        'allow_failure': False
                    }
                ],
                'stage':
                'testjob'
            }
        },
    )
