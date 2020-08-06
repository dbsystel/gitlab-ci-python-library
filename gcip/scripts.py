from typing import Any


def clone_repository(path: str, *args: Any, branch: str = "master") -> str:
    if not path.startswith("/"):
        path = "/" + path
    return f"git clone --branch {branch} --single-branch https://gitlab-ci-token:${{CI_JOB_TOKEN}}@${{CI_SERVER_HOST}}{path}.git"
