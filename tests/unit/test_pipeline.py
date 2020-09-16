import gcip
from gcip import rules, scripts
from tests import conftest
from gcip.job_sequences import cdk


def myapp_diff_deploy(environment: str, resource: str) -> gcip.JobSequence:
    return cdk.diff_deploy(stack=f"myapp-{environment}-{resource}", toolkit_stack_name=f"application-{environment}-cdk-toolkit")


def environment_pipeline(environment: str) -> gcip.JobSequence:
    env_pipe = gcip.JobSequence()

    env_pipe.add_sequences(myapp_diff_deploy(environment, "project-resources"), namespace="project_resources")

    if environment == "unstable":
        env_pipe.add_sequences(myapp_diff_deploy(environment, "windows-vm-bucket"), namespace="windows_vm_bucket")
        update_image_job = gcip.Job(name="update-windows-vm-image", script=f"python3 update_windows_vm_image.py {environment}")
        update_image_job.append_rules(rules.on_merge_request_events().never(), gcip.Rule(if_statement="$IMAGE_SOURCE_PASSWORD"))
        env_pipe.add_jobs(update_image_job)
    else:
        env_pipe.add_jobs(gcip.Job(name="copy-windows-vm-image", script=f"python3 update_windows_vm_image.py {environment}"))

    if environment == "dev":
        env_pipe.add_sequences(
            myapp_diff_deploy(environment, "windows-vm-instances-barista"), namespace="windows_vm_intances", name="barista"
        )
        env_pipe.add_sequences(
            myapp_diff_deploy(environment, "windows-vm-instances-impala"), namespace="windows_vm_intances", name="impala"
        )
    else:
        env_pipe.add_sequences(myapp_diff_deploy(environment, "windows-vm-instances"), namespace="windows_vm_intances")

    return env_pipe


