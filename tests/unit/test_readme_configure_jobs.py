import gcip
from tests import conftest


def test():
    pipeline = gcip.Pipeline()

    job = gcip.Job(name="print_date", script="date")
    job.set_image("docker/image:example")
    job.prepend_script("./before-script.sh")
    job.append_script("./after-script.sh")
    job.add_variables(USER="Max Power", URL="https://example.com")
    job.add_tags("test", "europe")
    job.add_artifacts_paths("binaries/", ".config")
    job.add_rules(gcip.Rule(if_statement="$MY_VARIABLE_IS_PRESENT"))

    pipeline.add_jobs(job)

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['print_date'],
            'print_date': {
                'script': ['./before-script.sh', 'date', './after-script.sh'],
                'variables': {
                    'USER': 'Max Power',
                    'URL': 'https://example.com'
                },
                'tags': ['test', 'europe'],
                'artifacts': {
                    'paths': ['binaries/', '.config']
                },
                'rules': [{
                    'if': '$MY_VARIABLE_IS_PRESENT',
                    'when': 'on_success',
                    'allow_failure': False
                }],
                'image': 'docker/image:example',
                'stage': 'print_date'
            }
        },
    )
