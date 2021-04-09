from typing import Union, Optional

from gcip.core.job import Job
from gcip.core.image import Image
from gcip.core.variables import PredefinedVariables
from gcip.addons.container.images import PredefinedImages


def scan_local_image(
    *,
    image_path: Optional[str] = None,
    image_name: Optional[str] = None,
    output_format: Optional[str] = None,
    severity: Optional[str] = None,
    vulnerability_types: Optional[str] = None,
    exit_if_vulnerable: bool = True,
    trivy_config: Optional[str] = None,
    trivy_image: Optional[Union[Image, str]] = None,
) -> Job:
    """This job scanns container images to find vulnerabilities.

    This job fails with exit code 1 if severities are found.
    The scan output is printed to stdout and uploaded to the artifacts of GitLab.


    Args:
        image_path (Optional[str]): Path where to find the container image.
            If `None` it defaults internally to `PredefinedVariables.CI_PROJECT_DIR`. Defaults to None.
        image_name (Optional[str]): Container image name, searched for in `image_path` and gets `.tar` appended.
            If `None` it defaults internally to `PredefinedVariables.CI_PROJECT_NAME`. Defaults to None.
        output_format (Optional[str]): Scan output format, possible values (table, json). Internal default `table`.
            Defaults to None.
        severity (Optional[str]): Severities of vulnerabilities to be displayed (comma separated).
            Defaults internally to "UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL". Defaults to None.
        vulnerability_types (Optional[str]): List of vulnerability types (comma separated).
            Defaults internally to "os,library". Defaults to None.
        exit_if_vulnerable (bool): Exit code when vulnerabilities were found. If true exit code is 1 else 0. Defaults to True.
        trivy_config (Optional[str]): Additional options to pass to `trivy` binary. Defaults to None.
        trivy_image (Optional[Union[Image, str]]): Container image which contains `trivy` command.
            Defaults to PredefindedImages.TRIVY.

    Returns:
        Job: `gcip.Job` will be returned to create container images with ```namespace=check_container_image```.
    """
    if not image_path:
        image_path = PredefinedVariables.CI_PROJECT_DIR
    if not image_name:
        image_name = PredefinedVariables.CI_PROJECT_NAME
    if not trivy_image:
        trivy_image = PredefinedImages.TRIVY

    trivy_cmd = ["trivy image"]
    trivy_cmd.append(f"--input {image_path}/{image_name}.tar")
    trivy_cmd.append(f"--output {PredefinedVariables.CI_PROJECT_DIR}/trivi.txt")
    trivy_cmd.append("--no-progress")

    if output_format:
        trivy_cmd.append(f"--format {output_format}")

    if severity:
        trivy_cmd.append(f"--severity {severity}")

    if vulnerability_types:
        trivy_cmd.append(f"--vuln-type {vulnerability_types}")

    if exit_if_vulnerable:
        trivy_cmd.append("--exit-code 1")

    if trivy_config:
        trivy_cmd.append(trivy_config)

    job = Job(script=" ".join(trivy_cmd), namespace="check_container_image")
    job.append_scripts(f"cat {PredefinedVariables.CI_PROJECT_DIR}/trivi.txt")
    job.set_image(trivy_image)
    job.add_artifacts_paths("trivi.txt")
    return job
