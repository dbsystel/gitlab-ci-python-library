class Service:
    def __init__(self, name: str):
        self._name = name

    def render(self) -> str:
        return self._name
