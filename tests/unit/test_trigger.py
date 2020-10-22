import pytest

from gcip import Rule, Pipeline, TriggerJob, TriggerStrategy
from tests import conftest
from gcip.includes.include_pattern import LocalInclude


def test_include_methods():
    test_dict = {}
    for member, value in TriggerStrategy.__members__.items():
        test_dict.update({member: value.value})
    assert {
        "DEPEND": "depend",
    } == test_dict


def test_include_exceptions():
    with pytest.raises(ValueError):
        assert TriggerJob(namespace="foobar", project="please/raise/execption", includes=[LocalInclude("TestConfig.yml")])
        assert TriggerJob(namespace="foobar", branch="Missing/Project")
        assert TriggerJob(namespace="foobar", includes=[LocalInclude(f"Localfile_{i}.yml") for i in range(4)])


def test_parent_child_trigger():
    conftest.check(TriggerJob(namespace="trigger-child", includes=[LocalInclude("Test-File.yml")]).render())


def test_multi_project_trigger():
    conftest.check(
        TriggerJob(
            namespace="trigger-project",
            project="my/project",
            branch="staging",
            strategy=TriggerStrategy.DEPEND,
        ).render()
    )


def test_trigger_job_keywords():
    trigger_job = TriggerJob(namespace="foobar", project="my/project")

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
    pipeline.add_jobs(trigger_job)
    conftest.check(pipeline.render())
