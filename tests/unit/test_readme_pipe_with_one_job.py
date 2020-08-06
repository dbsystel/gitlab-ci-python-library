import gcip


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(gcip.Job(name="print_date", script="date"))
    pipeline.print_yaml()
