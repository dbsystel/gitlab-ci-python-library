import tempfile

import gcip
from gcip import (
    Service,
    IncludeLocal,
    IncludeRemote,
    IncludeTemplate,
)
from tests import conftest
from gcip.lib import rules
from gcip.addons.cdk import sequences as cdk
from gcip.addons.gitlab import job_scripts


def myapp_diff_deploy(environment: str, resource: str) -> gcip.Sequence:
    return cdk.diff_deploy(f"myapp-{environment}-{resource}", toolkit_stack_name=f"application-{environment}-cdk-toolkit")


def environment_pipeline(environment: str) -> gcip.Sequence:
    env_pipe = gcip.Sequence()

    env_pipe.add_children(myapp_diff_deploy(environment, "project-resources"), namespace="project_resources")

    if environment == "unstable":
        env_pipe.add_children(myapp_diff_deploy(environment, "windows-vm-bucket"), namespace="windows_vm_bucket")
        update_image_job = gcip.Job(namespace="update-windows-vm-image", script=f"python3 update_windows_vm_image.py {environment}")
        update_image_job.append_rules(rules.on_merge_request_events().never(), gcip.Rule(if_statement="$IMAGE_SOURCE_PASSWORD"))
        env_pipe.add_children(update_image_job)
    else:
        env_pipe.add_children(gcip.Job(namespace="copy-windows-vm-image", script=f"python3 update_windows_vm_image.py {environment}"))

    if environment == "dev":
        env_pipe.add_children(
            myapp_diff_deploy(environment, "windows-vm-instances-barista"), namespace="windows_vm_intances", name="barista"
        )
        env_pipe.add_children(myapp_diff_deploy(environment, "windows-vm-instances-impala"), namespace="windows_vm_intances", name="impala")
    else:
        env_pipe.add_children(myapp_diff_deploy(environment, "windows-vm-instances"), namespace="windows_vm_intances")

    return env_pipe


def test_full_pipeline_yaml_output():

    pipeline = gcip.Pipeline()
    pipeline.initialize_image("python:3.9-slim")
    pipeline.prepend_scripts(
        job_scripts.clone_repository("otherproject/configuration"),
        "./install-dependencies.sh",
    )
    pipeline.add_tags("environment-iat")

    for environment in ["unstable", "dev", "tst", "iat"]:
        env_pipe = environment_pipeline(environment)
        if environment == "unstable":
            env_pipe.add_variables(MYPROJECT_RELEASE_VERSION=">=0.dev")
        else:
            env_pipe.add_variables(MYPROJECT_RELEASE_VERSION="==0.0.dev10")
        pipeline.add_children(env_pipe, namespace=environment)

    conftest.check(pipeline.render())


def test_includes_pipeline():
    first_include = IncludeLocal("local-file.yml")
    second_include = IncludeRemote("https://gitlab.com/my/project/include_file.yml")
    pipeline = gcip.Pipeline(includes=[first_include, second_include])
    pipeline.add_include(IncludeTemplate("Template-Include-File.yml"))
    conftest.check(pipeline.render())


def test_write_yaml():
    pipeline = gcip.Pipeline()
    pipeline.add_children(gcip.Job(script="testjob", namespace="test"))
    target = tempfile.TemporaryFile()
    pipeline.write_yaml(target.name)


def test_services():
    pipeline = gcip.Pipeline()
    pipeline.add_services("foo", "bar")
    pipeline.add_services(Service("baz"))
    conftest.check(pipeline.render())
