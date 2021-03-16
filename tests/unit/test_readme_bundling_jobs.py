import gcip
from tests import conftest


def test():
    sequence = gcip.Sequence()

    job1 = gcip.Job(namespace="job1", script="script1.sh")
    job1.prepend_scripts("from-job-1.sh")

    sequence.add_children(
        job1,
        gcip.Job(namespace="job2", script="script2.sh"),
    )

    sequence.prepend_scripts("from-sequence.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_children(sequence)

    conftest.check(pipeline.render())
