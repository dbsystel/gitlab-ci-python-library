import gcip
from tests import conftest
from gcip.jobs import python


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(python.flake8())

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['lint'],
            'flake8': {
                'script': ['pip3 install --upgrade flake8', 'flake8'],
                'stage': 'lint'
            }
        },
    )
