import gcip


def cdk_diff(stack: str) -> gcip.Job:
    return gcip.Job(
        name="cdk_diff",
        script=[
            f"cdk synth {stack}",
            f"cdk diff {stack}",
        ],
    )


def cdk_deploy(stack: str, toolkit_stack_name: str) -> gcip.Job:
    return gcip.Job(
        name="cdk_deploy",
        script=[f"cdk deploy --strict --require-approval 'never' --toolkit-stack-name {toolkit_stack_name} {stack}"],
    )
