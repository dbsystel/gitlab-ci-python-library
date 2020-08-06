import gcip
from tests import conftest
from gcip.job_sequences import python


def test():
    pipeline = gcip.Pipeline()

    pipeline.add_sequence(
        python.full_stack(
            repository_url="https://my.artifactory.net/pypi/repository",
            user="$ARTIFACTORY_USER",
            varname_password="$ARTIFACTORY_PASSWORD",
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
                'stage': 'build'
            },
            'pages_python_sphinx': {
                'script':
                ['pip3 install --upgrade -r docs/requirements.txt', 'sphinx-build -b html -E -a docs public/${CI_COMMIT_REF_NAME}'],
                'stage': 'build'
            },
            'twine_upload': {
                'script': ['pip3 install --upgrade twine', 'python3 -m twine upload --non-interactive --disable-progress-bar dist/*'],
                'variables': {
                    'TWINE_REPOSITORY_URL': 'https://my.artifactory.net/pypi/repository',
                    'TWINE_USERNAME': '$ARTIFACTORY_USER',
                    'TWINE_PASSWORD': '$ARTIFACTORY_PASSWORD'
                },
                'stage': 'deploy'
            }
        },
    )
