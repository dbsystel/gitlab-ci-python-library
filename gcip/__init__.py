"""#gcip API reference

## project structure and terminology of artifacts

To keep this source code folder as clean as possible, all code files are sorted into one of these folders:

* core
* lib
* tools
* addons

The **core** folder contains, as the name implies, all the core components that represent Gitlab CI objects in Python.
You need to know that all class names from all Python modules within the ```core``` folder are mapped to the gcip
root module. This is done within the ```__init__.py``` of the gcip folder. Instead of ```import gcip.core.job.Job```
you should ```import gcip.Job```. You should import all classes of the ```core``` folder the same way.

Always remember:

```
# Dos:
from gcip import Pipeline, Job, Sequence  # ... and so on

pipeline = Pipeline()
```

```
# Dont's
from gcip.core import pipeline, job

pipeline = pipeline.Pipeline()
```

The **lib** folder contains all higher level objects which are derived from the ```core``` objects. For example: `gcip.Rule`
from _gcip.core.rule_ is the general Gitlab CI Rule representation, whereas ```core.rules``` contains some convenient
predefined Rule instances like ```on_main()``` or ```on_tags()```.

The **tools** folder contains all code which is used by the library code but does not represent any Gitlab CI specific
functionality. This directory also contains scripts which could be run on their own and are supposed to be called
by Gitlab CI jobs during the pipeline execution. For example ```gcip.tools.url.is_valid_url(str)``` which, as the name implies,
checks if `str` is a valid url.

The **addons** folder also contains code which extends the core components in form of higher level objects that provide
functionality for a specific use case. A use case could be _python_, _ruby_, _cloudformation_, _ansible_ et cetera.
Every subdirectory of _addons_ has the name of such a use case. The name _addons_ is chosen by the intention that
in future the subdirectories will be outsourced into separate projects. This could be the case when the core library
is stable enough to not hinder the development of the downstream addons projects and the addons were too many to
be maintained within the core library. However at this point the project is small enough to provide the core and
add on functionality in an easy to use all-in-one package.

We also use a following naming conventions throughout the library:

* Files called ```_job_scripts.py``` hold functions that return strings, which could be used as command within
Gitlab CI jobs.
* Directories called _tools_ hold Python scripts which could be called by Gitlab CI jobs during the pipeline
execution. They will be called directly from the Gitlab CI Python library, e.g. ```python3 -m gcip.path.to.script```.
"""

from pkg_resources import (
    DistributionNotFound as _DistributionNotFound,
    get_distribution as _get_distribution,
)

# yapf: disable
from .core.job import (  # noqa
    Job,
    TriggerJob,
    TriggerStrategy,
)
from .core.need import Need  # noqa
# yapf: disable
from .core.rule import Rule, WhenStatement  # noqa
# yapf: disable
from .core.cache import Cache, CacheKey, CachePolicy  # noqa
# yapf: disable
from .core.image import Image  # noqa
# yapf: disable
from .core.include import (  # noqa
    IncludeFile,
    IncludeLocal,
    IncludeRemote,
    IncludeArtifact,
    IncludeTemplate,
)
# yapf: disable
from .core.pipeline import Pipeline  # noqa
from .core.variables import PredefinedVariables  # noqa
from .core.job_sequence import JobSequence  # noqa

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = 'Apache-2.0'
__maintainer__ = 'Thomas Steinbach'
__email__ = 'thomas.t.steinbach@deutschebahn.com'

try:
    _distribution = _get_distribution("gcip")
    __version__ = _distribution.version
except _DistributionNotFound:
    __version__ = "unknown"
