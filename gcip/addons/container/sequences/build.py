__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Daniel von Eßen"
__email__ = "daniel.von-essen@deutschebahn.com"

from typing import Any, Dict, Union, Optional

from gcip.core.cache import Cache
from gcip.core.sequence import Sequence
from gcip.addons.container.jobs import (
    dive,
    crane,
    trivy,
    kaniko,
)
from gcip.addons.container.config import DockerClientConfig
from gcip.addons.container.registries import Registry


def build_scan_push_image(
    *,
    registry: Union[Registry, str] = Registry.DOCKER,
    image_name: Optional[str] = None,
    image_tag: Optional[str] = None,
    kaniko_kwargs: Dict[str, Any] = {},
    dive_kwargs: Dict[str, Any] = {},
    trivy_kwargs: Dict[str, Any] = {},
    crane_kwargs: Dict[str, Any] = {},
    docker_client_config: Optional[DockerClientConfig] = None,
) -> Sequence:
    """
    Creates a `gcip.Sequence` to build, scan and push a container image.

    The build step is executed by `gcip.addons.container.jobs.kaniko.execute`, it will build the container image an outputs it to a tarball.
    There are two scan's, optimization scan with `gcip.addons.container.jobs.dive.scan_local_image` to scan storage wasting in container image
    and a vulnerability scan with `gcip.addons.container.jobs.trivy.scan`. Both outputs are uploaded as an artifact to the GitLab instance.
    Built container image is uploaded with `gcip.addons.container.jobs.crane.push`.

    Args:
        registry (Union[Registry, str], optional): Container registry to push the image to. If the container registry needs authentication,
            you have to provide a `gcip.addons.container.config.DockerClientConfig` object with credentials. Defaults to Registry.DOCKER.
        image_name (Optional[str]): Image name with stage in the registry. e.g. username/image_name.
            Defaults to `gcip.core.variables.PredefinedVariables.CI_PROJECT_NAME`.
        image_tag (Optional[str]): Image tag. The default is either `PredefinedVariables.CI_COMMIT_TAG` or
            `PredefinedVariables.CI_COMMIT_REF_SLUG` depending of building from a git tag or from a branch.
        kaniko_kwargs (Dict[str, Any]): Extra keyword arguaments passed to `gcip.addons.container.jobs.kaniko.execute`. Defaults to {}.
        dive_kwargs (Dict[str, Any], optional): Extra keyword arguaments passed to `gcip.addons.container.jobs.dive.scan`. Defaults to {}.
        trivy_kwargs (Dict[str, Any], optional): Extra keyword arguaments passed to `gcip.addons.container.jobs.trivy.scan_local_image`. Defaults to {}.
        crane_kwargs (Dict[str, Any], optional): Extra keyword arguaments passed to `gcip.addons.container.jobs.push`. Defaults to {}.
        docker_client_config (Optional[DockerClientConfig], optional): Creates the Docker configuration file base on objects settings,
            to authenticate against given registries. Defaults to a `DockerClientConfig` with login to the official Docker Hub
            and expecting credentials given as environment variables `REGISTRY_USER` and `REGISTRY_LOGIN`.

    Returns:
        Sequence: `gcip.Sequence` to build, scan and push a container image.
    """
    cache = Cache(paths=["image"])
    kaniko_execute = kaniko.execute(
        image_name=image_name,
        image_tag=image_tag,
        registries=[registry],
        tar_path=cache.paths[0],
        docker_client_config=docker_client_config,
        **kaniko_kwargs,
    )
    kaniko_execute.set_cache(cache)
    dive_scan = dive.scan(
        image_path=cache.paths[0],
        image_name=image_name,
        **dive_kwargs,
    )
    dive_scan.set_cache(cache)
    trivy_scan = trivy.scan_local_image(
        image_path=cache.paths[0],
        image_name=image_name,
        **trivy_kwargs,
    )
    trivy_scan.set_cache(cache)
    crane_push = crane.push(
        dst_registry=registry,
        tar_path=cache.paths[0],
        image_name=image_name,
        docker_client_config=docker_client_config,
        **crane_kwargs,
    )
    crane_push.set_cache(cache)

    job_sequence = Sequence()
    job_sequence.add_children(kaniko_execute, name="kaniko")
    job_sequence.add_children(dive_scan, name="dive")
    job_sequence.add_children(trivy_scan, name="trivy")
    job_sequence.add_children(crane_push, name="crane")

    return job_sequence
