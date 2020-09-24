import gcip
from tests import conftest


def test():
    sequence_a = gcip.JobSequence()
    sequence_a.add_jobs(gcip.Job(name="job1", script="script1.sh"))
    sequence_a.prepend_scripts("from-sequence.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_sequences(sequence_a)
    pipeline.add_jobs(gcip.Job(name="job2", script="script2.sh"))
    pipeline.prepend_scripts("from-pipeline.sh")

    conftest.check(pipeline.render())
