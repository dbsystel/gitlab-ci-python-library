from tests import conftest
from gcip.core.pipeline import Pipeline
from gcip.addons.container.jobs import trivy


def test_trivy_simple_scan_local_image(gitlab_ci_environment_variables):
    pipeline = Pipeline()
    pipeline.add_children(trivy.scan_local_image(), name="simple_scan")
    conftest.check(pipeline.render())


def test_trivy_advanced_scan_local_image(gitlab_ci_environment_variables):
    pipeline = Pipeline()
    pipeline.add_children(
        trivy.scan_local_image(
            image_path="/foo/bar/baz",
            image_name="custom_image",
            output_format="json",
            severity="MEDIUM,HIGH,CRITICAL",
            trivy_config="--list-all-pkgs",
        ), name="advanced_scan"
    )
    conftest.check(pipeline.render())
