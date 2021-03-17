from gcip import Pipeline
from tests import conftest
from gcip.addons.container.jobs import docker


def test_default_docker_jobs(gitlab_ci_environment_variables):
    pipeline = Pipeline()

    pipeline.add_children(
        docker.build(repository="myspace/myimage"),
        docker.push(image="myspace/myimage"),
    )

    conftest.check(pipeline.render())
