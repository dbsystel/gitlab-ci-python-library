from typing import Optional

from gcip.lib import rules
from gcip.core.job import Job
from gcip.addons.container.images import PredefinedImages

from . import job_scripts as scripts

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


def flake8() -> Job:
    """
    Runs:

    ```
    pip3 install --upgrade flake8
    flake8
    ```
    """
    return Job(
        name="flake8",
        namespace="lint",
        script=[
            "pip3 install --upgrade flake8",
            "flake8",
        ],
    )


def mypy(package_dir: str) -> Job:
    """Runs:

    ```python
    pip3 install --upgrade mypy
    mypy package_dir
    ```

    Args:
        package_dir (str): Relativ path to package which should be checked with mypy.

    Returns:
        Job: Job running mypy.
    """
    return Job(
        name="mypy",
        namespace="test",
        script=["pip3 install --upgrade mypy", f"mypy {package_dir}"],
    )


def isort() -> Job:
    """
    Runs:

    ```
    pip3 install --upgrade isort
    isort --check .
    ```
    """
    return Job(
        name="isort",
        namespace="lint",
        script=[
            "pip3 install --upgrade isort",
            "isort --check .",
        ],
    )


def pytest() -> Job:
    """
    Runs `pytest` and installs project requirements before (`scripts.pip_install_requirements()`)

    * Requires a `requirements.txt` in your project folder containing at least `pytest`
    """
    return Job(
        name="pytest",
        namespace="test",
        script=[
            scripts.pip_install_requirements(),
            "pytest",
        ],
    )


def evaluate_git_tag_pep440_conformity() -> Job:
    """
    Checks if the current pipelines `$CI_COMMIT_TAG` validates to a valid Python package version according to
    https://www.python.org/dev/peps/pep-0440

    This job already contains a rule to only run when a `$CI_COMMIT_TAG` is present (`rules.only_tags()`).
    """
    job = Job(
        name="evaluate_git_tag_pep440_conformity",
        namespace="test",
        script="python3 -m gcip.tools.evaluate_git_tag_pep440_conformity",
    )
    job.append_rules(rules.on_tags())
    job.set_image(PredefinedImages.GCIP)
    return job


def bdist_wheel() -> Job:
    """
    Runs `python3 setup.py bdist_wheel` and installs project requirements
    before (`scripts.pip_install_requirements()`)

    * Requires a `requirements.txt` in your project folder containing at least `setuptools`
    * Creates artifacts under the path `dist/`
    """
    job = Job(
        name="bdist_wheel",
        namespace="build",
        script=[
            scripts.pip_install_requirements(),
            "python3 setup.py bdist_wheel",
        ],
    )
    job.add_artifacts_paths("dist/")
    return job


def pages_sphinx() -> Job:
    """
    Runs `sphinx-build -b html -E -a docs public/${CI_COMMIT_REF_NAME}` and installs project requirements
    before (`scripts.pip_install_requirements()`)

    * Requires a `docs/requirements.txt` in your project folder` containing at least `sphinx`
    * Creates it artifacts for Gitlab Pages under `pages`
    """
    job = Job(
        name="pages_python_sphinx",
        namespace="build",
        script=[
            scripts.pip_install_requirements("docs/requirements.txt"),
            "sphinx-build -b html -E -a docs public/${CI_COMMIT_REF_NAME}",
        ],
    )
    job.add_artifacts_paths("public")
    return job


def twine_upload(
    twine_repository_url: Optional[str] = None,
    twine_username_env_var: Optional[str] = "TWINE_USERNAME",
    twine_password_env_var: Optional[str] = "TWINE_PASSWORD",
) -> Job:
    """
    Runs:

    ```
    pip3 install --upgrade twine
    python3 -m twine upload --non-interactive --disable-progress-bar dist/*
    ```

    * Requires artifacts from a build job under `dist/` (e.g. from `bdist_wheel()`)

    Args:
        twine_repository_url (str): The URL to the PyPI repository the python artifacts will be deployed to. Defaults
            to `None`, which means the package is published to `https://pypi.org`.
        twine_username_env_var (Optional[str]): The name of the environment variable, which contains the username value.
            **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue! Defaults to `TWINE_USERNAME`.
        twine_password_env_var (Optional[str]): The name of the environment variable, which contains the password.
            **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue! Defaults to `TWINE_PASSWORD`.
    """
    job = Job(
        name="twine_upload",
        namespace="deploy",
        script=[
            "pip3 install --upgrade twine",
            "python3 -m twine upload --non-interactive --disable-progress-bar dist/*",
        ],
    )
    job.add_variables(
        TWINE_USERNAME=f"${twine_username_env_var}",
        TWINE_PASSWORD=f"${twine_password_env_var}",
    )

    if twine_repository_url:
        job.add_variables(TWINE_REPOSITORY_URL=twine_repository_url)

    return job
