import gcip
from gcip import rules


def flake8():
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


def isort():
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
            scipts.pip_install_requirements(),
            "isort --check .",
        ],
    )


def pytest():
    """
    Runs `pytest` and installs project requirements before (`gcip.scripts.pip_install_requirements()`)

    * Requires a `requirements.txt` in your project folder containing at least `pytest`
    """
    return gcip.Job(
        name="pytest",
        stage="test",
        script=[
            scipts.pip_install_requirements(),
            "pytest",
        ],
    )


def evaluate_git_tag_pep404_conformity():
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
    job.add_rule(rules.only_tags())
    return job


def bdist_wheel():
    """
    Runs `python3 setup.py bdist_wheel` and installs project requirements before (`gcip.scripts.pip_install_requirements()`)

    * Requires a `requirements.txt` in your project folder containing at least `setuptools`
    """
    return gcip.Job(
        name="bdist_wheel",
        stage="build",
        script=[
            scipts.pip_install_requirements(),
            "python3 setup.py bdist_wheel",
        ],
    )


def pages_sphinx():
    """
    Runs `sphinx-build -b html -E -a docs public/${CI_COMMIT_REF_NAME}` and installs project requirements
    before (`gcip.scripts.pip_install_requirements()`)

    * Requires a `docs/requirements.txt` in your project folder` containing at least `sphinx`
    """
    return gcip.Job(
        name="pages_python_sphinx",
        stage="build",
        script=[
            scripts.pip_install_requirements("docs/requirements.txt"),
            "sphinx-build -b html -E -a docs public/${CI_COMMIT_REF_NAME}",
        ],
    )


def twine_upload(
    varname_repository_url: str,
    varname_user: str,
    varname_password: str,
):
    """
    Runs:

    ```
    pip3 install --upgrade twine
    python3 -m twine upload --non-interactive --disable-progress-bar dist/*
    ```

    :arg varname_repository_url: The name of the environment variable delivering the URL to the PyPI repository.
    :arg varname_user: The name of the environment variable delivering the user to access the PyPI repository.
    :arg varname_password: The name of the environment variable delivering the password to access the PyPI repository.
    """
    if not varname_repository_url.startswith("$"):
        varname_repository_url = "$" + varname_repository_url

    if not varname_user.startswith("$"):
        varname_user = "$" + varname_user

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
        TWINE_REPOSITORY_URL=varname_repository_url,
        TWINE_USERNAME=varname_user,
        TWINE_PASSWORD=varname_password,
    )
    return job
