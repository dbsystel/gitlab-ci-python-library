from tests import conftest
from gcip.core.pipeline import Pipeline
from gcip.addons.container.config import DockerClientConfig
from gcip.addons.container.registries import Registry
from gcip.addons.container.sequences.build import (
    build_scan_push_image,
)


def test_build_scan_push_image(gitlab_ci_environment_variables):
    pipeline = Pipeline()
    dcc = DockerClientConfig()
    dcc.add_cred_helper(Registry.QUAY, "quay-login")
    pipeline.add_children(build_scan_push_image(registry=Registry.QUAY, docker_client_config=dcc))
    conftest.check(pipeline.render())


def test_addons_container_sequences_build_scan_push_image(gitlab_ci_environment_variables):
    pipeline = Pipeline()
    dcc = DockerClientConfig()
    dcc.add_auth(Registry.DOCKER)
    trivy_config = {"trivy_image": "custom/trivy:v1.2.3"}
    kaniko_config = {"build_args": {"first_arg": "foo", "second_arg": "bar"}}
    pipeline.add_children(
        build_scan_push_image(
            registry=Registry.DOCKER,
            docker_client_config=dcc,
            kaniko_kwargs=kaniko_config,
            trivy_kwargs=trivy_config,
        )
    )
    conftest.check(pipeline.render())
