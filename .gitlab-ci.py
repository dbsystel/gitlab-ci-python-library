from gcip import Image, Pipeline, PredefinedVariables
from gcip.addons.python import jobs as python
from gcip.addons.container.jobs import kaniko

pipeline = Pipeline()
pipeline.initialize_image("python:3.9-slim")

# gitlabci-local only works with 'sh' as kaniko entrypoint
kaniko_image = None
if PredefinedVariables.CI_COMMIT_REF_SLUG == "gitlab-local-sh":
    kaniko_image = Image("gcr.io/kaniko-project/executor:debug", entrypoint=["sh"])

pipeline.add_children(
    python.isort(),
    python.flake8(),
    python.pytest(),
    python.mypy("gcip"),
    python.bdist_wheel(),
)

pipeline.add_children(
    kaniko.execute(
        gitlab_executor_image=kaniko_image,
        image_name="thomass/gcip",
        enable_push=PredefinedVariables.CI_COMMIT_TAG is not None or PredefinedVariables.CI_COMMIT_BRANCH == "main",
    ),
    name="gcip",
)

if PredefinedVariables.CI_COMMIT_TAG:
    pipeline.add_children(
        python.evaluate_git_tag_pep440_conformity(),
        python.twine_upload(),
    )

pipeline.write_yaml()
