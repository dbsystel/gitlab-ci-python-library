import gcip
from tests import conftest


def job_for(environment: str) -> gcip.Job:
    return gcip.Job(stage="do_something", script=f"./do-something-on.sh {environment}")


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_children(job_for(env), stage=env)

    conftest.check(pipeline.render())
