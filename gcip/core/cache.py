"""This module represents the Gitlab CI [cache](https://docs.gitlab.com/ee/ci/yaml/#cache) keyword
"""

import re
from enum import Enum
from typing import Any, Dict, List, Union, Optional

from gcip.core.rule import WhenStatement
from gcip.core.variables import PredefinedVariables


class CachePolicy(Enum):
    """This class represents the [cache:policy](https://docs.gitlab.com/ee/ci/yaml/#cachepolicy) keyword.

    The policy determines if a Job can modify the cache or read him only.
    """

    PULL_PUSH = "pull-push"
    """
    The default behavior of a caching job is to download the files at the start of execution, and to
    re-upload them at the end. Any changes made by the job are persisted for future runs.
    """

    PULL = "pull"
    """
    If you know the job does not alter the cached files, you can skip the upload step by setting this policy in the job specification.
    """


class CacheKey():
    """This class represents the [cache:key](https://docs.gitlab.com/ee/ci/yaml/#cachekey) keyword.

    Gitlab CI documentation: _"The key keyword defines the affinity of caching between jobs. You can have a single cache for
    all jobs, cache per-job, cache per-branch, or any other way that fits your workflow."_

    Args:
        key (Optional[str]): The key is the unique id of the cache. `gcip.core.job.Job`s referencing caches with the same key are
            sharing the cache contents. Mutually exclusive with `files`. Defaults to
            `gcip.core.variables.PredefinedVariables.CI_COMMIT_REF_SLUG` if neither `key` nor `files` is set.
        files (Optional[list]): A set of files is another way to define a caches unique id. Jobs referencing caches with the same
            set of files are sharing the cache contents. The [cache:key:files](https://docs.gitlab.com/ee/ci/yaml/#cachekeyfiles) keyword
            extends the cache:key functionality by making it easier to reuse some caches, and rebuild them less often, which speeds up
            subsequent pipeline runs. Mutually exclusive with `keys`. Defaults to None.
        prefix (Optional[str]): Prefix prefixed given `files` to allow creation of caches for branches. Defaults to None.

    Raises:
        ValueError: If both `key` and `files` are provided.
        ValueError: If both `key` and `prefix` are provided.
        ValueError: If `prefix` but not `files` is provided.
        ValueError: If `key` is only made out of dots '.'.
    """
    def __init__(self, key: Optional[str] = None, files: Optional[List[str]] = None, prefix: Optional[str] = None) -> None:
        self._key = key
        self._files = files
        self._prefix = prefix

        if self._key and self._files:
            raise ValueError("Parameters key and files are mutually exclusive.")
        elif self._prefix and not self._files:
            raise ValueError("Parameter 'prefix' can only be used together with 'files'.")

        if self._files is None and self._key is None:
            self._key = PredefinedVariables.CI_COMMIT_REF_SLUG

        if self._key:
            # Forward slash not allowed for cache key,
            # therefore converting slash to underscore
            self._key.replace("/", "_")

            if re.match(r"^\.*$", self._key):
                raise ValueError("The cache key cannot be a value only made of '.'")

    @property
    def key(self) -> Optional[str]:
        """Equals the identical Class argument."""
        return self._key

    @property
    def files(self) -> Optional[List[str]]:
        """Equals the identical Class argument."""
        return self._files

    @property
    def prefix(self) -> Optional[str]:
        """Equals the identical Class argument."""
        return self._prefix

    def render(self) -> Union[str, Dict[str, Union[List[str], str]]]:
        """Renders the class as string or dict.

        The rendered representation is used by the gcip to dump it
        in YAML format as part of the .gitlab-ci.yml pipeline.

        Returns:
            Union[str, Dict[str, Union[List[str], str]]]: A string or dictionary prepresenting the cache object in Gitlab CI.
        """
        rendered: Union[str, Dict[str, Union[List[str], str]]]
        if self._key:
            rendered = self._key
        else:
            rendered = {}
            if self._files:
                rendered["files"] = self._files
            if self._prefix:
                rendered["prefix"] = self._prefix
        return rendered


class Cache():
    """This class represents the [cache](https://docs.gitlab.com/ee/ci/yaml/#cache) keyword.

    Gitlab CI documentation: _"Use cache to specify a list of files and directories to cache between `gcip.core.job.Job`s.
    [...] Caching is shared between `gcip.core.pipeline.Pipeline`s and `gcip.core.job.Job`s. Caches are restored before artifacts."_

    Args:
        paths (List[str]): Paths to create the cache to.
        cache_key (Optional[CacheKey]): Cache key which is used to share the cache.
            If None, cache_key will be initialized with an empty CacheKey. See class CacheKey
        untracked (Optional[bool]): If true, cache will cache all untracked files within project path. Defaults to None.
        when (Optional[WhenStatement]): Defines when to save the cache, depending on job status.
            Possible values are WhenStatement.ON_SUCCESS, WhenStatement.ON_FAILURE, WhenStatement.ALWAYS Defaults to None.
        policy (Optional[CachePolicy]): There are two policies, pull and push-pull.
            Use pull policy if you know, that the job does not alter the files within the cache. Defaults to None.

    Raises:
        ValueError: When unallowed WhenStatements are used.
    """
    def __init__(
        self,
        paths: List[str],
        cache_key: Optional[CacheKey] = None,
        untracked: Optional[bool] = None,
        when: Optional[WhenStatement] = None,
        policy: Optional[CachePolicy] = None,
    ) -> None:
        self._paths = []
        self._untracked = untracked
        self._when = when
        self._policy = policy

        # Remove project path prefix from paths given.
        # Prepend ./ to path to clearify that cache paths
        # are relative to CI_PROJECT_PATH
        for path in paths:
            if PredefinedVariables.CI_PROJECT_PATH and path.startswith(PredefinedVariables.CI_PROJECT_PATH):
                path = path[len(PredefinedVariables.CI_PROJECT_PATH):]

            if not path.startswith("./"):
                path = "./" + path
            self._paths.append(path)

        # Get default CacheKey = PredefinedVariables.CI_COMMIT_REF_SLUG
        if cache_key:
            self._cache_key = cache_key
        else:
            self._cache_key = CacheKey()

        allowed_when_statements = [WhenStatement.ON_SUCCESS, WhenStatement.ON_FAILURE, WhenStatement.ALWAYS]
        if self._when and self._when not in allowed_when_statements:
            raise ValueError(f"{self._when} is not allowed. Allowed when statements: {allowed_when_statements}")

    @property
    def paths(self) -> List[str]:
        """Equals the identical Class argument."""
        return self._paths

    @property
    def cache_key(self) -> CacheKey:
        """Equals the identical Class argument."""
        return self._cache_key

    @property
    def untracked(self) -> Optional[bool]:
        """Equals the identical Class argument."""
        return self._untracked

    @property
    def when(self) -> Optional[WhenStatement]:
        """Equals the identical Class argument."""
        return self._when

    @property
    def policy(self) -> Optional[CachePolicy]:
        """Equals the identical Class argument."""
        return self._policy

    def render(self) -> Dict[str, Any]:
        """Rendering method to rendere object into GitLab CI object.

        Returns:
            Dict[str, Union[str, list]]: Configuration of a GitLab cache.
        """
        rendered: Dict[str, Union[str, bool, List[str], Union[str, Dict[str, Union[List[str], str]]]]]
        rendered = {
            "paths": self._paths
        }
        if self._when:
            rendered["when"] = self._when.value
        if self._untracked:
            rendered["untracked"] = self._untracked
        if self._policy:
            rendered["policy"] = self._policy.value
        rendered["key"] = self._cache_key.render()

        return rendered
