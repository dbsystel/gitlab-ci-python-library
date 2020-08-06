import gcip
from gcip.job_sequences import python


def test():
    pipeline = gcip.Pipeline()

    pipeline.add_sequence(
        python.full_stack(
            repository_url="https://my.artifactory.net/pypi/repository",
            user="$ARTIFACTORY_USER",
            varname_password="$ARTIFACTORY_PASSWORD",
        )
    )

    pipeline.print_yaml()
