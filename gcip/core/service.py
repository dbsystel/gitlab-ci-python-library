class Service:
    """This class represents the Gitlab CI [Service](https://docs.gitlab.com/ee/ci/yaml/README.html#services) keyword."""

    def __init__(self, name: str):
        self._name = name

    def render(self) -> str:
        return self._name
