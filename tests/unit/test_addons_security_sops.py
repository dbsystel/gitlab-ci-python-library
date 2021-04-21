from gcip.addons.security.sops import (
    sops_export_decrypted_values,
)


def test_sops_export_decrypted_values():
    expected = "set -eo pipefail; SOPS_OUTPUT=$(sops -d secrets/encrypted_file.env); export $SOPS_OUTPUT"
    assert sops_export_decrypted_values("secrets/encrypted_file.env") == expected
