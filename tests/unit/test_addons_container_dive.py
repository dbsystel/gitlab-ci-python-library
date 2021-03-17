from gcip import Pipeline
from tests import conftest
from gcip.addons.container.jobs import dive


def test_default_dive_job(gitlab_ci_environment_variables):
    pipeline = Pipeline()

    pipeline.add_children(
        dive.scan(),
        name="default",
    )
    pipeline.add_children(
        dive.scan(image_path="/absolute/path/", image_name="image_name"),
        name="custom_image_and_path",
    )
    pipeline.add_children(
        dive.scan(
            highest_user_wasted_percent=0.1,
            highest_wasted_bytes=0.2,
            lowest_efficiency=0.3,
            ignore_errors=True,
        ),
        name="custom_settings",
    )

    conftest.check(pipeline.render())
