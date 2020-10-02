import gcip
from gcip import rules
from tests import conftest


def test():
    job = gcip.Job(namespace="print_date", script="date")
    job.append_rules(
        rules.on_merge_request_events().never(),
        rules.on_master(),
    )

    pipeline = gcip.Pipeline()
    pipeline.add_jobs(job)

    conftest.check(pipeline.render())
