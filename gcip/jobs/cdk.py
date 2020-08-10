import gcip


def bootstrap(
    *args: None, aws_account_id: str, aws_region: str, toolkit_stack_name: str, bootstrap_kms_key_id: str, **tags: str
) -> gcip.Job:
    return gcip.Job(
        name="cdk_bootstrap",
        script="cdk bootstrap"
        f" --toolkit-stack-name {toolkit_stack_name}"
        f" --bootstrap-kms-key-id {bootstrap_kms_key_id}"
        f" aws://{aws_account_id}/{aws_region}" +
        " ".join([""] + list(map(lambda keyvalue: f"-t {keyvalue[0]}={keyvalue[1]}", tags.items()))),
    )


def diff(stack: str) -> gcip.Job:
    return gcip.Job(
        name="cdk_diff",
        stage="diff",
        script=[
            f"cdk synth {stack}",
            f"cdk diff {stack}",
        ],
    )


def deploy(stack: str, toolkit_stack_name: str) -> gcip.Job:
    return gcip.Job(
        name="cdk_deploy",
        stage="deploy",
        script=f"cdk deploy --strict --require-approval 'never' --toolkit-stack-name {toolkit_stack_name} {stack}",
    )
