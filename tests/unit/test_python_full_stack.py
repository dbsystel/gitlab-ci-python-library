import gcip
from tests import conftest
from gcip.job_sequences import python


def test():
    pipeline = gcip.Pipeline()

    pipeline.add_sequences(
        python.full_stack(
            dev_repository_url="https://my.artifactory.net/pypi/dev-repository",
            dev_user="$ARTIFACTORY_DEV_USER",
            varname_dev_password="$ARTIFACTORY_DEV_PASSWORD",
            stable_repository_url="https://my.artifactory.net/pypi/prod-repository",
            stable_user="$ARTIFACTORY_PROD_USER",
            varname_stable_password="$ARTIFACTORY_PROD_PASSWORD",
        )
    )

    conftest.check(pipeline.render())
