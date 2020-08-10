import gcip
from tests import conftest


def test():
    job_sequence = gcip.JobSequence()

    job1 = gcip.Job(name="job1", script="script1.sh")
    job1.prepend_scripts("from-job-1.sh")

    job_sequence.add_jobs(
        job1,
        gcip.Job(name="job2", script="script2.sh"),
    )

    job_sequence.prepend_scripts("from-sequence.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_jobs(job_sequence)

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['job1', 'job2'],
            'job1': {
                'script': ['from-sequence.sh', 'from-job-1.sh', 'script1.sh'],
                'variables': {},
                'tags': [],
                'stage': 'job1'
            },
            'job2': {
                'script': ['from-sequence.sh', 'script2.sh'],
                'variables': {},
                'tags': [],
                'stage': 'job2'
            }
        },
    )
