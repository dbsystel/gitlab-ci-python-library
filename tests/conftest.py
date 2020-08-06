from typing import Any

import pydash


# https://pydash.readthedocs.io/en/latest/api.html#pydash.predicates.is_match_with
def _set_comparison(a: Any, b: Any) -> bool:
    return (not isinstance(a, set) and not isinstance(b, set)) or (isinstance(a, set) and isinstance(b, set) and set(a) == set(b))


def dict_a_contains_b(a: dict, b: dict) -> bool:
    """
    https://stackoverflow.com/a/54696573/1768273
    """
    match = pydash.predicates.is_match_with(a, b, _set_comparison)
    if not match:
        import yaml
        print("Dictionary a should be a superset of b but isn't")
        print("a is:")
        print(yaml.safe_dump(a))
        print("----------------------------")
        print("b is:")
        print(yaml.safe_dump(b))

    return match
