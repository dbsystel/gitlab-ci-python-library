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
            qualifier="beautifulapp",
        ),
        namespace="dev"
    )
    pipeline.add_jobs(
        cdk.bootstrap(
            aws_account_id="1234567890",
            aws_region="net-wunderland-1",
            toolkit_stack_name="my-cdk-toolkit-tst",
            qualifier="beautifulapp",
            ApplicationName="testapp",
            Subsystem="testsystem",
        ),
        namespace="tst"
    )

    conftest.check(pipeline.render())
