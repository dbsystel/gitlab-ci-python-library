import gcip
from tests import conftest


def test():
    sequence_a = gcip.JobSequence()
    sequence_a.add_jobs(gcip.Job(name="job1", script="script1.sh"))
    sequence_a.prepend_scripts("from-sequence-a.sh")

    sequence_b = gcip.JobSequence()
    sequence_b.add_sequences(sequence_a)
    sequence_b.add_jobs(gcip.Job(name="job2", script="script2.sh"))
    sequence_b.prepend_scripts("from-sequence-b.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_jobs(sequence_b)

    conftest.check(pipeline.render())
