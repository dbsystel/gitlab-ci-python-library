import pytest

from gcip import Include, IncludeMethod
from tests import conftest
from gcip.includes.include_pattern import (
    FileInclude,
    LocalInclude,
    RemoteInclude,
    TemplateInclude,
)


def test_include_methods():
    test_dict = {}
    for member, value in IncludeMethod.__members__.items():
        test_dict.update({member: value.value})
    assert {
        "LOCAL": "local",
        "FILE": "project",
        "TEMPLATE": "template",
        "REMOTE": "remote",
    } == test_dict


def test_include_exceptions():
    with pytest.raises(TypeError):
        assert Include(file=["test"], include_method=IncludeMethod.FILE)
        assert Include(file="Gitlab-Ci.yaml", include_method="file")
    with pytest.raises(ValueError):
        assert Include(
            file="/test/gitlab-test.yaml",
            include_method=IncludeMethod.LOCAL,
            project="throw/exception",
        )
        assert Include(
            file="/test/gitlab-test.yaml",
            include_method=IncludeMethod.TEMPLATE,
            ref="missing/project",
        )
        assert Include(
            file="/test/gitlab-test.yaml",
            include_method=IncludeMethod.REMOTE,
            project="throw/exception",
            ref="added_exception",
        )
    with pytest.raises(AttributeError):
        assert Include(file="/test/gitlab-test.yaml", include_method=IncludeMethod.FILE)

    with pytest.raises(ValueError):
        assert Include(file="htp:/this.url/totaly/wrong", include_method=IncludeMethod.REMOTE)


def test_local_include():
    conftest.check(Include(
        file="/test/gitlab-test.yaml",
        include_method=IncludeMethod.LOCAL,
    ).render())


def test_remote_include():
    conftest.check(Include(
        file="https://test.example.com/gitlab-test.yaml",
        include_method=IncludeMethod.REMOTE,
    ).render())


def test_template_include():
    conftest.check(Include(
        file="Auto-DevOps.gitlab-ci.yml",
        include_method=IncludeMethod.TEMPLATE,
    ).render())


def test_file_include():
    conftest.check(
        Include(
            file="/test/gitlab-test.yaml",
            include_method=IncludeMethod.FILE,
            project="testgroup/testproject",
            ref="staging",
        ).render()
    )


def test_pattern_file_include():
    conftest.check(FileInclude(file="/test/file/gitlab.yml", project="test/project", ref="staging").render())


def test_pattern_remote_include():
    conftest.check(RemoteInclude(url="https://test.com/testfile.yml").render())


def test_pattern_template_include():
    conftest.check(TemplateInclude(file="Gitlab-Ci-Template.yml").render())


def test_pattern_local_include():
    conftest.check(LocalInclude(file="gitlab_local.yml").render())
