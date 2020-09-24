import argparse
from time import sleep

import boto3

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "--stack-name", dest="stack_name", help="The name of the stack to wait all CloudFormation operations are finished for."
)
argparser.add_argument(
    "--wait-seconds",
    type=int,
    default=30,
    dest="wait_seconds",
    help="The number of seconds to wait before checking stack status again. Default=30"
)
args = argparser.parse_args()

cfn = boto3.client('cloudformation')

if __name__ == "__main__":
    while "IN_PROGRESS" not in cfn.describe_stacks(StackName=args.stack_name)["Stacks"][0]["StackStatus"]:
        print(f"Stack {args.stack_name} status is in progress. Waiting...")
        sleep(args.wait_seconds)
