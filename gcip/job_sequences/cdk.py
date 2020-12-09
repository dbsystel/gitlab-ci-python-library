from ..jobs import cdk
from .._core.job_sequence import JobSequence

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


def diff_deploy(*stacks: str, toolkit_stack_name: str, **context: str) -> JobSequence:
    sequence = JobSequence()
    diff_job = cdk.diff(*stacks, **context)
    sequence.add_jobs(
        diff_job,
        cdk.deploy(*stacks, toolkit_stack_name=toolkit_stack_name, **context).add_needs(diff_job),
    )
    return sequence
