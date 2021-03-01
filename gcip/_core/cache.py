import re
from enum import Enum
from typing import Dict, List, Union, Optional

from gcip._core.rule import WhenStatement
from gcip._core.environment import GitLabCiEnv


class CachePolicy(Enum):
    """Static cache policies.
    Used to initialize policy in conjunction with Cache object.
    """
    PULL_PUSH = "pull-push"
    PULL = "pull"


class CacheKey():
    def __init__(self, key: Optional[str] = None, files: Optional[list] = None, prefix: Optional[str] = None) -> None:
        """Creates an object which represents an `key` within cache.

        For more information what a `cache` and its `key` is see: https://docs.gitlab.com/ee/ci/yaml/README.html#cachekey

        Args:
            key (Optional[str], optional): Name of the key, used to share the cache with jobs, exclusive with `files`.
            Defaults to GitLabCiEnv.CI_COMMIT_REF_SLUG() if neither `key` nor `file` is set.

            files (Optional[list], optional): Files which can be used to create the cache key, exclusive to `keys`. Defaults to None.
            prefix (Optional[str], optional): Prefix prefixed given `files` to allow creation of caches for branches. Defaults to None.

        Raises:
            ValueError: If `key` and `files` are given at the same time.
            ValueError: If `key` and `prefix` are given at the same time.
            ValueError: If `prefix` and not `files` is given.
            ValueError: If `key` contains only out of dots '.'.
        """
        self._key = key
        self._files = files
        self._prefix = prefix

        if self._key and self._files:
            raise ValueError("Parameters key and files are mutually exclusive.")
        elif self._prefix and not self._files:
            raise ValueError("Parameter 'prefix' can only be used together with 'files'.")

        if self._files is None and self._key is None:
            self._key = GitLabCiEnv.CI_COMMIT_REF_SLUG()

        if self._key:
            # Forward slash not allowed for cache key,
            # therefore converting slash to underscore
            self._key.replace("/", "_")

            if re.match(r"^\.*$", self._key):
                raise ValueError("The cache key cannot be a value only made of '.'")

    @property
    def key(self) -> str:
        return self._key

    @property
    def files(self) -> list:
        return self._files

    @property
    def prefix(self) -> str:
        return self._prefix

    def render(self) -> Union[str, Dict[str, dict]]:
        """Renders the class into a python dictionary.

        Example1:
        python```
        print(CacheKey(key="mycachekey").render())
            -> 'mycachekey'
        ```
        Example2:
        python```
        print(CacheKey(files=["requirements.txt", "setup.py"], prefix="myprefix").render())
            -> {'files': ['requirements.txt', 'setup.py'], 'prefix': 'myprefix'}
        ```

        Returns:
            Dict[str, Any]: Dictionary representing a cache object in Gitlab CI.
        """
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
    def __init__(
        self,
        paths: List[str],
        cache_key: Optional[CacheKey] = None,
        untracked: Optional[bool] = None,
        when: Optional[WhenStatement] = None,
        policy: Optional[CachePolicy] = None,
    ) -> None:
        """Creates

        Args:
            paths (List[str]): Paths to create the cache to.
            cache_key (Optional[CacheKey], optional): Cache key which is used to share the cache.
            If None, cache_key will be initialized with an empty CacheKey. See class CacheKey
            untracked (Optional[bool], optional): If true, cache will cache all untracked files within project path. Defaults to None.
            when (Optional[WhenStatement], optional): Defines when to save the cache, depending on job status.
            Possible values are WhenStatement.ON_SUCCESS, WhenStatement.ON_FAILURE, WhenStatement.ALWAYS Defaults to None.
            policy (Optional[CachePolicy], optional): There are two policies, pull and push-pull.
            Use pull policy if you know, that the job does not alter the files within the cache. Defaults to None.

        Raises:
            ValueError: When unallowed WhenStatements are used.
        """
        self._paths = []
        self._cache_key = cache_key
        self._untracked = untracked
        self._when = when
        self._policy = policy

        # Remove project path prefix from paths given.
        # Prepend ./ to path to clearify that cache paths
        # are relative to CI_PROJECT_PATH
        for path in paths:
            if path.startswith(GitLabCiEnv.CI_PROJECT_PATH()):
                path = path[len(GitLabCiEnv.CI_PROJECT_PATH()):]

            if not path.startswith("./"):
                path = "./" + path
            self._paths.append(path)

        # Get default CacheKey = GitLabCiEnv.CI_COMMIT_REF_SLUG()
        if not self._cache_key:
            self._cache_key = CacheKey()

        allowed_when_statements = [WhenStatement.ON_SUCCESS, WhenStatement.ON_FAILURE, WhenStatement.ALWAYS]
        if self._when and self._when not in allowed_when_statements:
            raise ValueError(f"{self._when} is not allowed. Allowed when statements: {allowed_when_statements}")

    @property
    def paths(self) -> List[str]:
        return self._paths

    @property
    def cache_key(self) -> CacheKey:
        return self._cache_key

    @property
    def untracked(self) -> Optional[bool]:
        return self._untracked

    @property
    def when(self) -> Optional[WhenStatement]:
        return self._when

    @property
    def policy(self) -> Optional[CachePolicy]:
        return self._policy

    def render(self) -> Dict[str, Union[str, list]]:
        """Rendering method to rendere object into GitLab CI object.

        Returns:
            Dict[str, Union[str, list]]: Configuration of a GitLab cache.
        """
        rendered = {"paths": self._paths}
        if self._when:
            rendered["when"] = self._when.value
        if self._untracked:
            rendered["untracked"] = self._untracked
        if self._policy:
            rendered["policy"] = self._policy.value
        rendered["key"] = self._cache_key.render()

        return rendered
