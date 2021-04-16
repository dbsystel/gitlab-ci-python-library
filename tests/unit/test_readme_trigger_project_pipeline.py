from gcip import Pipeline, TriggerJob, TriggerStrategy
from tests import conftest


def test():
    pipeline = Pipeline()
    pipeline.add_children(
        TriggerJob(
            stage="trigger-banana",
            project="myteam/banana",
            branch="test",
            strategy=TriggerStrategy.DEPEND,
        )
    )

    conftest.check(pipeline.render())
