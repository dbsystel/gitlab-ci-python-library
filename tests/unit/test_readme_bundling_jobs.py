import gcip
from tests import conftest


def test():
    job_sequence = gcip.JobSequence()

    job1 = gcip.Job(namespace="job1", script="script1.sh")
    job1.prepend_scripts("from-job-1.sh")

    job_sequence.add_jobs(
        job1,
        gcip.Job(namespace="job2", script="script2.sh"),
    )

    job_sequence.prepend_scripts("from-sequence.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_jobs(job_sequence)

    conftest.check(pipeline.render())
