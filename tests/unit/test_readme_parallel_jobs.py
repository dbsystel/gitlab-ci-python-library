import gcip


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(
        gcip.Job(name="job1", stage="single-stage", script="date"),
        gcip.Job(name="job2", stage="single-stage", script="date"),
    )
    pipeline.print_yaml()
