import os

import boto3  # type: ignore

sts = boto3.Session().client("sts")


def aws_account_id() -> str:
    """
    Returns the AWS account id.

    Account ID is resolved in following precedence:
    1. OS environment variable `AWS_ACCOUNT_ID`
    2. From response of `sts.get_caller_identity()` function call with an initialized `boto3.client`

    Returns:
        str: AWS account id.
    """
    if os.environ.get("AWS_ACCOUNT_ID"):
        return os.environ["AWS_ACCOUNT_ID"]

    return str(sts.get_caller_identity()["Account"])


def aws_region() -> str:
    """
    Returns the AWS region.

    AWS region is resolved in following precedence:
    1. OS environment variable `AWS_DEFAULT_REGION`
    2. From response of `sts.meta.region_name` function call with an initialized `boto3.client`

    Raises:
        ValueError: If neither environment variable nor `client.meta.region_name` is resolvable

    Returns:
        str: AWS region name.
    """
    if os.environ.get("AWS_DEFAULT_REGION"):
        return os.environ["AWS_DEFAULT_REGION"]
    elif sts.meta.region_name:
        return str(sts.meta.region_name)

    raise ValueError(
        "No resolution to AWS region, neither from API call nor from environment Variable. "
        "Please set `AWS_DEFAULT_REGION` environment variable to a aws region."
    )
