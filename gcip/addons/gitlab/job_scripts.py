from typing import Any

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


def clone_repository(path: str, *args: Any, branch: str = "main") -> str:
    if not path.startswith("/"):
        path = "/" + path
    return f"git clone --branch {branch} --single-branch https://gitlab-ci-token:${{CI_JOB_TOKEN}}@${{CI_SERVER_HOST}}{path}.git"
