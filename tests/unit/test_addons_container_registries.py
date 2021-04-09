from typing import get_args

import pytest

from gcip.addons.container.registries import Registry


@pytest.mark.parametrize(
    "registry,expected_url",
    [
        ("DOCKER", "https://index.docker.io/v1/"),
        ("GCR", "gcr.io"),
        ("QUAY", "quay.io"),
    ]
)
def test_registries(registry, expected_url):
    getattr(Registry, registry) == expected_url
