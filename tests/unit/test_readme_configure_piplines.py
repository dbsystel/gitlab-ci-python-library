import gcip
from tests import conftest


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_pipeline_variables(USER="Kueckii", URL="https://muttergans.de")

    job = gcip.Job(name="print_date", script="date")
    job.add_variables(USER="Max Power", URL="https://example.com")

    pipeline.add_jobs(job)

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'variables': {
                'USER': 'Kueckii',
                'URL': 'https://muttergans.de'
            },
            'stages': ['print_date'],
            'print_date': {
                'script': ['date'],
                'variables': {
                    'USER': 'Max Power',
                    'URL': 'https://example.com'
                },
                'tags': [],
                'stage': 'print_date'
            }
        },
    )
