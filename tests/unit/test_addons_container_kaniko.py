from gcip import Pipeline
from tests import conftest
from gcip.addons.container.jobs import kaniko
from gcip.addons.container.config import DockerClientConfig
from gcip.addons.container.registries import Registry


def test_simple_kaniko_job(gitlab_ci_environment_variables):
    pipeline = Pipeline()
    pipeline.add_children(
        kaniko.execute(),
        name="simple",
    )
    conftest.check(pipeline.render())


def test_default_kaniko_job(gitlab_ci_environment_variables):
    pipeline = Pipeline()
    dcc = DockerClientConfig()
    dcc.add_auth("index.docker.io", username_env_var="DOCKER_USER", password_env_var="DOCKER_LOGIN")

    pipeline.add_children(
        kaniko.execute(image_name="thomass/gcip", enable_push=True, docker_client_config=dcc),
        name="gcip",
    )

    conftest.check(pipeline.render())


def test_container_kaniko_job_docker_v2_replacement_(gitlab_ci_environment_variables):
    pipeline = Pipeline()
    dcc = DockerClientConfig()
    dcc.add_auth(Registry.DOCKER)
    pipeline.add_children(
        kaniko.execute(
            image_name="thomass/gcip",
            image_tag="v2.2.2",
            docker_client_config=dcc,
        ),
        name="gcip2",
    )

    conftest.check(pipeline.render())
