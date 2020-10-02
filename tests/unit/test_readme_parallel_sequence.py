import gcip
from tests import conftest


def environment_pipeline(environment: str) -> gcip.JobSequence:
    sequence = gcip.JobSequence()
    sequence.add_jobs(
        gcip.Job(namespace="job1", script=f"job-1-on-{environment}"),
        gcip.Job(namespace="job2", script=f"job-2-on-{environment}"),
    )
    return sequence


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_sequences(environment_pipeline(env), name=env)

    conftest.check(pipeline.render())
