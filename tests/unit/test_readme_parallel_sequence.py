import gcip


def environment_pipeline(environment: str) -> gcip.JobSequence:
    sequence = gcip.JobSequence()
    sequence.add_job(gcip.Job(name="job1", script=f"job-1-on-{environment}"))
    sequence.add_job(gcip.Job(name="job2", script=f"job-2-on-{environment}"))
    return sequence


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_sequence(environment_pipeline(env), name=env)

    pipeline.print_yaml()
