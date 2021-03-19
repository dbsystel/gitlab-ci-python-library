"""This module represents a Docker client configuration.

Example:

```
from gcip.addons.container.config import DockerClientConfig

cfg = DockerClientConfig()
cfg.add_cred_helper("1234567890.dkr.ecr.us-east-1.amazonaws.com", "ecr-login")
cfg.render()
```

This will render a Client configuration and dumps it as a json string.
"""
import json
from typing import Any, Dict

DockerConfig = Dict[str, Any]


class DockerClientConfig():
    def __init__(self, config_file_path: str = "$HOME/.docker/", config_file_name: str = "config.json") -> None:
        """
        Class which represents a docker client configuration.

        After creating an instance of this class you can add new credential helper or
        basic authentication settings. Or set a default credential store.
        The constructor has a limited feature set. If you change either `config_file_path` or `config_file_name`,
        you should consider using `docker --config` to specify the path to the configuration file.

        Args:
            config_file_path (str): Filesystem path where to create the docker client directory. Defaults to $HOME/.docker/.
            config_file_name (str): Docker client configuration filename. Defaults to config.json.
        """
        self._config_file_path = config_file_path
        self._config_file_name = config_file_name
        self.config: DockerConfig = {}

    def set_creds_store(self, creds_store: str) -> None:
        """
        Sets the `credsStore` setting for clients.
        See [docker login#credentials-store](https://docs.docker.com/engine/reference/commandline/login/#credentials-store)

        Be aware, that if you set the `credsStore` and add creds_helper or
        username and password authentication, those authentication methods
        are not used.

        Clients which can authenticate against a registry can handle the credential
        store itself, mostly you do not want to set the `credsStore`.
        Use `credsHelpers` instead.

        Args:
            creds_store (str): Should be the suffix of the program to use
            (i.e. everything after docker-credential-).
            For example `osxkeychain`, to use docker-credential-osxkeychain or
            `ecr-login`, to use docker-crendential-ecr-login
        """
        self.config["credsStore"] = creds_store

    def add_cred_helper(self, registry: str, cred_helper: str) -> None:
        """
        Adds a Credentials helper `credHelpers` for a registry.
        See [docker login#credential-helpers](https://docs.docker.com/engine/reference/commandline/login/#credential-helpers)

        Args:
            registry (str): Name of the container registry to set `creds_helper` for.
            cred_helper (str): Name of the credential helper to use together with the `registry`.
        """
        compose = {
            registry: cred_helper
        }
        if "credsHelpers" not in self.config.keys():
            self.config["credHelpers"] = compose
        else:
            self.config["credHelpers"].update(compose)

    def add_auth(
        self,
        registry: str,
        username_env_var: str = "REGISTRY_USERNAME",
        password_env_var: str = "REGISTRY_PASSWORD",
    ) -> None:
        """
        Adds basic authentication `auths` setting to the configuration.

        This method acts a little special, because of some security aspects.
        The method, takse three arguments, `registry`, `username_env_var` and `password_env_var`.
        Arguments ending wit *_env_var, are ment to be available as a `gcip.Job` variable.

        Args:
            registry (str): Name of the container registry to set `creds_helper` for.
            username_env_var (str): Name of the environment variable which as the registry username stored. Defaults to REGISTRY_USERNAME.
            password_env_var (str): Name of the environment variable which as the registry password stored. Defaults to REGISTRY_PASSWORD.
        """
        compose = {
            registry: {
                "username": "$" + username_env_var,
                "password": "$" + password_env_var
            }
        }

        if "auths" not in self.config.keys():
            self.config["auths"] = compose
        else:
            self.config["auths"].update(compose)

    def add_raw(self, raw_input: Dict[Any, Any]) -> None:
        """
        Adds arbitrary settings to configuration.

        Be aware and warned! You can overwrite any predefined settings with this method.
        This method is intendet to be used, if non suitable method is available and you
        have to set a configuration setting.

        Args:
            raw_input (Dict[Any, Any]): Dictionary of non-available settings to be set.
        """
        self.config.update(raw_input)

    def render(self) -> str:
        """
        Renders the shell command for creating the docker client config.

        The render method uses `json.dumps()` to dump the configuration as a json string and escapes it for the shell.
        In Jobs which needed the configuration the renderd output should be redirected to the appropriate
        destinatino e.g. ~/.docker/config.json. This ensures, that environment variables are substituted.

        Returns:
            str: Docker client configuration as a JSON string.
        """
        script = [
            f"mkdir -p {self._config_file_path}",
            "echo " + '"' + json.dumps(self.config).replace('"', '\\"') + '"' + f" > {self._config_file_path}{self._config_file_name}",
        ]
        return script
