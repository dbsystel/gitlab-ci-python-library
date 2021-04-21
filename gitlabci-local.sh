#!/bin/bash

# Run the Gitlab CI pipeline of this project on your local machine

if ! command -v gitlabci-local &> /dev/null
then
    echo "Please install following requirement before:"
    echo "pip3 install gitlabci-local"
    exit
fi

echo "Powerd by https://pypi.org/project/gitlabci-local/"

if [ -z $REGISTRY_USERNAME ]; then
    read -p "Enter container registry user: " REGISTRY_USERNAME
fi
if [ -z $REGISTRY_PASSWORD ]; then
    read -sp "Enter container registry password: " REGISTRY_PASSWORD
fi

./remove-caches.sh

gitlabci_local_envs="-e CI=true
    -e CI_PROJECT_NAME=gitlab-ci-python-library
    -e CI_PROJECT_DIR=/builds/gitlab-ci-python-library
    -e CI_COMMIT_REF_SLUG=gitlab-local-sh
    -e REGISTRY_USERNAME=${REGISTRY_USERNAME}
    -e REGISTRY_PASSWORD=${REGISTRY_PASSWORD}"

gitlabci-local -p $gitlabci_local_envs && \
cat generated-config.yml && \
gitlabci-local $gitlabci_local_envs -c generated-config.yml $@

./remove-caches.sh