import os
import re

__author__ = "Daniel von Eßen"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


def is_semver(version: str) -> bool:
    """
    Checks if `version` is semver compliant.

    :param version: Version number to check for compliance.
    :type version: str
    :return: True if `version` is semver compliant, otherwise false.
    :rtype: bool
    """
    return (
        re.match(
            (
                r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
                r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
                r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
            ),
            version,
        )
        is not None
    )


if __name__ == "__main__":
    ci_commit_tag = os.getenv("CI_COMMIT_TAG")

    if ci_commit_tag is None:
        raise ValueError("Environment variable CI_COMMIT_TAG must be set.")

    if not is_semver(ci_commit_tag):
        raise ValueError(f"'{ci_commit_tag}' is not a valid Semver version. https://semver.org/")
