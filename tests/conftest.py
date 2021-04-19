import os
import inspect
import pathlib
from typing import Any, Dict

import yaml
import pytest

from gcip.addons.container.config import DockerClientConfig


def check(output: Dict[str, Any]) -> None:
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
        try:
            with open(compare_file, "r") as infile:
                assert yaml_output == infile.read()
        except FileNotFoundError as exc:
            print(
                "Comparison file not found.",
                "Create it by executing:\n\n",
                f"\tUPDATE_TEST_OUTPUT=true pytest {caller_file_path}",
            )
            raise exc
        except AssertionError as exc:
            print(
                "If intentionally, you can update the comparions file:\n\n",
                "\trm -rf test/unit/comparison_files/*; UPDATE_TEST_OUTPUT=true pytest\n\n",
                "Always review the results carefully with 'git diff'!",
            )
            raise exc


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
    monkeypatch.setenv("CI", "true")  # indicate we are running within a (fake) pipeline
    monkeypatch.setenv("CI_PROJECT_NAME", "gitlab-ci-project")
    monkeypatch.setenv("CI_PROJECT_PATH", "my/awsome/project")
    monkeypatch.setenv("CI_COMMIT_REF_SLUG", "my-awsome-feature-branch")
    monkeypatch.setenv("CI_COMMIT_REF_NAME", "my_awsome_feature_branch")
    monkeypatch.setenv("CI_COMMIT_TAG", "11.22.33")
    monkeypatch.setenv("CI_PROJECT_DIR", "/path/to/project")


@pytest.fixture()
def docker_client_config() -> DockerClientConfig:
    dcc = DockerClientConfig()
    dcc.add_auth(registry="index.docker.io")
    dcc.add_cred_helper("0132456789.dkr.eu-central-1.amazonaws.com", cred_helper="ecr-login")
    return dcc
