from typing import Optional

from ..helpers import is_valid_url


class Include():
    def __init__():
        pass

    def render(self):
        return self._rendered_include


class IncludeLocal(Include):
    def __init__(self, local: str):
        self._rendered_include = {
            "local": local
        }


class IncludeFile(Include):
    def __init__(
        self,
        file: str,
        project: str,
        ref: Optional[str] = None,
    ):
        self._rendered_include = {
            "file": file,
            "project": project
        }
        if ref:
            self._rendered_include["ref"] = ref


class IncludeRemote(Include):
    def __init__(self, remote: str):
        if not is_valid_url(remote):
            raise ValueError(f"`remote` is not a valid URL: {remote}")

        self._rendered_include = {
            "remote": remote
        }


class IncludeTemplate(Include):
    def __init__(self, template: str):
        self._rendered_include = {
            "template": template
        }


class IncludeArtifact(Include):
    """for triggering a child pipeline with generated configuration file"""
    def __init__(self, job: str, artifact: str):
        self._rendered_include = {
            "job": job,
            "artifact": artifact
        }
