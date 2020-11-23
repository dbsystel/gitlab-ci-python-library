from .._core.job import Job

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


def bootstrap(*args: None, aws_account_id: str, aws_region: str, qualifier: str, **tags: str) -> Job:
    return Job(
        namespace="cdk_bootstrap",
        script="cdk bootstrap"
        f" --qualifier {qualifier}"
        f" aws://{aws_account_id}/{aws_region}" +
        " ".join([""] + list(map(lambda keyvalue: f"-t {keyvalue[0]}={keyvalue[1]}", tags.items()))),
    ).add_variables(CDK_NEW_BOOTSTRAP="1")


def diff(*stacks: str) -> Job:
    stacks_string = " ".join(stacks)
    return Job(
        name="cdk",
        namespace="diff",
        script=[
            f"cdk synth {stacks_string}",
            f"cdk diff {stacks_string}",
        ],
    )


def deploy(*stacks: str) -> Job:
    stacks_string = " ".join(stacks)
    return Job(
        name="cdk",
        namespace="deploy",
        script=[
            "pip3 install --upgrade gcip",
            f"python3 -m gcip.script_library.wait_for_cloudformation_stack_ready --stack-names '{stacks_string}'",
            f"cdk deploy --strict --require-approval 'never' {stacks_string}",
        ],
    )
