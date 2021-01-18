import tempfile

import gcip
from gcip import (
    IncludeLocal,
    IncludeRemote,
    IncludeTemplate,
    rules,
    scripts,
)
from tests import conftest
from gcip.job_sequences import cdk


def myapp_diff_deploy(environment: str, resource: str) -> gcip.JobSequence:
    return cdk.diff_deploy(f"myapp-{environment}-{resource}", toolkit_stack_name=f"application-{environment}-cdk-toolkit")


def environment_pipeline(environment: str) -> gcip.JobSequence:
    env_pipe = gcip.JobSequence()

    env_pipe.add_sequences(myapp_diff_deploy(environment, "project-resources"), namespace="project_resources")

    if environment == "unstable":
        env_pipe.add_sequences(myapp_diff_deploy(environment, "windows-vm-bucket"), namespace="windows_vm_bucket")
        update_image_job = gcip.Job(namespace="update-windows-vm-image", script=f"python3 update_windows_vm_image.py {environment}")
        update_image_job.append_rules(rules.on_merge_request_events().never(), gcip.Rule(if_statement="$IMAGE_SOURCE_PASSWORD"))
        env_pipe.add_jobs(update_image_job)
    else:
        env_pipe.add_jobs(gcip.Job(namespace="copy-windows-vm-image", script=f"python3 update_windows_vm_image.py {environment}"))

    if environment == "dev":
        env_pipe.add_sequences(
            myapp_diff_deploy(environment, "windows-vm-instances-barista"), namespace="windows_vm_intances", name="barista"
        )
        env_pipe.add_sequences(
            myapp_diff_deploy(environment, "windows-vm-instances-impala"), namespace="windows_vm_intances", name="impala"
        )
    else:
        env_pipe.add_sequences(myapp_diff_deploy(environment, "windows-vm-instances"), namespace="windows_vm_intances")

    return env_pipe


def test_full_pipeline_yaml_output():

    pipeline = gcip.Pipeline()
    pipeline.initialize_image("python:3.9-slim")
    pipeline.prepend_scripts(
        scripts.clone_repository("otherproject/configuration"),
        "./install-dependencies.sh",
    )
    pipeline.add_tags("environment-iat")

    for environment in ["unstable", "dev", "tst", "iat"]:
        env_pipe = environment_pipeline(environment)
        if environment == "unstable":
            env_pipe.add_variables(MYPROJECT_RELEASE_VERSION=">=0.dev")
        else:
            env_pipe.add_variables(MYPROJECT_RELEASE_VERSION="==0.0.dev10")
        pipeline.add_sequences(env_pipe, namespace=environment)

    conftest.check(pipeline.render())


def test_includes_pipeline():
    first_include = IncludeLocal("local-file.yml")
    second_include = IncludeRemote("https://gitlab.com/my/project/include_file.yml")
    pipeline = gcip.Pipeline(includes=[first_include, second_include])
    pipeline.add_include(IncludeTemplate("Template-Include-File.yml"))
    conftest.check(pipeline.render())


def test_write_yaml():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(gcip.Job(script="testjob", namespace="test"))
    target = tempfile.TemporaryFile()
    pipeline.write_yaml(target.name)
