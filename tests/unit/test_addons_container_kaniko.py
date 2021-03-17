from gcip import Pipeline
from tests import conftest
from gcip.addons.container.jobs import kaniko


def test_default_kaniko_job(gitlab_ci_environment_variables):
    pipeline = Pipeline()

    pipeline.add_children(
        kaniko.execute(
            image_name="thomass/gcip",
            enable_push=True,
            registry_user_env_var="DOCKER_USER",
            registry_login_env_var="DOCKER_LOGIN",
        ),
    )

    conftest.check(pipeline.render())
