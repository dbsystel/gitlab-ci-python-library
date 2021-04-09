import re

__author__ = "Daniel von Eßen"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "daniel.von-essen@deutschebahn.com"


def is_valid_url(url: str) -> bool:
    """
    Validates given `url`.

    Implementation details
        1. https://stackoverflow.com/a/7160778
        2. https://github.com/django/django/blob/6726d750979a7c29e0dd866b4ea367eef7c8a420/django/core/validators.py#L45

    Args:
        url (str): Uniform Resource Locator (URL) to check.

    Returns:
        bool: ``True`` if ``url`` is valid. If not, ``False`` is returned.
    """
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(regex, url) is not None
