import argparse
from time import sleep

import boto3

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--stack-name",
        dest="stack_name",
        help="The name of the stack to wait all CloudFormation operations are finished for.",
    )
    argparser.add_argument(
        "--wait-seconds",
        type=int,
        default=30,
        dest="wait_seconds",
        help="The number of seconds to wait before checking stack status again. Default=30",
    )
    args = argparser.parse_args()

    cfn = boto3.client('cloudformation')

    # everything but DELETE_COMPLETE
    stack_status_filter = [
        'CREATE_IN_PROGRESS',
        'CREATE_FAILED',
        'CREATE_COMPLETE',
        'ROLLBACK_IN_PROGRESS',
        'ROLLBACK_FAILED',
        'ROLLBACK_COMPLETE',
        'DELETE_IN_PROGRESS',
        'DELETE_FAILED',
        'UPDATE_IN_PROGRESS',
        'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
        'UPDATE_COMPLETE',
        'UPDATE_ROLLBACK_IN_PROGRESS',
        'UPDATE_ROLLBACK_FAILED',
        'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS',
        'UPDATE_ROLLBACK_COMPLETE',
        'REVIEW_IN_PROGRESS',
        'IMPORT_IN_PROGRESS',
        'IMPORT_COMPLETE',
        'IMPORT_ROLLBACK_IN_PROGRESS',
        'IMPORT_ROLLBACK_FAILED',
        'IMPORT_ROLLBACK_COMPLETE',
    ]

    stacks = []
    if "*" in args.stack_name:
        stack_name = args.stack_name.replace("*", "")
        for ppage in cfn.get_paginator("list_stacks").paginate(StackStatusFilter=stack_status_filter):
            for stack in ppage.get("StackSummaries"):
                if stack_name in stack["StackName"]:
                    stacks.append(stack["StackName"])
    else:
        stacks.append(args.stack_name)

    print(f"waiting for to complete: {stacks}")

    def stack_in_progress() -> bool:
        for stack in stacks:
            if "IN_PROGRESS" in cfn.describe_stacks(StackName=stack)["Stacks"][0]["StackStatus"]:
                return True
        return False

    while stack_in_progress():
        print(f"One of the stacks {stacks} status is in progress. Waiting...", flush=True)
        sleep(args.wait_seconds)
