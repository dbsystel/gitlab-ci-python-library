"""**ALPHA** This module represents the Gitlab CI [Service](https://docs.gitlab.com/ee/ci/yaml/README.html#services) keyword.

The services keyword defines a Docker image that runs during a job linked to the Docker image that the image keyword defines.
This allows you to access the service image during build time.

Currently this module is an unfinished prototype.
"""


class Service:
    """**ALPHA** This class represents the Gitlab CI [Service](https://docs.gitlab.com/ee/ci/yaml/README.html#services) keyword.

    Currently there is nothing more implemented than providing a service name. In general the `service` functionality
    currently isn't well implemented, as is is only available for `gcip.core.pipeline.Pipeline`s.
    """

    def __init__(self, name: str):
        self._name = name

    def render(self) -> str:
        """Return a representation of this Service object as dictionary with static values.

        The rendered representation is used by the gcip to dump it
        in YAML format as part of the .gitlab-ci.yml pipeline.

        Returns:
            Dict[str, Any]: A dictionary representing the service object in Gitlab CI.
        """
        return self._name
