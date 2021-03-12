from gcip import Pipeline, PredefinedVariables
from gcip.addons.kaniko import jobs as kaniko
from gcip.addons.python import jobs as python

pipeline = Pipeline()
pipeline.initialize_image("python:3.9-slim")

pipeline.add_children(
    python.isort(), python.flake8(), python.pytest(), python.evaluate_git_tag_pep404_conformity(),
    kaniko.execute(
        image_name="thomass/gcip",
        enable_push=(PredefinedVariables.CI_COMMIT_TAG or PredefinedVariables.CI_COMMIT_BRANCH == "master"),
        dockerhub_user_env_var="DOCKER_USER",
        dockerhub_login_env_var="DOCKER_LOGIN",
    )
)

pipeline.write_yaml()
