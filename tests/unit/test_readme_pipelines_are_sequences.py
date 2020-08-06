import gcip
from tests import conftest


def test():
    sequence_a = gcip.JobSequence()
    sequence_a.add_jobs(gcip.Job(name="job1", script="script1.sh"))
    sequence_a.prepend_script("from-sequence.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_sequence(sequence_a)
    pipeline.add_jobs(gcip.Job(name="job2", script="script2.sh"))
    pipeline.prepend_script("from-pipeline.sh")

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['job1', 'job2'],
            'job1': {
                'script': ['from-pipeline.sh', 'from-sequence.sh', 'script1.sh'],
                'stage': 'job1'
            },
            'job2': {
                'script': ['from-pipeline.sh', 'script2.sh'],
                'stage': 'job2'
            }
        },
    )
