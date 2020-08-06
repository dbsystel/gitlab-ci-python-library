import gcip
from tests import conftest


def job_for(environment: str) -> gcip.Job:
    return gcip.Job(name="do_something", script=f"./do-something-on.sh {environment}")


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_jobs(job_for(env), namespace=env)

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['do_something_development', 'do_something_test'],
            'do_something_development': {
                'script': ['./do-something-on.sh development'],
                'stage': 'do_something_development'
            },
            'do_something_test': {
                'script': ['./do-something-on.sh test'],
                'stage': 'do_something_test'
            }
        },
    )
