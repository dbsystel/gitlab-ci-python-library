from gcip import Pipeline
from tests import conftest
from gcip.addons.container.jobs import kaniko
from gcip.addons.container.config import DockerClientConfig


def test_default_kaniko_job(gitlab_ci_environment_variables):
    pipeline = Pipeline()
    dcc = DockerClientConfig(config_file_path="/kaniko/.docker")
    dcc.add_auth("index.docker.io", username_env_var="DOCKER_USER", password_env_var="DOCKER_LOGIN")

    pipeline.add_children(
        kaniko.execute(
            image_name="thomass/gcip",
            enable_push=True,
            docker_client_config=dcc
        ), name="gcip",
    )

    conftest.check(pipeline.render())
