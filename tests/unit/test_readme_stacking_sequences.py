import gcip
from tests import conftest


def test():
    sequence_a = gcip.JobSequence()
    sequence_a.add_jobs(gcip.Job(name="job1", script="script1.sh"))
    sequence_a.prepend_script("from-sequence-a.sh")

    sequence_b = gcip.JobSequence()
    sequence_b.add_sequences(sequence_a)
    sequence_b.add_jobs(gcip.Job(name="job2", script="script2.sh"))
    sequence_b.prepend_script("from-sequence-b.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_jobs(sequence_b)

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['job1', 'job2'],
            'job1': {
                'script': ['from-sequence-b.sh', 'from-sequence-a.sh', 'script1.sh'],
                'stage': 'job1'
            },
            'job2': {
                'script': ['from-sequence-b.sh', 'script2.sh'],
                'stage': 'job2'
            }
        },
    )
