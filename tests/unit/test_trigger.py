import pytest

from gcip import (
    Rule,
    Pipeline,
    TriggerJob,
    IncludeLocal,
    TriggerStrategy,
)
from tests import conftest


def test_include_methods():
    test_dict = {}
    for member, value in TriggerStrategy.__members__.items():
        test_dict.update({member: value.value})
    assert {
        "DEPEND": "depend",
    } == test_dict


def test_include_exceptions():
    with pytest.raises(ValueError):
        assert TriggerJob(stage="foobar", project="please/raise/execption", includes=[IncludeLocal("TestConfig.yml")])
        assert TriggerJob(stage="foobar", branch="Missing/Project")
        assert TriggerJob(stage="foobar", includes=[IncludeLocal(f"Localfile_{i}.yml") for i in range(4)])


def test_parent_child_trigger():
    conftest.check(TriggerJob(stage="trigger-child", includes=[IncludeLocal("Test-File.yml")]).render())


def test_multi_project_trigger():
    conftest.check(
        TriggerJob(
            stage="trigger-project",
            project="my/project",
            branch="staging",
            strategy=TriggerStrategy.DEPEND,
        ).render()
    )


def test_trigger_job_keywords():
    trigger_job = TriggerJob(stage="foobar", project="my/project")

    # add supported keywords
    trigger_job.add_variables(USER="Max Power", URL="https://example.com")
    trigger_job.append_rules(Rule(if_statement="$MY_VARIABLE_IS_PRESENT"))

    # add unsupported keywords
    trigger_job.set_image("docker/image:example")
    trigger_job.prepend_scripts("./before-script.sh")
    trigger_job.append_scripts("./after-script.sh")
    trigger_job.add_tags("test", "europe")
    trigger_job.add_artifacts_paths("binaries/", ".config")

    pipeline = Pipeline()
    pipeline.add_children(trigger_job)
    conftest.check(pipeline.render())
