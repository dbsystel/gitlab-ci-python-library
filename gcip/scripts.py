def clone_repository(path: str):
    if not path.startswith("/"):
        path = "/" + path
    return f"git clone --branch master --single-branch https://gitlab-ci-token:${{CI_JOB_TOKEN}}@${{CI_SERVER_HOST}}{path}.git"
