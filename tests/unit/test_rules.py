import gcip
from gcip import rules
from tests import conftest


def test_on_success():
    pipeline = gcip.Pipeline()
    job = gcip.Job(name="testjob", script="foo")
    job.add_rules(rules.on_success())
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
