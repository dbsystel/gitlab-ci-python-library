from gcip import Pipeline
from tests import conftest
from gcip.addons.cdk import sequences as cdk


def test_diff_deploy_multiple_stacks() -> None:
    pipeline = Pipeline()
    pipeline.add_children(cdk.diff_deploy("stack1", "stack2", toolkit_stack_name="toolkit-stack"))
    conftest.check(pipeline.render())


def test_diff_deploy_with_context() -> None:
    pipeline = Pipeline()
    pipeline.add_children(cdk.diff_deploy("teststack", toolkit_stack_name="toolkit-stack", foo="bar", abra="kadabra"))
    conftest.check(pipeline.render())


def test_diff_deploy_with_options() -> None:
    pipeline = Pipeline()
    pipeline.add_children(
        cdk.diff_deploy("teststack", toolkit_stack_name="toolkit-stack", synth_options="-s", diff_options="-d", deploy_options="-e")
    )
    conftest.check(pipeline.render())
