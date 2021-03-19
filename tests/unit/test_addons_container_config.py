from tests import conftest
from gcip.addons.container.config import DockerClientConfig


def test_docker_client_config():
    dcc = DockerClientConfig()
    dcc.add_auth("index.docker.com")
    conftest.check(dcc.get_shell_command())


def test_complex_docker_client_config():
    dcc = DockerClientConfig()
    dcc.add_auth("index.docker.com", "CUSTOM_DOCKER_USER", "CUSTOM_DOCKER_PW")
    dcc.add_cred_helper("123456789.dkr.ecr.eu-central-1.amazonaws.com", "ecr-login")
    dcc.set_creds_store("gcr")
    dcc.add_raw({"proxies": {
        "default": {
            "httpProxy": "127.0.0.1:1234"
        }
    }})
    conftest.check(dcc.get_shell_command())
