from gcip.core.image import Image


class PredefinedImages():
    """
    PredefinedImages provides container images objects that are widley used withing the `gcip`.
    """
    KANIKO: Image = Image("gcr.io/kaniko-project/executor:debug", entrypoint=[""])
    CRANE: Image = Image("gcr.io/go-containerregistry/crane:latest")
    DIVE: Image = Image("wagoodman/dive:latest")
    GCIP: Image = Image("thomass/gcip:0.3.0")
    TRIVY: Image = Image("aquasec/trivy:latest")
