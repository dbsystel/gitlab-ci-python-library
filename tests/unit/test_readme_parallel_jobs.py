import gcip


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_job(gcip.Job(name="job1", stage="single-stage", script="date"))
    pipeline.add_job(gcip.Job(name="job2", stage="single-stage", script="date"))
    pipeline.print_yaml()
