import gcip
from tests import conftest
from gcip.jobs import cdk


def test_bootstrap() -> None:
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(
        cdk.bootstrap(
            aws_account_id="1234567890",
            aws_region="net-wunderland-1",
            toolkit_stack_name="my-cdk-toolkit-dev",
            bootstrap_kms_key_id="abcd",
        ),
        namespace="dev"
    )
    pipeline.add_jobs(
        cdk.bootstrap(
            aws_account_id="1234567890",
            aws_region="net-wunderland-1",
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
                    'cdk bootstrap --toolkit-stack-name my-cdk-toolkit-dev --bootstrap-kms-key-id abcd aws://1234567890/net-wunderland-1'  # noqa: E501,W505
                ],
                'stage':
                'cdk_bootstrap_dev'
            },
            'cdk_bootstrap_tst': {
                'script': [
                    'cdk bootstrap --toolkit-stack-name my-cdk-toolkit-tst --bootstrap-kms-key-id abcd aws://1234567890/net-wunderland-1 -t ApplicationName=testapp -t Subsystem=testsystem'  # noqa: E501,W505
                ],
                'stage':
                'cdk_bootstrap_tst'
            }
        },
    )
