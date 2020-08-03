from gcip import gcip
from gcip import scripts
from gcip import jobs
from gcip import job_sequences


def import_windows_vm_image(stage: str):
    return f"python3 update_windows_vm_image.py {stage}"


def pipeline_stage(pipeline: gcip.Pipeline,
                   environment: str) -> gcip.JobSequence:
    pipeline.add_sequence(
        job_sequence=job_sequences.cdk_diff_deploy(
            stack=f"myapp-{environment}-project-resources",
            toolkit_stack_name="foobar-toolkit",
        ),
        namespace=f"{environment}_project_resources",
    )

    if environment == "unstable":
        pipeline.add_sequence(
            job_sequence=job_sequences.cdk_diff_deploy(
                stack=f"myapp-{environment}-windows-vm-bucket",
                toolkit_stack_name="foobar-toolkit",
            ),
            namespace=f"{environment}_windows_vm_bucket",
        )

    pipeline.add_sequence(
        job_sequence=job_sequences.cdk_diff_deploy(
            stack=f"myapp-{environment}-windows-vm-instances",
            toolkit_stack_name="foobar-toolkit",
        ),
        namespace=f"{environment}_windows_vm_intances",
    )


def test_full_pipeline_yaml_output():

    variables_unstable = {"MYPROJECT_RELEASE_VERSION": ">=0.dev"}
    variables_dev = {"MYPROJECT_RELEASE_VERSION": "==0.0.dev10"}
    variables_tst = {"MYPROJECT_RELEASE_VERSION": "==0.0.dev10"}
    variables_iat = {"MYPROJECT_RELEASE_VERSION": "==0.0.dev10"}

    image_iat = "python:3.9-slim"
    image_prd = "python:3.9-slim"

    #full_stage = gcip.JobSequence()

    pipeline = gcip.Pipeline(before_script=[
        scripts.clone_repository("otherproject/configuration")
    ], )

    for environment in ["unstable", "dev", "tst", "iat"]:
        pipeline_stage(pipeline, environment)

    pipeline.prepend_script("./install-dependencies.sh")

    pipeline.print_yaml()
