import pytest

from gcip import Pipeline
from tests import conftest
from gcip.jobs import cdk


def test_bootstrap() -> None:
    pipeline = Pipeline()
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


def test_diff_deploy_with_context() -> None:
    pipeline = Pipeline()
    pipeline.add_jobs(
        cdk.diff("teststack", foo="bar", abra="kadabra"),
        cdk.deploy("teststack", toolkit_stack_name="CDKToolkit", foo="bar", abra="kadabra"),
    )

    conftest.check(pipeline.render())


def test_deploy_with_assume_role() -> None:
    pipeline = Pipeline()
    pipeline.add_jobs(
        cdk.deploy(
            "teststack",
            toolkit_stack_name="CDKToolkit",
            wait_for_stack_assume_role="MasterOfDesaster",
        ),
        namespace="local-role",
    )
    pipeline.add_jobs(
        cdk.deploy(
            "teststack",
            toolkit_stack_name="CDKToolkit",
            wait_for_stack_assume_role="MasterOfDesaster",
            wait_for_stack_account_id="1234567890",
        ),
        namespace="remote-role",
    )
    conftest.check(pipeline.render())


def test_assume_role_warning() -> None:
    with pytest.warns(UserWarning, match="`wait_for_stack_account_id` has no effects without `wait_for_stack_assume_role`"):
        cdk.deploy("teststack", toolkit_stack_name="CDKToolkit", wait_for_stack_account_id="MasterOfDesaster")
