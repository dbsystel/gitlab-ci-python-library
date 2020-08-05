import gcip
from gcip import scripts


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_job(gcip.Job(name="print_date", script=scripts.clone_repository("path/to/group")))
    pipeline.print_yaml()
