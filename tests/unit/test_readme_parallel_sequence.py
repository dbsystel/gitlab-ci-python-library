import gcip
from tests import conftest


def environment_pipeline(environment: str) -> gcip.JobSequence:
    sequence = gcip.JobSequence()
    sequence.add_jobs(
        gcip.Job(name="job1", script=f"job-1-on-{environment}"),
        gcip.Job(name="job2", script=f"job-2-on-{environment}"),
    )
    return sequence


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_sequence(environment_pipeline(env), name=env)

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['job1', 'job2'],
            'job1_development': {
                'script': ['job-1-on-development'],
                'stage': 'job1'
            },
            'job2_development': {
                'script': ['job-2-on-development'],
                'stage': 'job2'
            },
            'job1_test': {
                'script': ['job-1-on-test'],
                'stage': 'job1'
            },
            'job2_test': {
                'script': ['job-2-on-test'],
                'stage': 'job2'
            }
        },
    )
