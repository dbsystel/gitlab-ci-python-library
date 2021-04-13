from gcip import Image, Pipeline, PredefinedVariables
from gcip.addons.python import jobs as python
from gcip.addons.container.sequences import build

pipeline = Pipeline()
pipeline.initialize_image("python:3.9-slim")

# gitlabci-local only works with 'sh' as kaniko and crane entrypoint
kaniko_image = None
crane_image = None
if PredefinedVariables.CI_COMMIT_REF_SLUG == "gitlab-local-sh":
    kaniko_image = Image("gcr.io/kaniko-project/executor:debug", entrypoint=["sh"])
    crane_image = Image("gcr.io/go-containerregistry/crane:debug", entrypoint=["sh"])

pipeline.add_children(
    python.isort(),
    python.flake8(),
    python.pytest(),
    python.mypy("gcip"),
    python.bdist_wheel(),
)

pipeline.add_children(
    build.build_scan_push_image(
        image_name="thomass/gcip",
        kaniko_kwargs={"kaniko_image": kaniko_image},
        crane_kwargs={"crane_image": crane_image},
    ),
    name="gcip",
)

if PredefinedVariables.CI_COMMIT_TAG:
    pipeline.add_children(
        python.evaluate_git_tag_pep440_conformity(),
        python.twine_upload(),
    )

pipeline.write_yaml()
