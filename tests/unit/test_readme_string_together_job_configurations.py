from gcip import Job, Rule, Pipeline
from tests import conftest


def test():
    pipeline = Pipeline()

    # yapf: disable
    pipeline.add_children(
        Job(stage="print_date", script="date")
        .set_image("docker/image:example")
        .prepend_scripts("./before-script.sh")
        .append_scripts("./after-script.sh")
        .add_variables(USER="Max Power", URL="https://example.com")
        .add_tags("test", "europe")
        .add_artifacts_paths("binaries/", ".config")
        .append_rules(Rule(if_statement="$MY_VARIABLE_IS_PRESENT"))
    )
    # yapf: enable

    conftest.check(pipeline.render())
