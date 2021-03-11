from abc import ABCMeta
from typing import Dict, Optional

from ..tools.url import is_valid_url

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'


class Include(metaclass=ABCMeta):

    _rendered_include: Dict[str, str]

    def render(self) -> Dict[str, str]:
        return self._rendered_include


class IncludeLocal(Include):
    def __init__(self, local: str) -> None:
        self._rendered_include = {
            "local": local
        }


class IncludeFile(Include):
    def __init__(
        self,
        file: str,
        project: str,
        ref: Optional[str] = None,
    ) -> None:
        self._rendered_include = {
            "file": file,
            "project": project
        }
        if ref:
            self._rendered_include["ref"] = ref


class IncludeRemote(Include):
    def __init__(self, remote: str) -> None:
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
