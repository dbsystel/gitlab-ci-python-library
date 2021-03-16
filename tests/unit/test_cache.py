import pytest

from gcip import Cache, CacheKey, CachePolicy, WhenStatement


def test_cache_policies():
    expected_members = ["PULL", "PULL_PUSH"]
    for member in CachePolicy.__members__:
        assert member in expected_members


def test_default_cache_key_matches_ci_commit_ref_slug(gitlab_ci_environment_variables):
    cache_key = CacheKey()
    expected_render = "my-awsome-feature-branch"
    assert expected_render == cache_key.render()
    assert cache_key.key == "my-awsome-feature-branch"
    assert cache_key.files is None
    assert cache_key.prefix is None


def test_cache_key_with_custom_value():
    cache_key = CacheKey(key="mykey")
    expected_render = "mykey"
    assert expected_render == cache_key.render()
    assert cache_key.key == "mykey"
    assert cache_key.files is None
    assert cache_key.prefix is None


def test_cache_key_with_files():
    cache_key = CacheKey(files=["filea", "fileb", "filec"])
    expected_render = {
        "files": ["filea", "fileb", "filec"]
    }
    assert expected_render == cache_key.render()
    assert cache_key.key is None
    assert cache_key.files == ["filea", "fileb", "filec"]
    assert cache_key.prefix is None


def test_cache_key_files_prefix():
    cache_key = CacheKey(files=["filea", "fileb", "filec"], prefix="myprefix")
    expected_render = {
        "files": ["filea", "fileb", "filec"],
        "prefix": "myprefix"
    }
    assert expected_render == cache_key.render()
    assert cache_key.key is None
    assert cache_key.files == ["filea", "fileb", "filec"]
    assert cache_key.prefix == "myprefix"


def test_cache_key_exceptions():
    with pytest.raises(ValueError):
        CacheKey(key="mykey", files=["filea", "fileb", "filec"])
        CacheKey(key="mykey", prefix="myprefix")
        CacheKey(prefix="myprefix")
        CacheKey(key="...")
        CacheKey(key="my/key")


def test_cache(gitlab_ci_environment_variables):
    cache = Cache(paths=["path1", "path/two", "./path/three"])
    expected_render = {
        "key": "my-awsome-feature-branch",
        "paths": ["./path1", "./path/two", "./path/three"]
    }
    assert expected_render == cache.render()
    assert cache.cache_key.render() == "my-awsome-feature-branch"
    assert cache.paths == ["./path1", "./path/two", "./path/three"]
    assert cache.policy is None
    assert cache.untracked is None
    assert cache.when is None


def test_full_featured_cache():
    cache = Cache(
        paths=["path1", "path/two", "./path/three"],
        cache_key=CacheKey(key="mykey"),
        untracked=True,
        when=WhenStatement.ON_FAILURE,
        policy=CachePolicy.PULL
    )
    expected_render = dict(key="mykey", paths=["./path1", "./path/two", "./path/three"], untracked=True, when="on_failure", policy="pull")
    assert expected_render == cache.render()
    assert cache.cache_key.render() == "mykey"
    assert cache.paths == ["./path1", "./path/two", "./path/three"]
    assert cache.policy.value == "pull"
    assert cache.untracked is True
    assert cache.when == WhenStatement.ON_FAILURE
