__author__ = "Daniel von Eßen"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Daniel von Eßen", "Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "daniel.von-essen@deutschebahn.com"


def sops_export_decrypted_values(path: str) -> str:
    """Returns a helper string to embedd it into jobs to allow exporting
    Values which are decrypted by `sops`. e.g. 'export $(sops -d sops/encrypted_file.env)'

    This function is usefull, if you want to use environment variables to login to e.g. a container registry.

    Args:
        path (str): Path to `sops` encrypted file, must be relative to project directory.

    Returns:
        str: Export string of sops decrypted file.
    """
    return f"set -eo pipefail; SOPS_OUTPUT=$(sops -d {path}); export $SOPS_OUTPUT"
