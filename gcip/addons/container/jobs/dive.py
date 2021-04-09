__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Daniel von Eßen"
__email__ = "daniel.von-essen@deutschebahn.com"

from typing import List, Optional

from gcip.core.job import Job
from gcip.core.image import Image
from gcip.core.variables import PredefinedVariables
from gcip.addons.container.images import PredefinedImages


def _is_float_between_zero_and_one(validate: float) -> bool:
    """
    Helper function to validate given arguments type and range.

    If `validate` is not of type float or not between 0.0 and 1.0 function returns `False`.
            Otherwise function returns `True`
    Args:
        validate (float): Argument to validate.

    Returns:
        bool:
    """

    if not isinstance(validate, float):
        raise TypeError("Argument is not of type float.")
    if not 0 <= validate <= 1:
        raise ValueError("Argument is not between 0.0 and 1.0.")
    return True


def scan(
    *,
    dive_image: Optional[Image] = None,
    image_path: Optional[str] = None,
    image_name: Optional[str] = None,
    highest_user_wasted_percent: Optional[float] = None,
    highest_wasted_bytes: Optional[float] = None,
    lowest_efficiency: Optional[float] = None,
    ignore_errors: bool = False,
    source: str = "docker-archive",
) -> Job:
    """
    Scan your images with [wagoodman/dive](https://github.com/wagoodman/dive).

    `dive` will scan your container image layers and will output the efficency of each layer.
    You can see which layer and which file is consuming the most storage and optimize the layers if possible.
    It prevents container images and its layers beeing polluted with files like apt or yum cache's.

    Args:
        dive_image (Image): Container Image used for this job. This image has to contain the `dive` command available.
            Defaults to `PredefinedImages.DIVE` image.
        image_path (Optional[str]): Path to the image can be either a remote container registry,
            as well as a local path to an image. Defaults to `PredefinedVariables.CI_PROJECT_PATH`.
        image_name (Optional[str]): Name of the container image to scan, if `source` is `docker-archive` argument gets prefix `.tar`.
            Defaults to PredefinedVariables.CI_PROJECT_NAME.
        highest_user_wasted_percent (Optional[float]): Highest allowable percentage of bytes wasted
            (as a ratio between 0-1), otherwise CI validation will fail. (default "0.1"). Defaults to None.
        highest_wasted_bytes (Optional[float]): Highest allowable bytes wasted, otherwise CI validation will fail.
            (default "disabled"). Defaults to None.
        lowest_efficiency (Optional[float]): Lowest allowable image efficiency (as a ratio between 0-1),
            otherwise CI validation will fail. (default "0.9"). Defaults to None.
        ignore_errors (Optional[bool]): Ignore image parsing errors and run the analysis anyway. Defaults to False.
        source (Optional[str]): The container engine to fetch the image from. Allowed values: docker, podman, docker-archive
            (default "docker"). Defaults to "docker-archive".

    Returns:
        Job: gcip.Job returned which will scan your image(s).
    """
    if not dive_image:
        dive_image = PredefinedImages.DIVE
    if not image_path:
        image_path = "/" + PredefinedVariables.CI_PROJECT_PATH
    if image_path and image_path.endswith("/"):
        image_path = image_path[:-1]

    if not image_name:
        image_name = PredefinedVariables.CI_PROJECT_NAME

    if source == "docker-archive":
        image_name = f"{image_name}.tar"

    dive_command: List[str] = ["dive", f"{source}://{image_path}/{image_name}", "--ci"]

    if highest_user_wasted_percent and _is_float_between_zero_and_one(highest_user_wasted_percent):
        dive_command.append(f'--highestUserWastedPercent "{highest_user_wasted_percent}"')
    if highest_wasted_bytes and _is_float_between_zero_and_one(highest_wasted_bytes):
        dive_command.append(f'--highestWastedBytes "{highest_wasted_bytes}"')
    if lowest_efficiency and _is_float_between_zero_and_one(lowest_efficiency):
        dive_command.append(f'--lowestEfficiency "{lowest_efficiency}"')
    if ignore_errors:
        dive_command.append("--ignore-errors")

    job = Job(script=["date", " ".join(dive_command)], namespace="check_container_image")
    job.set_image(dive_image)
    return job
