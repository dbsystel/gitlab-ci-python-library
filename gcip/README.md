# gcip code documentation

## project structure and terminology of artifacts

To keep this source code folder as clean as possible, all code files are sorted into one of these folders:

* \_core
* lib
* tools
* addons

The _\_core_ folder holds, as the name implies, all the core components that represent Gitlab CI objects in Python.
You need to know that all class names from all Python modules within the `_core` folder are mapped to the gcip
root module. This is done within the `__init__.py` of the gcip folder. Instead of `import gcip._core.job.Job`
you should `import gcip.Job`. You should import all classes of the `_core` folder in the same way.

The _lib_ folder holds all higher level objects which are derived from the _core_ objects.

The _tools_ folder holds all code which is used by the library code but does not represent any Gitlab CI specific
functionality. This directory also contains scripts which could be run on their own and are supposed to be called
by Gitlab CI jobs during the pipeline execution.

The _addons_ folder also holds code which extends the core components in form of higher level objects that provide
functionality for a specific use case. A use case could be _python_, _ruby_, _cloudformation_, _ansible_ et cetera.
Every subdirectory of _addons_ has the name of such a use case. The name _addons_ is chosen by the intention that
in future the subdirectories will be outsourced into separate projects. This could be the case when the core library
is stable enough to not hinder the development of the downstream addons projects and the addons are too many to
be maintained within the core library. However at this point the project is small enough to provide the core and
add on functionality in an easy to use all-in-one package.

We also use a naming convention, which should make the structuring more clear:

* Files called _helpers.py_ hold python functions solves an isolated task that potentially could be used multiple
  times accross the library.
* Files called _job_scripts.py_ hold functions that return strings, which could be used as a script call within
  Gitlab CI job script sections.
* Directories called _tools_ hold Python scripts which could be called by Gitlab CI jobs during the pipeline
  execution. They will be called directly from the Gitlab CI Python library, e.g. `python3 -m gcip.path.to.script`.
