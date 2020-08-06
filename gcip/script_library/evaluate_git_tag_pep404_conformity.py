import os
import re
import sys


# https://www.python.org/dev/peps/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions
def is_canonical(version: str) -> bool:
    return re.match(
        r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$',
        version
    ) is not None


if __name__ == "__main__":
    ci_commit_tag = os.getenv('CI_COMMIT_TAG')
    
    if ci_commit_tag is None:
        raise ValueError("Environment variable CI_COMMIT_TAG must be set.")

    if is_canonical(ci_commit_tag):
        sys.exit()

    print(f"'{ci_commit_tag}' is not a valid Python package version.")
    print('See https://www.python.org/dev/peps/pep-0440')
    sys.exit(1)
