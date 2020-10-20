from typing import Optional

from gcip import Include, IncludeMethod


class LocalInclude(Include):
    def __init__(self, file: str) -> None:
        super().__init__(file=file, include_method=IncludeMethod.LOCAL)


class FileInclude(Include):
    def __init__(self, file: str, project: str, ref: Optional[str] = None) -> None:
        super().__init__(
            file=file,
            include_method=IncludeMethod.FILE,
            project=project,
            ref=ref,
        )


class RemoteInclude(Include):
    def __init__(self, url: str) -> None:
        super().__init__(file=url, include_method=IncludeMethod.REMOTE)


class TemplateInclude(Include):
    def __init__(self, file: str) -> None:
        super().__init__(file=file, include_method=IncludeMethod.TEMPLATE)
