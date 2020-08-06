import gcip
from tests import conftest


def job_for(environment: str) -> gcip.Job:
    return gcip.Job(name="do_something", script=f"./do-something-on.sh {environment}")


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_jobs(job_for(env))

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['do_something'],
            'do_something': {
                'script': ['./do-something-on.sh test'],
                'stage': 'do_something'
            }
        },
    )
