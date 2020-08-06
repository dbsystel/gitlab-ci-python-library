import gcip
from gcip import rules, scripts


def flake8() -> gcip.Job:
    """
    Runs:

    ```
    pip3 install --upgrade flake8
    flake8
    ```
    """
    return gcip.Job(
        name="flake8",
        stage="lint",
        script=[
            "pip3 install --upgrade flake8",
            "flake8",
        ],
    )


def isort() -> gcip.Job:
    """
    Runs:

    ```
    pip3 install --upgrade isort
    isort --check .
    ```
    """
    return gcip.Job(
        name="isort",
        stage="lint",
        script=[
            "pip3 install --upgrade isort",
            "isort --check .",
        ],
    )


def pytest() -> gcip.Job:
    """
    Runs `pytest` and installs project requirements before (`gcip.scripts.pip_install_requirements()`)

    * Requires a `requirements.txt` in your project folder containing at least `pytest`
    """
    return gcip.Job(
        name="pytest",
        stage="test",
        script=[
            scripts.pip_install_requirements(),
            "pytest",
        ],
    )


def evaluate_git_tag_pep404_conformity() -> gcip.Job:
    """
    Checks if the current pipelines `$CI_COMMIT_TAG` validates to a valid Python package version according to
    https://www.python.org/dev/peps/pep-0440

    This job already contains a rule to only run when a `$CI_COMMIT_TAG` is present (`gcip.rules.only_tags()`).
    """
    job = gcip.Job(
        name="evaluate_git_tag_pep404_conformity",
        stage="test",
        script=[
            "pip3 install --upgrade gcip",
            "python3 -m gcip.script_library.evaluate_git_tag_pep404_conformity",
        ],
    )
    job.add_rules(rules.only_tags())
    return job


def bdist_wheel() -> gcip.Job:
    """
    Runs `python3 setup.py bdist_wheel` and installs project requirements before (`gcip.scripts.pip_install_requirements()`)

    * Requires a `requirements.txt` in your project folder containing at least `setuptools`
    * Creates artifacts under the path `dist/`
    """
    job = gcip.Job(
        name="bdist_wheel",
        stage="build",
        script=[
            scripts.pip_install_requirements(),
            "python3 setup.py bdist_wheel",
        ],
    )
    job.add_artifacts_paths("dist/")
    return job


def pages_sphinx() -> gcip.Job:
    """
    Runs `sphinx-build -b html -E -a docs public/${CI_COMMIT_REF_NAME}` and installs project requirements
    before (`gcip.scripts.pip_install_requirements()`)

    * Requires a `docs/requirements.txt` in your project folder` containing at least `sphinx`
    * Creates it artifacts for Gitlab Pages under `pages`
    """
    job = gcip.Job(
        name="pages_python_sphinx",
        stage="build",
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
) -> gcip.Job:
    """
    Runs:

    ```
    pip3 install --upgrade twine
    python3 -m twine upload --non-interactive --disable-progress-bar dist/*
    ```

    * Requires artifacts from a build job under `dist/` (e.g. from `gcip.jobs.python.bdist_wheel()`)

    :arg repository_url: The URL to the PyPI repository the python artifacts will be deployed to.
    :arg user: The name of the user to access the PyPI repository.
    :arg varname_password: The name of the environment variable delivering the password to access the PyPI repository.
    If not existent, automatically a "$" will be prepended to the string. DO NOT DEFINE THE PASSWORD WITHIN THE PIPELINE.
    Define your password outside the pipeline, e.g. as secret variable in the Gitlab CI/CD settings section.
    """
    if not varname_password.startswith("$"):
        varname_password = "$" + varname_password

    job = gcip.Job(
        name="twine_upload",
        stage="deploy",
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
