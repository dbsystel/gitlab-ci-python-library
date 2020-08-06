import gcip
from gcip import rules
from tests import conftest


def test():
    job = gcip.Job(name="print_date", script="date")
    job.add_rules(rules.not_on_merge_request_events())

    pipeline = gcip.Pipeline()
    pipeline.add_jobs(job)

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['print_date'],
            'print_date': {
                'script': ['date'],
                'rules': [{
                    'if': '$CI_PIPELINE_SOURCE == "merge_request_event"',
                    'when': 'never',
                    'allow_failure': False
                }],
                'stage': 'print_date'
            }
        },
    )
