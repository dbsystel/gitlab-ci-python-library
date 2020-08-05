import gcip


def test():
    sequence_a = gcip.JobSequence()
    sequence_a.add_job(gcip.Job(name="job1", script="script1.sh"))
    sequence_a.prepend_script("from-sequence.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_sequence(sequence_a)
    pipeline.add_job(gcip.Job(name="job2", script="script2.sh"))
    pipeline.prepend_script("from-pipeline.sh")

    pipeline.print_yaml()
