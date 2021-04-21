import pytest

from gcip import Job, Pipeline, JobNameConflictError


def job_for(environment: str) -> Job:
    return Job(stage="do_something", script=f"./do-something-on.sh {environment}")


def test():
    pipeline = Pipeline()
    for env in ["development", "test"]:
        pipeline.add_children(job_for(env))

    with pytest.raises(JobNameConflictError):
        pipeline.render()
