from gcip import Image, Pipeline, PredefinedVariables
from gcip.addons.kaniko import jobs as kaniko
from gcip.addons.python import jobs as python

pipeline = Pipeline()
pipeline.initialize_image("python:3.9-slim")

# gitlabci-local only works with 'sh' as kaniko entrypoint
kaniko_image = None
if not PredefinedVariables.CI:
    kaniko_image = Image("gcr.io/kaniko-project/executor:debug", entrypoint=["sh"])

pipeline.add_children(
    python.isort(),
    python.flake8(),
    python.pytest(),
    python.bdist_wheel(),
    kaniko.execute(
        gitlab_executor_image=kaniko_image,
        image_name="thomass/gcip",
        enable_push=(PredefinedVariables.CI_COMMIT_TAG or PredefinedVariables.CI_COMMIT_BRANCH == "main"),
        registry_user_env_var="DOCKER_USER",
        registry_login_env_var="DOCKER_LOGIN",
    ),
)

if PredefinedVariables.CI_COMMIT_TAG:
    pipeline.add_children(
        python.evaluate_git_tag_pep440_conformity(),
        python.twine_upload(),
    )

pipeline.write_yaml()
