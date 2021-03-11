from typing import Optional

from gcip.lib import rules
from gcip.core.job_sequence import JobSequence

from . import jobs as python

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


def full_stack(
    dev_repository_url: str,
    dev_user: str,
    varname_dev_password: str,
    stable_repository_url: str,
    stable_user: str,
    varname_stable_password: str,
    mypy_package_dir: Optional[str] = None,
) -> JobSequence:
    """
    Returns a pipeline containing all jobs from `gcip.addons.python.jobs`:
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
    sequence = JobSequence()
    sequence.add_children(
        python.isort(),
        python.flake8(),
        python.pytest(),
        python.evaluate_git_tag_pep404_conformity(),
        python.bdist_wheel(),
    )

    if mypy_package_dir:
        sequence.add_children(python.mypy(mypy_package_dir))

    pages_sphinx = python.pages_sphinx()
    pages_sphinx.append_rules(
        rules.on_main(),
        rules.on_master(),
        rules.on_tags(),
    )
    sequence.add_children(pages_sphinx)

    twine_upload_dev = python.twine_upload(dev_repository_url, dev_user, varname_dev_password)
    twine_upload_dev.append_rules(
        rules.on_tags().never(),
        rules.on_success(),
    )
    sequence.add_children(twine_upload_dev, name="dev")

    twine_upload_stable = python.twine_upload(stable_repository_url, stable_user, varname_stable_password)
    twine_upload_stable.append_rules(rules.on_tags())
    sequence.add_children(twine_upload_stable, name="stable")

    return sequence
