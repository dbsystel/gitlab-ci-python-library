def clone_repository(path: str, *args, branch: str = "master"):
    if not path.startswith("/"):
        path = "/" + path
    return f"git clone --branch {branch} --single-branch https://gitlab-ci-token:${{CI_JOB_TOKEN}}@${{CI_SERVER_HOST}}{path}.git"


def pip_install_requirements() -> str:
    """
    Runs `pip3 install --upgrade -r requirements.txt`

    * Requires to have access to the `requirements.txt` in the working directory.
    """
    return "pip3 install --upgrade -r requirements.txt"
