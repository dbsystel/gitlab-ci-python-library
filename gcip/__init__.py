from pkg_resources import (
    DistributionNotFound as _DistributionNotFound,
    get_distribution as _get_distribution,
)

from ._core.job import (  # noqa
    Job,
    Need,
    TriggerJob,
    TriggerStrategy,
)
from ._core.rule import Rule  # noqa
from ._core.include import (  # noqa
    IncludeFile,
    IncludeLocal,
    IncludeRemote,
    IncludeArtifact,
    IncludeTemplate,
)
from ._core.pipeline import Pipeline  # noqa
from ._core.job_sequence import JobSequence  # noqa

try:
    _distribution = _get_distribution("gcip")
    __version__ = _distribution.version
    __doc__ = _distribution.project_name
except _DistributionNotFound:
    __version__ = "unknown"
