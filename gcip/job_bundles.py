from gcip import gcip
from gcip import jobs


def cdk_diff_deploy(
    *args,
    stack: str,
    toolkit_stack_name: str,
) -> gcip.JobBundle:
    bundle = gcip.JobBundle()
    bundle.add_job(
        job=jobs.cdk_diff(stack),
        job_name="cdk_diff",
    )
    bundle.add_job(
        job=jobs.cdk_deploy(stack, toolkit_stack_name),
        job_name="cdk_deploy",
    )
    return bundle
