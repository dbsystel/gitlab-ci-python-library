import gcip
from tests import conftest


def test():
    sequence_a = gcip.Sequence()
    sequence_a.add_children(gcip.Job(stage="job1", script="script1.sh"))
    sequence_a.prepend_scripts("from-sequence.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_children(sequence_a)
    pipeline.add_children(gcip.Job(stage="job2", script="script2.sh"))
    pipeline.prepend_scripts("from-pipeline.sh")

    conftest.check(pipeline.render())
