from __future__ import annotations

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Daniel von Eßen"
__email__ = "daniel.von-essen@deutschebahn.com"

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
from typing import Any, Dict, List, Union
from os.path import dirname, normpath

from gcip.addons.container.registries import Registry

DockerConfig = Dict[str, Any]


class DockerClientConfig:
    def __init__(self) -> None:
        """
        Class which represents a docker client configuration.

        After creating an instance of this class you can add new credential helper or
        basic authentication settings. Or set a default credential store.
        """
        self._config_file_path: str = "$HOME/.docker/config.json"
        self.config: DockerConfig = {}

    def set_config_file_path(self, path: str) -> DockerClientConfig:
        """Change the path of the docker client configuration.

        If changed the config file will be created in this path.
        At instantiation time of an DockerClientConfig object
        the path will be defaulted to "$HOME/.docker/config.json".

        Args:
            path (str): Complete path to docker client config.

        Returns:
            DockerClientConfig: Returns the instance of `DockerClientConfig`.
        """
        self._config_file_path = normpath(path)
        return self

    def set_creds_store(self, creds_store: str) -> DockerClientConfig:
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
        return self

    def add_cred_helper(self, registry: Union[Registry, str], cred_helper: str) -> DockerClientConfig:
        """
        Adds a Credentials helper `credHelpers` for a registry.
        See [docker login#credential-helpers](https://docs.docker.com/engine/reference/commandline/login/#credential-helpers)

        Args:
            registry (str): Name of the container registry to set `creds_helper` for.
            cred_helper (str): Name of the credential helper to use together with the `registry`.
        """
        compose = {registry: cred_helper}
        if "credsHelpers" not in self.config.keys():
            self.config["credHelpers"] = compose
        else:
            self.config["credHelpers"].update(compose)
        return self

    def add_auth(
        self,
        registry: Union[Registry, str],
        username_env_var: str = "REGISTRY_USERNAME",
        password_env_var: str = "REGISTRY_PASSWORD",
    ) -> DockerClientConfig:
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
        if registry == Registry.DOCKER:
            registry = f"https://{registry}/v1/"
        compose = {
            registry: {
                "username": "$" + username_env_var,
                "password": "$" + password_env_var,
            }
        }

        if "auths" not in self.config.keys():
            self.config["auths"] = compose
        else:
            self.config["auths"].update(compose)
        return self

    def add_raw(self, raw_input: Dict[Any, Any]) -> DockerClientConfig:
        """
        Adds arbitrary settings to configuration.

        Be aware and warned! You can overwrite any predefined settings with this method.
        This method is intendet to be used, if non suitable method is available and you
        have to set a configuration setting.

        Args:
            raw_input (Dict[Any, Any]): Dictionary of non-available settings to be set.
        """
        self.config.update(raw_input)
        return self

    def get_shell_command(self) -> List[str]:
        """
        Renders the shell command for creating the docker client config.

        The render method uses `json.dumps()` to dump the configuration as a json string and escapes it for the shell.
        In Jobs which needed the configuration the renderd output should be redirected to the appropriate
        destinatino e.g. ~/.docker/config.json. This ensures, that environment variables are substituted.

        Returns:
            list:  Returns a list with `mkdir -p config_file_path` and a shell escaped JSON string
                echoed to `config_file_path`/`config_file_name`
        """
        script = [
            f"mkdir -p {dirname(self._config_file_path)}",
            'echo "' + json.dumps(self.config).replace('"', '\\"') + '" > ' + self._config_file_path,
        ]
        return script
