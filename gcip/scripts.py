def clone_repository(path: str, *args, branch: str = "master"):
    if not path.startswith("/"):
        path = "/" + path
    return f"git clone --branch {branch} --single-branch https://gitlab-ci-token:${{CI_JOB_TOKEN}}@${{CI_SERVER_HOST}}{path}.git"


def pip_install_requirements(requirements_file: str = "requirements.txt") -> str:
    """
    Runs `pip3 install --upgrade -r {requirements_file}`

    * Requires to have access to the `{requirements_file}` in the working directory.

    :arg requirements_file: Defaults to `requirements.txt`
    """
    return "pip3 install --upgrade -r {requirements_file}"
