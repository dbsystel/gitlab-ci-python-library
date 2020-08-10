import gcip
from tests import conftest
from gcip.job_sequences import python


def test():
    pipeline = gcip.Pipeline()

    pipeline.add_sequences(
        python.full_stack(
            dev_repository_url="https://my.artifactory.net/pypi/dev-repository",
            dev_user="$ARTIFACTORY_DEV_USER",
            varname_dev_password="$ARTIFACTORY_DEV_PASSWORD",
            stable_repository_url="https://my.artifactory.net/pypi/prod-repository",
            stable_user="$ARTIFACTORY_PROD_USER",
            varname_stable_password="$ARTIFACTORY_PROD_PASSWORD",
        )
    )

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['lint', 'test', 'build', 'deploy'],
            'isort': {
                'script': ['pip3 install --upgrade isort', 'isort --check .'],
                'stage': 'lint'
            },
            'flake8': {
                'script': ['pip3 install --upgrade flake8', 'flake8'],
                'stage': 'lint'
            },
            'pytest': {
                'script': ['pip3 install --upgrade -r requirements.txt', 'pytest'],
                'stage': 'test'
            },
            'evaluate_git_tag_pep404_conformity': {
                'script': ['pip3 install --upgrade gcip', 'python3 -m gcip.script_library.evaluate_git_tag_pep404_conformity'],
                'rules': [{
                    'if': '$CI_COMMIT_TAG',
                    'when': 'on_success',
                    'allow_failure': False
                }],
                'stage': 'test'
            },
            'bdist_wheel': {
                'script': ['pip3 install --upgrade -r requirements.txt', 'python3 setup.py bdist_wheel'],
                'artifacts': {
                    'paths': ['dist/']
                },
                'stage': 'build'
            },
            'pages_python_sphinx': {
                'script':
                ['pip3 install --upgrade -r docs/requirements.txt', 'sphinx-build -b html -E -a docs public/${CI_COMMIT_REF_NAME}'],
                'rules': [
                    {
                        'if': '$CI_COMMIT_REF_NAME == "master"',
                        'when': 'on_success',
                        'allow_failure': False
                    }, {
                        'if': '$CI_COMMIT_TAG',
                        'when': 'on_success',
                        'allow_failure': False
                    }
                ],
                'artifacts': {
                    'paths': ['public']
                },
                'stage':
                'build'
            },
            'twine_upload_dev': {
                'script': ['pip3 install --upgrade twine', 'python3 -m twine upload --non-interactive --disable-progress-bar dist/*'],
                'variables': {
                    'TWINE_REPOSITORY_URL': 'https://my.artifactory.net/pypi/dev-repository',
                    'TWINE_USERNAME': '$ARTIFACTORY_DEV_USER',
                    'TWINE_PASSWORD': '$ARTIFACTORY_DEV_PASSWORD'
                },
                'rules': [
                    {
                        'if': '$CI_PIPELINE_SOURCE == "merge_request_event"',
                        'when': 'never',
                        'allow_failure': False
                    }, {
                        'if': '$CI_COMMIT_TAG',
                        'when': 'never',
                        'allow_failure': False
                    }, {
                        'if': '$CI_COMMIT_REF_NAME == "master"',
                        'when': 'on_success',
                        'allow_failure': False
                    }
                ],
                'stage':
                'deploy'
            },
            'twine_upload_stable': {
                'script': ['pip3 install --upgrade twine', 'python3 -m twine upload --non-interactive --disable-progress-bar dist/*'],
                'variables': {
                    'TWINE_REPOSITORY_URL': 'https://my.artifactory.net/pypi/prod-repository',
                    'TWINE_USERNAME': '$ARTIFACTORY_PROD_USER',
                    'TWINE_PASSWORD': '$ARTIFACTORY_PROD_PASSWORD'
                },
                'rules': [{
                    'if': '$CI_COMMIT_TAG',
                    'when': 'on_success',
                    'allow_failure': False
                }],
                'stage': 'deploy'
            }
        },
    )
