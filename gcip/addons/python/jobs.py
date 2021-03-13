from gcip.lib import rules
from gcip.core.job import Job

from . import job_scripts as scripts

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


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


def evaluate_git_tag_pep404_conformity() -> Job:
    """
    Checks if the current pipelines `$CI_COMMIT_TAG` validates to a valid Python package version according to
    https://www.python.org/dev/peps/pep-0440

    This job already contains a rule to only run when a `$CI_COMMIT_TAG` is present (`rules.only_tags()`).
    """
    job = Job(
        name="evaluate_git_tag_pep404_conformity",
        namespace="test",
        script="python3 -m gcip.tools.evaluate_git_tag_pep404_conformity",
    )
    job.append_rules(rules.on_tags())
    job.set_image("thomass/gcip:0.3.0")
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
    repository_url: str,
    user: str,
    varname_password: str,
) -> Job:
    """
    Runs:

    ```
    pip3 install --upgrade twine
    python3 -m twine upload --non-interactive --disable-progress-bar dist/*
    ```

    * Requires artifacts from a build job under `dist/` (e.g. from `bdist_wheel()`)

    :arg repository_url: The URL to the PyPI repository the python artifacts will be deployed to.
    :arg user: The name of the user to access the PyPI repository.
    :arg varname_password: The name of the environment variable delivering the password to access the PyPI repository.
    If not existent, automatically a "$" will be prepended to the string. DO NOT DEFINE THE PASSWORD WITHIN THE PIPELINE.
    Define your password outside the pipeline, e.g. as secret variable in the Gitlab CI/CD settings section.
    """
    if not varname_password.startswith("$"):
        varname_password = "$" + varname_password

    job = Job(
        name="twine_upload",
        namespace="deploy",
        script=[
            "pip3 install --upgrade twine",
            "python3 -m twine upload --non-interactive --disable-progress-bar dist/*",
        ],
    )
    job.add_variables(
        TWINE_REPOSITORY_URL=repository_url,
        TWINE_USERNAME=user,
        TWINE_PASSWORD=varname_password,
    )
    return job
