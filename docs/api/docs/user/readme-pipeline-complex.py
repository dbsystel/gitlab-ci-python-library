from gcip import Pipeline, JobSequence, Job
from gcip.addons.gitlab import job_scripts as gitlab


def get_build_deploy_sequence(environment: str):
    return JobSequence().add_children(
        Job(namespace="build", script=f"docker build -t myimage-{environment} ."),
        Job(namespace="deploy", script=["docker login", f"docker push myimage-{environment}"]),
    )


pipeline = Pipeline()
pipeline.initialize_image("my/enterprise/build-image:stable")

for environment in ("develop", "test", "production"):
    jobs = get_build_deploy_sequence(environment)
    jobs.prepend_scripts(
        gitlab.clone_repository(path="projectx/configuration", branch=environment),
        f"source {environment}.env",
    )
    jobs.add_tags(environment)

    pipeline.add_children(jobs, namespace=environment)

pipeline.write_yaml("generated-config.yml")
