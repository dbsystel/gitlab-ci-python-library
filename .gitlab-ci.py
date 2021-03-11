from gcip import Pipeline
from gcip.addons.python import sequences as python

pipeline = Pipeline()
pipeline.initialize_image("python:3.9-slim")
pipeline.add_tags("environment-prd")

pipeline.add_children(
    python.full_stack(
        dev_repository_url="<pypi-repo-url-dev>",
        dev_user="$ARTIFACTORY_DEV_USER",
        varname_dev_password="$ARTIFACTORY_DEV_PASSWORD",
        stable_repository_url="<pypi-repo-url-stable>",
        stable_user="$ARTIFACTORY_PRD_USER",
        varname_stable_password="$ARTIFACTORY_PRD_PASSWORD",
        mypy_package_dir="./gcip"
    ),
)

pipeline.write_yaml()
