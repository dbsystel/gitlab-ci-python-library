from gcip import Pipeline, PredefinedVariables
from tests import conftest
from gcip.addons.kaniko import jobs as kaniko


def test_default_kaniko_job(gitlab_ci_environment_variables):
    pipeline = Pipeline()

    pipeline.add_children(
        kaniko.execute(
            image_name="thomass/gcip",
            enable_push=(PredefinedVariables.CI_COMMIT_TAG or PredefinedVariables.CI_COMMIT_BRANCH == "main"),
            dockerhub_user_env_var="DOCKER_USER",
            dockerhub_login_env_var="DOCKER_LOGIN",
        ),
    )

    conftest.check(pipeline.render())
