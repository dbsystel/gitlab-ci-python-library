from typing import Optional

from gcip.core.job_sequence import JobSequence

from . import jobs as cdk

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


def diff_deploy(
    *stacks: str,
    toolkit_stack_name: str,
    wait_for_stack: bool = True,
    wait_for_stack_assume_role: Optional[str] = None,
    wait_for_stack_account_id: Optional[str] = None,
    synth_options: str = "",
    diff_options: str = "",
    deploy_options: str = "",
    **context: str,
) -> JobSequence:
    sequence = JobSequence()
    diff_job = cdk.diff(*stacks, synth_options=synth_options, diff_options=diff_options, **context)
    sequence.add_children(
        diff_job,
        cdk.deploy(
            *stacks,
            toolkit_stack_name=toolkit_stack_name,
            wait_for_stack=wait_for_stack,
            wait_for_stack_assume_role=wait_for_stack_assume_role,
            wait_for_stack_account_id=wait_for_stack_account_id,
            options=deploy_options,
            **context,
        ).add_needs(diff_job),
    )
    return sequence
