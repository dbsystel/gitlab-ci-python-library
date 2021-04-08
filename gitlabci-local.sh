#!/bin/bash

# Run the Gitlab CI pipeline of this project on your local machine

if ! command -v gitlabci-local &> /dev/null
then
    echo "Please install following requirement before:"
    echo "pip3 install gitlabci-local"
    exit
fi

echo "Powerd by https://pypi.org/project/gitlabci-local/"
gitlabci-local -p -e CI="true" -e CI_PROJECT_DIR="/builds/gitlab-ci-python-library" -e CI_COMMIT_REF_SLUG="gitlab-local-sh" && cat generated-config.yml && gitlabci-local -c generated-config.yml $@

rm -rf generated-config.yml
rm -rf dist
rm -rf build
rm -rf .pytest_cache
rm -rf .mypy_cache
rm -rf gcip.egg-info
