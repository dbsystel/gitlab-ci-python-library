from botocore.stub import Stubber

from gcip.addons.aws.helper import (
    sts,
    aws_region,
    aws_account_id,
)


def test_aws_account_id_with_sts_client():
    # Test if sts.get_caller_identity works
    with Stubber(sts) as stub:
        stub.add_response(
            "get_caller_identity",
            service_response={"Account": "123456789012"},
        )
        assert aws_account_id() == "123456789012"


def test_aws_account_id_with_env_var(monkeypatch):
    # Test AWS_ACCOUNT_ID environment variable
    monkeypatch.setenv("AWS_ACCOUNT_ID", "123456789012")
    assert aws_account_id() == "123456789012"


def test_aws_region_with_env_var(monkeypatch):
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-central-1")
    assert aws_region() == "eu-central-1"
