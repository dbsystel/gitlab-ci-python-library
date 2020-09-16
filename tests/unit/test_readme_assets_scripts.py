import gcip
from gcip import scripts
from tests import conftest


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(gcip.Job(name="print_date", script=scripts.clone_repository("path/to/group")))

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['print_date'],
            'print-date': {
                'script':
                ['git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/path/to/group.git'],
                'stage':
                'print_date'
            }
        },
    )
