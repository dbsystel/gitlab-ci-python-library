import gcip
from tests import conftest
from gcip.job_sequences import cdk


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(cdk.diff_deploy(stack="my-cdk-stack", toolkit_stack_name="cdk-toolkit"))

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['diff', 'deploy'],
            'cdk-diff': {
                'script': ['cdk synth my-cdk-stack', 'cdk diff my-cdk-stack'],
                'stage': 'diff'
            },
            'cdk-deploy': {
                'script': ["cdk deploy --strict --require-approval 'never' --toolkit-stack-name cdk-toolkit my-cdk-stack"],
                'stage': 'deploy'
            }
        },
    )
