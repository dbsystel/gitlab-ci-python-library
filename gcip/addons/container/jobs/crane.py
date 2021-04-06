from typing import Union, Optional

from gcip.core.job import Job
from gcip.core.image import Image
from gcip.addons.container.config import DockerClientConfig
from gcip.addons.container.images import PredefinedImages


def copy(
    src: str,
    dst: str,
    *,
    docker_client_config: Optional[DockerClientConfig] = None,
    crane_image: Optional[Union[Image, str]] = None,
) -> Job:
    """
    Creates a job to copy container images with `crane`.
    See [`crane`](https://github.com/google/go-containerregistry/tree/main/cmd/crane)

    Copying an image is usfull, if you want to have container images as close as possible
    to your cluster or servers.

    Args:
        src (str): Registry URL to copy container image from.
        dst (str): Registry URL to copy container image to.
        docker_client_config (Optional[DockerClientConfig], optional): Creates the Docker configuration file base on objects settings,
            used by crane to authenticate against given registries. Defaults to None.
        crane_image (Optional[Union[Image, str]], optional): Container image which contains `crane` command.
            Defaults to PredefindedImages.CRANE.

    Returns:
        Job: Returns a `gcip.Job`, with neccessary configuration to copy a container image between images.
    """
    if not crane_image:
        crane_image = PredefinedImages.CRANE

    job = Job(
        script=[
            f"crane validate --remote {src}",
            f"crane copy {src} {dst}",
        ],
        namespace="push_container_image",
    )
    job.set_image(crane_image)

    if docker_client_config:
        job.prepend_scripts(*docker_client_config.get_shell_command())

    return job
