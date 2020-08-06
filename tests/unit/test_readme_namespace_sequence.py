import gcip


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
        pipeline.add_sequence(environment_pipeline(env), namespace=env)

    pipeline.print_yaml()
