import gcip
from tests import conftest


def test():
    sequence_a = gcip.Sequence()
    sequence_a.add_children(gcip.Job(namespace="job1", script="script1.sh"))
    sequence_a.prepend_scripts("from-sequence-a.sh")

    sequence_b = gcip.Sequence()
    sequence_b.add_children(sequence_a)
    sequence_b.add_children(gcip.Job(namespace="job2", script="script2.sh"))
    sequence_b.prepend_scripts("from-sequence-b.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_children(sequence_b)

    conftest.check(pipeline.render())
