import pytest

from gcip import TriggerJob, TriggerStrategy
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
