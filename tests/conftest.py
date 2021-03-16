import os
import inspect
import pathlib

import yaml
import pytest


def check(output: str) -> bool:
    yaml_output = yaml.safe_dump(output, default_flow_style=False, sort_keys=False)
    # inspired by https://stackoverflow.com/a/60297932
    caller_file_path, caller_file_name = os.path.split(os.path.abspath(inspect.stack()[1].filename))
    caller_file_name = os.path.splitext(caller_file_name)[0]
    caller_function_name = inspect.stack()[1].function
    compare_file = f"{caller_file_path}/comparison_files/{caller_file_name}_{caller_function_name}.yml"

    if os.getenv("UPDATE_TEST_OUTPUT", "false").lower() == "true":
        pathlib.Path(os.path.split(compare_file)[0]).mkdir(parents=True, exist_ok=True)
        with open(compare_file, "w") as outfile:
            outfile.write(yaml_output)
    else:
        with open(compare_file, "r") as infile:
            assert yaml_output == infile.read()


@pytest.fixture
def gitlab_ci_environment_variables(monkeypatch):
    """
    Fixture to patch GitLab CI predefined environment variables.

    You can extend this fixture with all GitLab CI environment variables that will be used by gcip.PredefinedVariables.
    All other environment variables should be placed elswhere.

    Fore more information about `monkeypatch` ->
    https://docs.pytest.org/en/stable/monkeypatch.html
    https://docs.pytest.org/en/stable/monkeypatch.html#monkeypatching-environment-variables
    """
    monkeypatch.setenv("CI_PROJECT_NAME", "gitlab-ci-project")
    monkeypatch.setenv("CI_PROJECT_PATH", "my/awsome/project")
    monkeypatch.setenv("CI_COMMIT_REF_SLUG", "my-awsome-feature-branch")
    monkeypatch.setenv("CI_PROJECT_DIR", "/path/to/project")
