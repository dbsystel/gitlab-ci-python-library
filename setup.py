import os

import setuptools

from gcip.script_library import (
    evaluate_git_tag_pep404_conformity as pep404,
)

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


def get_version() -> str:
    ci_commit_tag = os.getenv("CI_COMMIT_TAG")
    if ci_commit_tag is not None and pep404.is_canonical(ci_commit_tag):
        return ci_commit_tag
    return f"0.0.{os.getenv('CI_PIPELINE_ID')}"


with open("README.md") as fp:
    long_description_from_readme = fp.read()

setuptools.setup(
    name="gcip",
    version=get_version(),
    description="The Gitlab CI Python Library",
    long_description=long_description_from_readme,
    long_description_content_type="text/markdown",
    author="Thomas Steinbach",
    author_email="thomas.t.steinbach@deutschebahn.com",
    url=os.getenv("CI_PROJECT_URL"),
    packages=setuptools.find_packages(exclude=("tests*", )),
    include_package_data=True,
    python_requires="~=3.7",
    install_requires=[
        "pyaml~=20.4",
    ],
)
