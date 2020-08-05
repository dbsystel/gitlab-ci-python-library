import gcip


def test():
    job_sequence = gcip.JobSequence()

    job1 = gcip.Job(name="job1", script="script1.sh")
    job1.prepend_script("from-job-1.sh")

    job_sequence.add_job(job1)
    job_sequence.add_job(gcip.Job(name="job2", script="script2.sh"))

    job_sequence.prepend_script("from-sequence.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_job(job_sequence)

    pipeline.print_yaml()
