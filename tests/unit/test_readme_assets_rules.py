import gcip
from gcip import rules


def test():
    job = gcip.Job(name="print_date", script="date")
    job.add_rules(rules.not_on_merge_request_events())

    pipeline = gcip.Pipeline()
    pipeline.add_jobs(job)
    pipeline.print_yaml()
