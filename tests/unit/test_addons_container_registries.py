import pytest

from gcip.addons.container.registries import Registry


@pytest.mark.parametrize(
    "registry,expected_url",
    [
        ("DOCKER", "https://index.docker.io/v1/"),
        ("GCR", "gcr.io"),
        ("QUAY", "quay.io"),
    ],
)
def test_registries(registry, expected_url):
    getattr(Registry, registry) == expected_url


def test_aws_registry(mocker, monkeypatch):
    monkeypatch.setenv("AWS_ACCOUNT_ID", "123456789012")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-central-1")
    mocker.patch("gcip.addons.aws.helper.aws_region", return_value="eu-central-1")
    mocker.patch("gcip.addons.aws.helper.aws_account_id", return_value="123456789012")
    aws_registry = Registry.AWS()
    assert "123456789012.dkr.ecr.eu-central-1.amazonaws.com" == aws_registry
