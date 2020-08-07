import pydash


def dict_a_contains_b(a: dict, b: dict) -> bool:
    """
    https://stackoverflow.com/a/54696573/1768273
    """
    match = pydash.predicates.is_match(a, b)
    if not match:
        import yaml
        print("Dictionary a should be a superset of b but isn't")
        print("a is:")
        print(yaml.safe_dump(a))
        print("----------------------------")
        print("b is:")
        print(yaml.safe_dump(b))

    return match
