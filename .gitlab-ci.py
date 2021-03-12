from gcip import Pipeline, PredefinedVariables
from gcip.addons.docker import jobs as docker
from gcip.addons.python import jobs as python

pipeline = Pipeline()
pipeline.initialize_image("python:3.9-slim")
pipeline.add_service("docker:dind")

pipeline.add_children(
    python.isort(),
    python.flake8(),
    python.pytest(),
    python.evaluate_git_tag_pep404_conformity(),
    docker.build(repository="thomass/gcip", tag=PredefinedVariables.CI_COMMIT_REF_SLUG),
)

if PredefinedVariables.CI_COMMIT_TAG or PredefinedVariables.CI_COMMIT_BRANCH == "master":
    pipeline.add_children(
        docker.push(
            image="thomass/gcip",
            tag=PredefinedVariables.CI_COMMIT_REF_SLUG,
            user_env_var="DOCKER_USER",
            login_env_var="DOCKER_LOGIN",
        )
    )

pipeline.write_yaml()
