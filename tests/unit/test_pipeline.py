from gcip import gcip
from gcip import scripts
from gcip import jobs
from gcip import job_sequences


def environment_pipeline(environment: str) -> gcip.JobSequence:
    env_pipe = gcip.JobSequence(environment)

    env_pipe.add_sequence(job_sequences.cdk_diff_deploy(
        stack=f"myapp-{environment}-project-resources",
        toolkit_stack_name="foobar-toolkit"),
                          namespace="project_resources")

    if environment == "unstable":
        env_pipe.add_sequence(job_sequences.cdk_diff_deploy(
            stack=f"myapp-{environment}-windows-vm-bucket",
            toolkit_stack_name="foobar-toolkit"),
                              namespace=f"windows_vm_bucket")

    env_pipe.add_sequence(job_sequences.cdk_diff_deploy(
        stack=f"myapp-{environment}-windows-vm-instances",
        toolkit_stack_name="foobar-toolkit"),
                          namespace=f"windows_vm_intances")

    return env_pipe


def test_full_pipeline_yaml_output():

    variables_unstable = {"MYPROJECT_RELEASE_VERSION": ">=0.dev"}
    variables_dev = {"MYPROJECT_RELEASE_VERSION": "==0.0.dev10"}
    variables_tst = {"MYPROJECT_RELEASE_VERSION": "==0.0.dev10"}
    variables_iat = {"MYPROJECT_RELEASE_VERSION": "==0.0.dev10"}

    image_iat = "python:3.9-slim"
    image_prd = "python:3.9-slim"

    pipeline = gcip.Pipeline()
    pipeline.prepend_script(
        scripts.clone_repository("otherproject/configuration"))

    for environment in ["unstable", "dev", "tst", "iat"]:
        pipeline.add_sequence(environment_pipeline(environment))

    pipeline.prepend_script("./install-dependencies.sh")

    pipeline.print_yaml()
