__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Daniel von Eßen"
__email__ = "daniel.von-essen@deutschebahn.com"

from gcip.core.image import Image


class PredefinedImages:
    """
    PredefinedImages provides container images objects that are widley used withing the `gcip`.
    """

    KANIKO: Image = Image("gcr.io/kaniko-project/executor:debug", entrypoint=[""])
    CRANE: Image = Image("gcr.io/go-containerregistry/crane:latest")
    DIVE: Image = Image("wagoodman/dive:latest")
    GCIP: Image = Image("thomass/gcip:0.3.0")
    TRIVY: Image = Image("aquasec/trivy:latest")
