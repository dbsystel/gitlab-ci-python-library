import gcip
from tests import conftest


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(gcip.Job(name="print_date", script="date"))

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['print_date'],
            'print_date': {
                'script': ['date'],
                'stage': 'print_date'
            }
        },
    )
