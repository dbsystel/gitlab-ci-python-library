import pytest

from gcip import Trigger, TriggerStrategy
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
        assert Trigger(project="please/raise/execption", includes=[LocalInclude("TestConfig.yml")])
        assert Trigger(branch="Missing/Project")
        assert Trigger(includes=[LocalInclude(f"Localfile_{i}.yml") for i in range(4)])


def test_parent_child_trigger():
    conftest.check(Trigger(includes=[LocalInclude("Test-File.yml")]).render())


def test_multi_project_trigger():
    conftest.check(Trigger(
        project="my/project",
        branch="staging",
        strategy=TriggerStrategy.DEPEND,
    ).render())
