from typing import Dict, List, Union, Optional

from gcip import Job, Image, PredefinedVariables

__author__ = "Daniel von Eßen"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Daniel von Eßen", "Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


def execute(
    gitlab_executor_image: Optional[Union[Image, str]] = Image("gcr.io/kaniko-project/executor:debug", entrypoint=[""]),
    context: Optional[str] = None,
    image_name: Optional[str] = None,
    image_tag: Optional[str] = None,
    registries: List[str] = list(),
    tar_path: Optional[str] = None,
    build_args: Dict[str, str] = {},
    build_target: str = None,
    dockerfile: Optional[str] = None,
    enable_push: bool = False,
    verbosity: Optional[str] = None,
    ecr_login: bool = False,
    dockerhub_user_env_var: Optional[str] = None,
    dockerhub_login_env_var: Optional[str] = None,
):
    """
    Creates a job which builds container images.

    This job creates images depending on their git branches.
    e.g If the branch which gets pushed to the remote is named
    `my_awsome_feature` the image

    Args:
        gitlab_executor_image (Optional[Union[Image, str]]): The Gitlab executor image this `gcip.core.job.Job` should run with.
            Must contain the kaniko ```executor``` binary. If set to `None`, no image will be set for this job.
            Defaults to ```gcr.io/kaniko-project/executor:latest```.
        context (Optional[str], optional): Context which will be send to kaniko. Defaults to `None` which implies the local
            directory is the context.
        image_name (Optional[str], optional): Image name which will be created. Defaults to PredefinedVariables.CI_PROJECT_NAME.
        image_tag (Optional[str]): The tag the image will be tagged with. Defaults to `PredefinedVariables.CI_COMMIT_REF_SLUG`.
        registries (Optional[List[str]], optional): List of container registries to push created image to. Defaults to an empty list.
        tar_path (Optional[str], optional): Container images created by kaniko are tarball files.
            This is the path where to store the image, will be named with suffix `.tar`. This path will be created if not present.
            Defaults to `None` which implies the image will be pushed to ```hub.docker.com```.
        build_args (Dict[str, str], optional): Container build arguments, used to instrument the container image build. Defaults to {}.
        build_target (Optional[str], optional): For container multistage builds name of the build stage you want to create.
            Image tag will be appended with the build_target. e.g. latest-buildtarget. Defaults to None.
        dockerfile (str, optional): Name of the dockerfile to use. File is relative to context. Defaults to "Dockerfile".
        enable_push (bool, optional): Enable push to container registry, disabled to allow subsequent jobs to act on container tarball.
            Defaults to False.
        verbosity (str, optional): Verbosity of kaniko logging. Defaults to "info".
        ecr_login (bool): If ```ecr-login``` should be registered as ```credStore``` in the ```.docker/config.json```.
            Mutually exclusive with `dockerhub_user_env_var` and `dockerhub_login_env_var`. Defaults to `False`.
        dockerhub_user_env_var (Optional[str]): If you have to login to the docker registry before the push, you have to provide
            the name of the environment variable, which contains the username value, here.
            **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
            Mutually exclusive with `ecr_login`.
            Defaults to `None` which skips the docker login attempt.
        dockerhub_login_env_var (Optional[str]): If you have to login to the docker registry before the push, you have to provide
            the name of the environment variable, which contains the password or token, here.
            **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
            Mutually exclusive with `ecr_login`.
            Defaults to `None` which skips the docker login attempt.

    Returns:
        Job: gcip.Job will be returned to create container images with ```name=kaniko``` and ```namespace=execute```.
    """

    if ecr_login and (dockerhub_user_env_var or dockerhub_login_env_var):
        raise ValueError("`ecr_login` is mutually exclusive with `dockerhub_user_env_var` and `dockerhub_login_env_var`.")

    job = Job(
        name="kaniko",
        namespace="execute",
        script="date",
    )

    if image_name is None:
        image_name = PredefinedVariables.CI_PROJECT_NAME

    if not image_tag:
        if PredefinedVariables.CI_COMMIT_TAG:
            image_tag = PredefinedVariables.CI_COMMIT_TAG
        elif PredefinedVariables.CI_COMMIT_REF_SLUG:
            image_tag = PredefinedVariables.CI_COMMIT_REF_SLUG

    image_tag_postfix = ""
    if image_tag:
        image_tag_postfix = f":{image_tag}"

    executor_cmd: List[str] = ["executor"]

    if not context and PredefinedVariables.CI_PROJECT_DIR:
        context = PredefinedVariables.CI_PROJECT_DIR

    if context:
        if context.endswith("/"):
            context = context[:-1]
        executor_cmd.append(f"--context {context}")

    if tar_path:
        if tar_path.endswith("/"):
            tar_path = tar_path[:-1]
        executor_cmd.append(f"--tarPath {tar_path}/{image_name}.tar")
        job.append_scripts(f"mkdir -p {tar_path}")

    if verbosity:
        executor_cmd.append(f"--verbosity {verbosity}")

    if not dockerfile and PredefinedVariables.CI_PROJECT_DIR:
        dockerfile = f"{PredefinedVariables.CI_PROJECT_DIR}/Dockerfile"

    if dockerfile:
        executor_cmd.append(f"--dockerfile {dockerfile}")

    # Disable push to registries.
    if not enable_push:
        executor_cmd.append("--no-push")

    # Check if multistage build is wanted.
    # Add --target flag to executor and prefix build_target "-"
    build_target_postfix = ""
    if build_target:
        executor_cmd.append(f"--target {build_target}")
        build_target_postfix = f"-{build_target}"

    # Compose build arguments.
    for k, v in build_args.items():
        executor_cmd.append(f"--build-arg '{k}={v}'")

    # Extend executor comman with --destination per registry
    if len(registries) == 0:
        executor_cmd.append(f"--destination {image_name}{image_tag_postfix}{build_target_postfix}")
        if image_tag and (image_tag == "main" or image_tag == "master"):
            executor_cmd.append(f"--destination {image_name}:latest{build_target_postfix}")

    for registry in registries:
        executor_cmd.append(f"--destination {registry}/{image_name}{image_tag_postfix}{build_target_postfix}")
        if image_tag and (image_tag == "main" or image_tag == "master"):
            executor_cmd.append(f"--destination {registry}/{image_name}:latest{build_target_postfix}")

    if ecr_login:
        job.prepend_scripts('mkdir -p /kaniko/.docker && echo "{\\"credsStore\\":\\"ecr-login\\"}" > /kaniko/.docker/config.json')

    if dockerhub_user_env_var and dockerhub_login_env_var:
        job.prepend_scripts(
            'mkdir -p /kaniko/.docker && echo "{\\"auths\\":{\\"https://index.docker.io/v1/\\":{\\"username\\":\\"$' +
            dockerhub_user_env_var + '\\",\\"password\\":\\"$' + dockerhub_login_env_var + '\\"}}}" > /kaniko/.docker/config.json'
        )

    job.append_scripts(" ".join(executor_cmd))
    job.append_scripts("rm -rf /kaniko/.docker/config.json")

    if gitlab_executor_image:
        job.set_image(gitlab_executor_image)
    return job
