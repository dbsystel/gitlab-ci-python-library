from gcip import Pipeline, TriggerJob, TriggerStrategy
from setup import get_version
from gcip.lib import rules
from gcip.addons.python import sequences as python

pipeline = Pipeline()
pipeline.initialize_image("<docker-image-with-cdk-and-python>")
pipeline.add_tags("environment-prd")

pipeline.add_children(
    python.full_stack(
        dev_repository_url="<pypi-repo-url-dev>",
        dev_user="$ARTIFACTORY_DEV_USER",
        varname_dev_password="$ARTIFACTORY_DEV_PASSWORD",
        stable_repository_url="<pypi-repo-url-stable>",
        stable_user="$ARTIFACTORY_PRD_USER",
        varname_stable_password="$ARTIFACTORY_PRD_PASSWORD",
    )
)

trigger_custom_gcip_library_job = TriggerJob(
    namespace="trigger-custom-gcip-library",
    project="otherproject/custom-gcip-library",
    branch="main",
    strategy=TriggerStrategy.DEPEND,
)
trigger_custom_gcip_library_job.add_variables(CUSTOM_GCIP_LIB_UPSTREAM_GCIP_VERSION=get_version())
trigger_custom_gcip_library_job.append_rules(rules.on_tags().never(), rules.on_main())
pipeline.add_children(trigger_custom_gcip_library_job)

pipeline.print_yaml()
