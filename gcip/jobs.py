import gcip


def cdk_diff(stack: str):
    return gcip.Job(
        name="cdk_diff",
        stage="diff",
        script=[
            f"cdk synth {stack}",
            f"cdk diff {stack}",
        ],
    )


def cdk_deploy(stack: str, toolkit_stack_name: str):
    return gcip.Job(
        name="cdk_deploy",
        stage="deploy",
        script=f"cdk deploy --strict --require-approval 'never' --toolkit-stack-name {toolkit_stack_name} {stack}",
    )


def flake8():
    """
    Runs `flake8`

    * Requires a Gitlab executor with _flake8_ installed.
    * Does not install requirements, so you should prepend `gcip.scipts.pip_install_requirements()`
    """
    return gcip.Job(name="flake8", stage="lint", script="flake8")


def isort():
    """
    Runs `isort --check .`

    * Requires a Gitlab executor with _isort_ installed.
    * Does not install requirements, so you should prepend `gcip.scipts.pip_install_requirements()`
    """
    return gcip.Job(name="isort", stage="lint", script="isort --check .")


def pytest():
    """
    Runs `pytest`

    * Requires a Gitlab executor with _pytest_ installed.
    * Does not install requirements, so you should prepend `gcip.scipts.pip_install_requirements()`
    """
    return gcip.Job(name="pytest", stage="test", script="isort --check .")


def python_bdist_wheel():
    """
    Runs `python3 setup.py bdist_wheel`

    * Requires a Gitlab executor with _setuptools_ installed.
    * Does not install requirements, so you should prepend `gcip.scipts.pip_install_requirements()`
    """
    return gcip.Job(name="bdist_wheel", stage="build", script="python3 setup.py bdist_wheel")
