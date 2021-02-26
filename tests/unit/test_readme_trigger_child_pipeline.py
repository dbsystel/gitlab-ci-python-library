from gcip import (
    Pipeline,
    TriggerJob,
    IncludeLocal,
    TriggerStrategy,
)
from tests import conftest


def test():
    pipeline = Pipeline()
    pipeline.add_children(
        TriggerJob(
            namespace="trigger-subpipe",
            includes=IncludeLocal("./my-subpipe.yml"),
            strategy=TriggerStrategy.DEPEND,
        )
    )

    conftest.check(pipeline.render())
