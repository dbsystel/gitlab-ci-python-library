import gcip
from tests import conftest


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(
        gcip.Job(name="job1", stage="single-stage", script="date"),
        gcip.Job(name="job2", stage="single-stage", script="date"),
    )

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['single_stage'],
            'job1': {
                'script': ['date'],
                'stage': 'single_stage'
            },
            'job2': {
                'script': ['date'],
                'stage': 'single_stage'
            }
        },
    )
