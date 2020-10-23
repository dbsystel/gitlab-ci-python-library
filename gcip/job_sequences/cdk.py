from typing import Any

from ..jobs import cdk
from .._core.job_sequence import JobSequence

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


def diff_deploy(
    *args: Any,
    stack: str,
    toolkit_stack_name: str,
) -> JobSequence:
    sequence = JobSequence()
    sequence.add_jobs(
        cdk.diff(stack),
        cdk.deploy(stack, toolkit_stack_name),
    )
    return sequence
