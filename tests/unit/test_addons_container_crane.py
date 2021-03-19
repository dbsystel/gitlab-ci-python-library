from gcip import Pipeline
from tests import conftest
from gcip.core.image import Image
from gcip.addons.container.jobs import crane
from gcip.addons.container.config import DockerClientConfig


def test_default_crane_job():
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


def test_advanced_crane_job():
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
