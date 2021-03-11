import warnings
from typing import Dict, Optional

from gcip.core.job import Job

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


def bootstrap(*args: None, aws_account_id: str, aws_region: str, toolkit_stack_name: str, qualifier: str, **tags: str) -> Job:
    """
    Test
    """
    return Job(
        namespace="cdk_bootstrap",
        script="cdk bootstrap"
        f" --toolkit-stack-name {toolkit_stack_name}"
        f" --qualifier {qualifier}"
        f" aws://{aws_account_id}/{aws_region}" +
        " ".join([""] + list(map(lambda keyvalue: f"-t {keyvalue[0]}={keyvalue[1]}", tags.items()))),
    ).add_variables(CDK_NEW_BOOTSTRAP="1")


def _context_options(context_dict: Dict[str, str]) -> str:
    if not context_dict:
        return ""
    return " ".join(f"-c {key}={value}" for key, value in context_dict.items()) + " "


def _space(string: str) -> str:
    if string:
        return f"{string} "
    return ""


def diff(*stacks: str, synth_options: str = "", diff_options: str = "", **context: str) -> Job:
    stacks_string = " ".join(stacks)
    return Job(
        name="cdk",
        namespace="diff",
        script=[
            f"cdk synth {_space(synth_options)}{stacks_string}",
            f"cdk diff {_space(diff_options)}{_context_options(context)}{stacks_string}",
        ],
    )


def deploy(
    *stacks: str,
    toolkit_stack_name: str,
    wait_for_stack: bool = True,
    wait_for_stack_assume_role: Optional[str] = None,
    wait_for_stack_account_id: Optional[str] = None,
    options: str = "",
    **context: str,
) -> Job:
    stacks_string = " ".join(stacks)

    job = Job(
        name="cdk",
        namespace="deploy",
        script=[
            f"cdk deploy --strict --require-approval 'never' {_space(options)}"
            f"--toolkit-stack-name {toolkit_stack_name} {_context_options(context)}{stacks_string}",
        ],
    )

    if wait_for_stack:
        wait_for_stack_options = ""
        if wait_for_stack_assume_role:
            wait_for_stack_options += f" --assume-role {wait_for_stack_assume_role}"
            if wait_for_stack_account_id:
                wait_for_stack_options += f" --assume-role-account-id {wait_for_stack_account_id}"
        elif wait_for_stack_account_id:
            warnings.warn("`wait_for_stack_account_id` has no effects without `wait_for_stack_assume_role`")

        job.prepend_scripts(
            "pip3 install gcip",
            f"python3 -m gcip.addons.cdk.tools.wait_for_cloudformation_stack_ready --stack-names '{stacks_string}'{wait_for_stack_options}",
        )

    return job
