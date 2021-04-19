# __author__ = "Thomas Steinbach"
# __copyright__ = "Copyright 2020 DB Systel GmbH"
# __credits__ = ["Daniel von Eßen"]
# # SPDX-License-Identifier: Apache-2.0
# __license__ = "Apache-2.0"
# __maintainer__ = "Daniel von Eßen"
# __email__ = "daniel.von-essen@deutschebahn.com"

# from typing import Any, Dict, List, Optional

# from gcip.core.rule import WhenStatement
# from gcip.core.variables import PredefinedVariables


# class Artifacts:
#     def __init__(
#         self,
#         paths: List[str],
#         *,
#         excludes: List[str] = [],
#         expire_in: Optional[str] = None,
#         expose_as: Optional[str] = None,
#         name: Optional[str] = None,
#         public: Optional[bool] = None,
#         untracked: Optional[bool] = None,
#         when: Optional[WhenStatement] = None,
#     ) -> None:
#         self._expire_in = expire_in
#         self._expose_as = expose_as
#         self._name = name if name else f"{PredefinedVariables.CI_JOB_NAME}-{PredefinedVariables.CI_COMMIT_REF_SLUG}"
#         self._public = public
#         self._untracked = untracked
#         self._when = when

#         # Remove project path prefix from paths given.
#         # Prepend ./ to path to clearify that cache paths
#         # are relative to CI_PROJECT_DIR
#         self._paths = [path if not path.startswith(PredefinedVariables.CI_PROJECT_DIR) else path[len(PredefinedVariables.CI_PROJECT_DIR) :] for path in paths]
#         if len(excludes) > 0:
#             self._excludes = [
#                 exclude if not exclude.startswith(PredefinedVariables.CI_PROJECT_DIR) else exclude[len(PredefinedVariables.CI_PROJECT_DIR) :]
#                 for exclude in excludes
#             ]

#     @property
#     def paths(self):
#         return self._paths

#     @property
#     def excludes(self):
#         return self._excludes

#     @property
#     def expire_in(self):
#         return self._expire_in

#     @property
#     def expose_as(self):
#         return self._expose_as

#     @property
#     def name(self):
#         return self._name

#     @property
#     def public(self):
#         return self._public

#     @property
#     def untracked(self):
#         return self._untracked

#     @property
#     def when(self):
#         return self._when

#     def render(self) -> Dict[str, Any]:
#         """Return a representation of this Cache object as dictionary with static values.

#         The rendered representation is used by the gcip to dump it
#         in YAML format as part of the .gitlab-ci.yml pipeline.

#         Returns:
#             Dict[str, Any]: A dictionary prepresenting the cache object in Gitlab CI.
#         """
#         rendered: Dict[str, Union[str, bool, List[str], Union[str, Dict[str, Union[List[str], str]]]]]
#         rendered = {
#             "paths": self.paths,
#             "name": self.name,
#         }
#         if self.excludes:
#             rendered["excludes"] = self.excludes
#         if self.expire_in:
#             rendered["expire_in"] = self.expire_in
#         if self.expose_as:
#             rendered["expose_as"] = self.expose_as
#         if self.expose_as:
#             rendered["expose_as"] = self._policy.value
#         if self.expose_as:
#             rendered["expose_as"] = self._policy.value
#         if self.expose_as:
#             rendered["expose_as"] = self._policy.value
#         rendered["key"] = self._cache_key.render()

#         return rendered
