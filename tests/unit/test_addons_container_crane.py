from gcip import Pipeline
from tests import conftest
from gcip.core.image import Image
from gcip.addons.container.jobs import crane
from gcip.addons.container.config import DockerClientConfig
from gcip.addons.container.registries import Registry


def test_simple_crane_copy_job(gitlab_ci_environment_variables):
    pipeline = Pipeline()

    pipeline.add_children(
        crane.copy("index.docker.io/alpine:3", "index.docker.io/user/alpine:3"),
        name="default",
    )
    pipeline.add_children(
        crane.copy(
            "quay.io/wagoodman/dive:0.10.0",
            "index.docker.io/user/dive:latest",
            crane_image=Image("index.docker.io/user/crane:latest"),
        ),
        name="custom_image",
    )
    conftest.check(pipeline.render())


def test_advanced_crane_copy_job(gitlab_ci_environment_variables):
    dcc = DockerClientConfig()
    dcc.add_auth(registry="index.docker.io")
    dcc.add_cred_helper("0132456789.dkr.eu-central-1.amazonaws.com", "ecr-login")

    pipeline = Pipeline()
    pipeline.add_children(
        crane.copy(
            "index.docker.io/alpine:3",
            "0132456789.dkr.eu-central-1.amazonaws.com/namespace/alpine:3",
            docker_client_config=dcc,
        ),
        name="with_authentication",
    )
    conftest.check(pipeline.render())


def test_simple_crane_push_job(gitlab_ci_environment_variables):
    pipeline = Pipeline()
    pipeline.add_children(crane.push(dst_registry="index.docker.io"), name="push_image")
    conftest.check(pipeline.render())


def test_advanced_crane_push_job(gitlab_ci_environment_variables):
    dcc = DockerClientConfig()
    dcc.add_auth(registry="index.docker.io")
    dcc.add_cred_helper("0132456789.dkr.eu-central-1.amazonaws.com", cred_helper="ecr-login")
    pipeline = Pipeline()
    pipeline.add_children(
        crane.push(
            dst_registry="index.docker.io",
            image_name="crane",
            docker_client_config=dcc,
            crane_image="crane_image:v1.1.2",
        ),
        name="push_image",
    )
    conftest.check(pipeline.render())


def test_addons_container_jobs_crane_push_registry(gitlab_ci_environment_variables):
    dcc = DockerClientConfig()
    dcc.add_auth(registry=Registry.DOCKER)
    dcc.add_cred_helper("0132456789.dkr.eu-central-1.amazonaws.com", cred_helper="ecr-login")
    pipeline = Pipeline()
    pipeline.add_children(
        crane.push(
            dst_registry=Registry.DOCKER,
            image_name="crane",
            docker_client_config=dcc,
            crane_image="crane_image:v1.1.2",
        ),
        name="push_image",
    )
    conftest.check(pipeline.render())
