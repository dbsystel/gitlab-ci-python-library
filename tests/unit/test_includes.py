from gcip import (
    IncludeFile,
    IncludeLocal,
    IncludeRemote,
    IncludeArtifact,
    IncludeTemplate,
)
from tests import conftest


def test_include_local():
    conftest.check(IncludeLocal("gitlab_local.yml").render())


def test_include_local_kwarg():
    conftest.check(IncludeLocal(local="gitlab_local.yml").render())


def test_include_file():
    conftest.check(IncludeFile(file="/test/file/gitlab.yml", project="test/project").render())


def test_include_file_with_ref():
    conftest.check(IncludeFile(file="/test/file/gitlab.yml", project="test/project", ref="staging").render())


def test_include_remote():
    conftest.check(IncludeRemote("https://test.com/testfile.yml").render())


def test_include_remote_kwarg():
    conftest.check(IncludeRemote(remote="https://test.com/testfile.yml").render())


def test_include_template():
    conftest.check(IncludeTemplate("Gitlab-Ci-Template.yml").render())


def test_include_template_kwarg():
    conftest.check(IncludeTemplate(template="Gitlab-Ci-Template.yml").render())


def test_include_artifact():
    conftest.check(IncludeArtifact(job="generator", artifact="pipeline.yml").render())
