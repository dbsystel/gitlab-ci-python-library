import pytest

import gcip


def job_for(environment: str) -> gcip.Job:
    return gcip.Job(namespace="do_something", script=f"./do-something-on.sh {environment}")


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_children(job_for(env))

    with pytest.raises(ValueError, match="NAMING CONFLICT: Two jobs have the same name"):
        pipeline.render()