def test_full_pipeline_yaml_output():

    pipeline = gcip.Pipeline()
    pipeline.set_image("python:3.9-slim")
    pipeline.prepend_scripts(
        scripts.clone_repository("otherproject/configuration"),
        "./install-dependencies.sh",
    )
    pipeline.add_tags("environment-iat")

    for environment in ["unstable", "dev", "tst", "iat"]:
        env_pipe = environment_pipeline(environment)
        if environment == "unstable":
            env_pipe.add_variables(MYPROJECT_RELEASE_VERSION=">=0.dev")
        else:
            env_pipe.add_variables(MYPROJECT_RELEASE_VERSION="==0.0.dev10")
        pipeline.add_sequences(env_pipe, namespace=environment)

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': [
                'diff_project_resources_unstable', 'deploy_project_resources_unstable', 'diff_windows_vm_bucket_unstable',
                'deploy_windows_vm_bucket_unstable', 'update_windows_vm_image_unstable', 'diff_windows_vm_intances_unstable',
                'deploy_windows_vm_intances_unstable', 'diff_project_resources_dev', 'deploy_project_resources_dev',
                'copy_windows_vm_image_dev', 'diff_windows_vm_intances_dev', 'deploy_windows_vm_intances_dev', 'diff_project_resources_tst',
                'deploy_project_resources_tst', 'copy_windows_vm_image_tst', 'diff_windows_vm_intances_tst',
                'deploy_windows_vm_intances_tst', 'diff_project_resources_iat', 'deploy_project_resources_iat', 'copy_windows_vm_image_iat',
                'diff_windows_vm_intances_iat', 'deploy_windows_vm_intances_iat'
            ],
            'cdk-diff-project-resources-unstable': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'cdk synth myapp-unstable-project-resources',
                    'cdk diff myapp-unstable-project-resources'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '>=0.dev'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'diff_project_resources_unstable'
            },
            'cdk-deploy-project-resources-unstable': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    "cdk deploy --strict --require-approval 'never' --toolkit-stack-name application-unstable-cdk-toolkit myapp-unstable-project-resources"  # noqa: E501,W505
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '>=0.dev'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'deploy_project_resources_unstable'
            },
            'cdk-diff-windows-vm-bucket-unstable': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'cdk synth myapp-unstable-windows-vm-bucket',
                    'cdk diff myapp-unstable-windows-vm-bucket'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '>=0.dev'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'diff_windows_vm_bucket_unstable'
            },
            'cdk-deploy-windows-vm-bucket-unstable': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    "cdk deploy --strict --require-approval 'never' --toolkit-stack-name application-unstable-cdk-toolkit myapp-unstable-windows-vm-bucket"  # noqa: E501,W505
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '>=0.dev'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'deploy_windows_vm_bucket_unstable'
            },
            'update-windows-vm-image-unstable': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'python3 update_windows_vm_image.py unstable'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '>=0.dev'
                },
                'tags': ['environment-iat'],
                'rules': [
                    {
                        'if': '$CI_PIPELINE_SOURCE == "merge_request_event"',
                        'when': 'never',
                        'allow_failure': False
                    }, {
                        'if': '$IMAGE_SOURCE_PASSWORD',
                        'when': 'on_success',
                        'allow_failure': False
                    }
                ],
                'image':
                'python:3.9-slim',
                'stage':
                'update_windows_vm_image_unstable'
            },
            'cdk-diff-windows-vm-intances-unstable': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'cdk synth myapp-unstable-windows-vm-instances',
                    'cdk diff myapp-unstable-windows-vm-instances'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '>=0.dev'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'diff_windows_vm_intances_unstable'
            },
            'cdk-deploy-windows-vm-intances-unstable': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    "cdk deploy --strict --require-approval 'never' --toolkit-stack-name application-unstable-cdk-toolkit myapp-unstable-windows-vm-instances"  # noqa: E501,W505
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '>=0.dev'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'deploy_windows_vm_intances_unstable'
            },
            'cdk-diff-project-resources-dev': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'cdk synth myapp-dev-project-resources',
                    'cdk diff myapp-dev-project-resources'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'diff_project_resources_dev'
            },
            'cdk-deploy-project-resources-dev': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    "cdk deploy --strict --require-approval 'never' --toolkit-stack-name application-dev-cdk-toolkit myapp-dev-project-resources"  # noqa: E501,W505
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'deploy_project_resources_dev'
            },
            'copy-windows-vm-image-dev': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'python3 update_windows_vm_image.py dev'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'copy_windows_vm_image_dev'
            },
            'cdk-diff-windows-vm-intances-barista-dev': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'cdk synth myapp-dev-windows-vm-instances-barista',
                    'cdk diff myapp-dev-windows-vm-instances-barista'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'diff_windows_vm_intances_dev'
            },
            'cdk-deploy-windows-vm-intances-barista-dev': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    "cdk deploy --strict --require-approval 'never' --toolkit-stack-name application-dev-cdk-toolkit myapp-dev-windows-vm-instances-barista"  # noqa: E501,W505
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'deploy_windows_vm_intances_dev'
            },
            'cdk-diff-windows-vm-intances-impala-dev': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'cdk synth myapp-dev-windows-vm-instances-impala',
                    'cdk diff myapp-dev-windows-vm-instances-impala'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'diff_windows_vm_intances_dev'
            },
            'cdk-deploy-windows-vm-intances-impala-dev': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    "cdk deploy --strict --require-approval 'never' --toolkit-stack-name application-dev-cdk-toolkit myapp-dev-windows-vm-instances-impala"  # noqa: E501,W505
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'deploy_windows_vm_intances_dev'
            },
            'cdk-diff-project-resources-tst': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'cdk synth myapp-tst-project-resources',
                    'cdk diff myapp-tst-project-resources'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'diff_project_resources_tst'
            },
            'cdk-deploy-project-resources-tst': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    "cdk deploy --strict --require-approval 'never' --toolkit-stack-name application-tst-cdk-toolkit myapp-tst-project-resources"  # noqa: E501,W505
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'deploy_project_resources_tst'
            },
            'copy-windows-vm-image-tst': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'python3 update_windows_vm_image.py tst'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'copy_windows_vm_image_tst'
            },
            'cdk-diff-windows-vm-intances-tst': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'cdk synth myapp-tst-windows-vm-instances',
                    'cdk diff myapp-tst-windows-vm-instances'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'diff_windows_vm_intances_tst'
            },
            'cdk-deploy-windows-vm-intances-tst': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    "cdk deploy --strict --require-approval 'never' --toolkit-stack-name application-tst-cdk-toolkit myapp-tst-windows-vm-instances"  # noqa: E501,W505
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'deploy_windows_vm_intances_tst'
            },
            'cdk-diff-project-resources-iat': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'cdk synth myapp-iat-project-resources',
                    'cdk diff myapp-iat-project-resources'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'diff_project_resources_iat'
            },
            'cdk-deploy-project-resources-iat': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    "cdk deploy --strict --require-approval 'never' --toolkit-stack-name application-iat-cdk-toolkit myapp-iat-project-resources"  # noqa: E501,W505
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'deploy_project_resources_iat'
            },
            'copy-windows-vm-image-iat': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'python3 update_windows_vm_image.py iat'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'copy_windows_vm_image_iat'
            },
            'cdk-diff-windows-vm-intances-iat': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    'cdk synth myapp-iat-windows-vm-instances',
                    'cdk diff myapp-iat-windows-vm-instances'
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'diff_windows_vm_intances_iat'
            },
            'cdk-deploy-windows-vm-intances-iat': {
                'script': [
                    'git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/otherproject/configuration.git',  # noqa: E501
                    './install-dependencies.sh',
                    "cdk deploy --strict --require-approval 'never' --toolkit-stack-name application-iat-cdk-toolkit myapp-iat-windows-vm-instances"  # noqa: E501,W505
                ],
                'variables': {
                    'MYPROJECT_RELEASE_VERSION': '==0.0.dev10'
                },
                'tags': ['environment-iat'],
                'image':
                'python:3.9-slim',
                'stage':
                'deploy_windows_vm_intances_iat'
            }
        },
    )
