import gcip
from gcip import rules, scripts, job_sequences


def myapp_diff_deploy(environment: str, resource: str) -> gcip.JobSequence:
    return job_sequences.cdk_diff_deploy(
        stack=f"myapp-{environment}-{resource}", toolkit_stack_name=f"application-{environment}-cdk-toolkit"
    )


def environment_pipeline(environment: str) -> gcip.JobSequence:
    env_pipe = gcip.JobSequence(namespace=environment)

    env_pipe.add_sequence(myapp_diff_deploy(environment, "project-resources"), namespace="project_resources")

    if environment == "unstable":
        env_pipe.add_sequence(myapp_diff_deploy(environment, "windows-vm-bucket"), namespace="windows_vm_bucket")
        update_image_job = gcip.Job(name="update-windows-vm-image", script=f"python3 update_windows_vm_image.py {environment}")
        update_image_job.add_rules(rules.not_on_merge_request_events(), gcip.Rule(if_statement="$IMAGE_SOURCE_PASSWORD"))
        env_pipe.add_job(update_image_job)
    else:
        env_pipe.add_job(gcip.Job(name="copy-windows-vm-image", script=f"python3 update_windows_vm_image.py {environment}"))

    if environment == "dev":
        env_pipe.add_sequence(
            myapp_diff_deploy(environment, "windows-vm-instances-barista"), namespace="windows_vm_intances", name="barista"
        )
        env_pipe.add_sequence(myapp_diff_deploy(environment, "windows-vm-instances-impala"), namespace="windows_vm_intances", name="impala")
    else:
        env_pipe.add_sequence(myapp_diff_deploy(environment, "windows-vm-instances"), namespace="windows_vm_intances")

    return env_pipe


def test_full_pipeline_yaml_output():

    pipeline = gcip.Pipeline()
    pipeline.set_image("python:3.9-slim")
    pipeline.prepend_script(
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
        pipeline.add_sequence(env_pipe)

    pipeline.print_yaml()
