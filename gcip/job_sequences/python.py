import gcip
from gcip.jobs import python


def full_stack(
    repository_url: str,
    user: str,
    varname_password: str,
) -> gcip.JobSequence:
    """
    Returns a pipeline containing all jobs from `gcip.jobs.python`:
        * isort
        * flake8
        * pytest
        * evaluating CI_COMMIT_TAG as valid PyPI version string (if exists)
        * bdist_wheel
        * Gitlab Pages sphinx
        * twine upload

    :arg repository_url: The URL to the PyPI repository the python artifacts will be deployed to.
    :arg user: The name of the user to access the PyPI repository.
    :arg varname_password: The name of the environment variable delivering the password to access the PyPI repository.
    If not existent, automatically a "$" will be prepended to the string. DO NOT DEFINE THE PASSWORD WITHIN THE PIPELINE.
    Define your password outside the pipeline, e.g. as secret variable in the Gitlab CI/CD settings section.
    """
    sequence = gcip.JobSequence()
    sequence.add_jobs(
        python.isort(),
        python.flake8(),
        python.pytest(),
        python.evaluate_git_tag_pep404_conformity(),
        python.bdist_wheel(),
        python.pages_sphinx(),
        python.twine_upload(repository_url, user, varname_password),
    )
    return sequence
