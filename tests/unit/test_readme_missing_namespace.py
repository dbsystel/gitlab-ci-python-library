import gcip


def job_for(environment: str) -> gcip.Job:
    return gcip.Job(name="do_something", script=f"./do-something-on.sh {environment}")


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_job(job_for(env))

    pipeline.print_yaml()
