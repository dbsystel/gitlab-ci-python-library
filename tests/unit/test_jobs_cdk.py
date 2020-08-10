import gcip
from gcip.jobs import cdk
from tests import conftest


def test_bootstrap() -> None:
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(cdk.bootstrap(
        toolkit_stack_name="my-cdk-toolkit-dev",
        bootstrap_kms_key_id="abcd",
    ), namespace="dev")
    pipeline.add_jobs(
        cdk.bootstrap(
            toolkit_stack_name="my-cdk-toolkit-tst",
            bootstrap_kms_key_id="abcd",
            ApplicationName="testapp",
            Subsystem="testsystem",
        ),
        namespace="tst"
    )

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['cdk_bootstrap_dev', 'cdk_bootstrap_tst'],
            'cdk_bootstrap_dev': {
                'script': [
                    'cdk bootstrap --toolkit-stack-name my-cdk-toolkit-dev --bootstrap-kms-key-id abcd aws://${AWS_ACCOUNT_ID}/${AWS_DEFAULT_REGION}'
                ],
                'stage':
                'cdk_bootstrap_dev'
            },
            'cdk_bootstrap_tst': {
                'script': [
                    'cdk bootstrap --toolkit-stack-name my-cdk-toolkit-tst --bootstrap-kms-key-id abcd aws://${AWS_ACCOUNT_ID}/${AWS_DEFAULT_REGION} -t ApplicationName=testapp -t Subsystem=testsystem'
                ],
                'stage':
                'cdk_bootstrap_tst'
            }
        },
    )
