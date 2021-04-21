import argparse
from time import sleep

import boto3  # type: ignore
from botocore.config import Config  # type: ignore

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--stack-names",
        dest="stack_names",
        help="The names of the stacks to wait all CloudFormation operations are finished for, separated by blanks.",
    )
    argparser.add_argument(
        "--wait-seconds",
        type=int,
        default=30,
        dest="wait_seconds",
        help="The number of seconds to wait before checking stack status again. Default=30",
    )
    argparser.add_argument(
        "--assume-role",
        dest="assume_role",
        help="The IAM role to execute this script with.",
    )
    argparser.add_argument(
        "--assume-role-account-id",
        dest="assume_role_account_id",
        help="The account Id the `--assume-role` resides in.",
    )
    args = argparser.parse_args()

    config = Config(retries={"max_attempts": 15, "mode": "standard"})

    if args.assume_role:
        assume_role_account_id = args.assume_role_account_id
        if not assume_role_account_id:
            assume_role_account_id = boto3.client("sts").get_caller_identity().get("Account")

        sts_client = boto3.client("sts")
        assumed_role_object = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{assume_role_account_id}:role/{args.assume_role}",
            RoleSessionName="AssumeRoleSession1",
        )
        credentials = assumed_role_object["Credentials"]
        session = boto3.session.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
        cfn = session.client("cloudformation", config=config)
    else:
        cfn = boto3.client("cloudformation", config=config)

    # everything but DELETE_COMPLETE
    stack_status_filter = [
        "CREATE_IN_PROGRESS",
        "CREATE_FAILED",
        "CREATE_COMPLETE",
        "ROLLBACK_IN_PROGRESS",
        "ROLLBACK_FAILED",
        "ROLLBACK_COMPLETE",
        "DELETE_IN_PROGRESS",
        "DELETE_FAILED",
        "UPDATE_IN_PROGRESS",
        "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS",
        "UPDATE_COMPLETE",
        "UPDATE_ROLLBACK_IN_PROGRESS",
        "UPDATE_ROLLBACK_FAILED",
        "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS",
        "UPDATE_ROLLBACK_COMPLETE",
        "REVIEW_IN_PROGRESS",
        "IMPORT_IN_PROGRESS",
        "IMPORT_COMPLETE",
        "IMPORT_ROLLBACK_IN_PROGRESS",
        "IMPORT_ROLLBACK_FAILED",
        "IMPORT_ROLLBACK_COMPLETE",
    ]

    stacks = []
    for stack_id in args.stack_names.split(" "):
        if "*" in stack_id:
            stack_name = stack_id.replace("*", "")
            for ppage in cfn.get_paginator("list_stacks").paginate(StackStatusFilter=stack_status_filter):
                for stack in ppage.get("StackSummaries"):
                    if stack_name in stack["StackName"]:
                        stacks.append(stack["StackName"])
        else:
            for ppage in cfn.get_paginator("list_stacks").paginate(StackStatusFilter=stack_status_filter):
                for stack in ppage.get("StackSummaries"):
                    if stack_id == stack["StackName"]:
                        stacks.append(stack_id)

    print(f"waiting for stacks to complete: {stacks}")

    def stack_in_progress() -> bool:
        for stack in stacks:
            sleep(0.5)  # prevent API rate limiting when iterating through many stacks
            if "IN_PROGRESS" in cfn.describe_stacks(StackName=stack)["Stacks"][0]["StackStatus"]:
                return True
        return False

    while stack_in_progress():
        print(f"One of the stacks {stacks} status is in progress. Waiting...", flush=True)
        sleep(args.wait_seconds)
