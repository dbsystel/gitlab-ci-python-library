from gcip import Pipeline, TriggerJob, TriggerStrategy
from tests import conftest
from gcip.includes.include_pattern import LocalInclude


def test():
    pipeline = Pipeline()
    pipeline.add_jobs(
        TriggerJob(
            namespace="trigger-subpipe",
            includes=LocalInclude("./my-subpipe.yml"),
            strategy=TriggerStrategy.DEPEND,
        )
    )

    conftest.check(pipeline.render())
