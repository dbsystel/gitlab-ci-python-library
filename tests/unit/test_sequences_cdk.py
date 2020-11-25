from gcip import Pipeline
from tests import conftest
from gcip.job_sequences import cdk


def test_diff_deploy_multiple_stacks() -> None:
    pipeline = Pipeline()
    pipeline.add_sequences(cdk.diff_deploy("stack1", "stack2", toolkit_stack_name="toolkit-stack"))
    conftest.check(pipeline.render())
