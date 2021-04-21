__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Daniel von Eßen"
__email__ = "daniel.von-essen@deutschebahn.com"

from typing import Optional

from gcip.addons.aws.helper import (
    aws_region,
    aws_account_id,
)


class Registry:
    """
    Container registry urls constants.
    """

    DOCKER: str = "index.docker.io"
    QUAY: str = "quay.io"
    GCR: str = "gcr.io"

    @staticmethod
    def AWS(*, account_id: Optional[str] = None, region: Optional[str] = None) -> str:
        """Amazon Elastic Container Registry (ECR).

        If neither `account_id` nor `region` is given, method tries to evaluate `account_id` and `region`
        with helper functions from `gcip.addons.aws.helper`. If one of the helper functions, do not
        resolve to an appropriate value they will throw a `ValueError` or `KeyError` exception.

        Args:
            account_id (Optional[str]): AWS account id. Defaults internally to `gcip.addons.aws.helper.aws_account_id()`.
            region (Optional[str]): AWS region where the ECR repository lives in. Defaults internally to `gcip.addons.aws.helper.aws_region`.

        Raises:
            ValueError: If no region was found in `gcip.addons.aws.helper.aws_region()`.
            ValueError: If aws account id to resolvable from `gcip.addons.aws.helper.aws_account_id()`.

        Returns:
            str: Elastic Container Registry URL in format of **aws_account_id.dkr.ecr.region.amazonaws.com**
        """
        if not account_id:
            account_id = aws_account_id()
        if not region:
            region = aws_region()

        return f"{account_id}.dkr.ecr.{region}.amazonaws.com"
