"""This modules provide Jobs executing [Docker CLI](https://docs.docker.com/engine/reference/commandline/cli/) scripts

Those require [Docker to be installed](https://docs.docker.com/engine/install/) on the Gitlab runner.
"""

from typing import Optional

from gcip.core.job import Job

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


def build(
    *,
    repository: str,
    tag: Optional[str] = None,
    context: str = ".",
) -> Job:
    """Runs [```docker build```](https://docs.docker.com/engine/reference/commandline/build/)

    Example:

    ```
    from gcip.addons.docker import jobs as docker
    build_job = docker.build(repository="myrepo/myimage", tag="v0.1.0")
    ```

    Args:
        repository (str): The Docker repository name ```([<registry>/]<image>)```.
        tag (Optional[str]): A Docker image tag applied to the image. Defaults to `None` which no tag is provided
            to the docker build command. Docker should then apply the default tag ```latest```.
        context (str): The Docker build context (the directory containing the Dockerfile). Defaults to
            the current directory `.`.

    Returns:
        A `gcip.core.job.Job` object doing the docker build.
    """
    _fq_image_name = repository
    if tag:
        _fq_image_name += f":{tag}"
    return Job(
        name="docker",
        namespace="build",
        script=f"docker build -t {_fq_image_name} {context}",
    ).add_variables(DOCKER_DRIVER="overlay2", DOCKER_TLS_CERTDIR="")


def push(
    *,
    registry: Optional[str] = None,
    image: str,
    tag: Optional[str] = None,
    user_env_var: Optional[str] = None,
    login_env_var: Optional[str] = None,
) -> Job:
    """Runs [```docker push```](https://docs.docker.com/engine/reference/commandline/push/)
       and optionally [```docker login```](https://docs.docker.com/engine/reference/commandline/login/) before.

    Example:

    ```
    from gcip.addons.docker import jobs as docker
    build_job = docker.push(
                    registry="docker.pkg.github.com/dbsystel/gitlab-ci-python-library",
                    image="gcip",
                    tag="v0.1.0",
                    user_env_var="DOCKER_USER",
                    login_env_var="DOCKER_TOKEN")
    ```

    The `user_env_var` and `login_env_var` should be created as *protected* and *masked*
    [custom environment variable configured
    in the UI](https://git.tech.rz.db.de/help/ci/variables/README#create-a-custom-variable-in-the-ui).

    Args:
        registry (Optional[str]): The Docker registry the image should be pushed to.
            Defaults to `None` which targets to the official Docker Registry at hub.docker.com.
        image (str): The name of the Docker image to push to the `registry`.
        tag (Optional[str]): The Docker image tag that should be pushed to the `registry`. Defaults to ```latest```.
        user_env_var (Optional[str]): If you have to login to the registry before the push, you have to provide
            the name of the environment variable, which contains the username value, here.
            **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
            Defaults to `None` which skips the docker login attempt.
        login_env_var (Optional[str]): If you have to login to the registry before the push, you have to provide
            the name of the environment variable, which contains the password or token, here.
            **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
            Defaults to `None` which skips the docker login attempt.

    Returns:
        A `gcip.core.job.Job` object doing the docker push.
    """
    _fq_image_name = image

    if registry:
        _fq_image_name = f"{registry}/{_fq_image_name}"

    if tag:
        _fq_image_name += f":{tag}"

    job = Job(
        name="docker",
        namespace="deploy",
        script=f"docker push {_fq_image_name}",
    )

    if user_env_var and login_env_var:
        job.prepend_scripts(f'docker login -u "${user_env_var}" -p "${login_env_var}"')

    return job
