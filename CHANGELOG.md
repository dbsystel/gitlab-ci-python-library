# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
* Added `gcip.addon.container.job.trivy.scan_local_image` to scan local container images of vulnerabilities.
* Added set_config_file_path method to DockerClientConfig.
* Return own instance on each method call for DockerClientConfig instances.
* Added Registry class to `gcip.addons.container.registry` module. It contains constants of Container registries.

### Changed
* Normalize config_file_path in `gcip.addons.container.config.DockerClientConfig`
* Line length check in flake8 linter to 160.
* **BREAKING** Removed arguments from DockerClientConfig constructor to set config file path, use `set_config_file_path` of DockerClientConfig instance.
* **BREAKING** Removed custom docker client config from kaniko job.
  Added DockerClientConfig as a optional client configuration to kaniko job.
  Simplyfied function and sorted initialisation tests an actuall composing of job.
* **BREAKING** Removed custom docker client config from kaniko job.
  Added DockerClientConfig as a optional client configuration to kaniko job.
  Simplyfied function and sorted initialisation tests an actuall composing of job.

### Removed
* Removed `date` call from dive job.

### Fixed
* Several linter issues has been fixed
* Fixed kaniko build in gitlabci-local.sh
* Kankio job's tar_path behavior fixed. If you specified tar_path in `kaniko.execute()`, the `tar_path` was added to the same line as the executor. Now it gets added to a item bevor `execute`.


## [0.6.1] - 2021-04-07

### Changed

* `PredefinedVariables` return in all cases a proxy object, which calls `os.environ` or `os.getenv` as late as possible.
  This helps when overriding (monkeypatching) variables in pytestes.

## [0.6.0] - 2021-04-06

### Added

* Added config.yml to .github dir to force using issue templates.
* Added gitlab_ci_environment_variables monkeypatch fixture. It allows patching environment variables.
* Added gitlab_ci_environmnet_variables fixture to tests.
* The gcip is now able to detect if two or more jobs would have the same name in the rendered pipeline
  and raises an ValueError to prevent undesirable pipeline behavior.
* Added new addon to check container optimization with `dive`
* Improved conftest.check() function. It tells the user how to create comparison files if the file not found exception.
* Improved `conftest.check()` function. Now AssertionError is handled, the user will get receive how to update comparison files.
* Added new class `PredefinedImages` in `gcip.addons.container`. Allows access to container images, that are widley used.
* Added new `class` which handels docker client config and renders it to a json string.
* Added `gcip.addon.container.job.crane` to allow copying container images between registries.
* Added `push` Job function to `gcip.addon.container.job.crane` to allow pushing local tarballs to remote registries.

### Changed

* **BREAKING** Renamed all occurences of 'job*sequence' to 'sequence'. Mainly this renames
  `gcip.core.job_sequence.JobSequence` to `gcip.core.sequence.Sequence`.
* Changed behavior how PredefinedVariables is handling environment variables.
  PredefinedVariables knows which environment variables are always present or under certain circumstances,
  like merge requests or if GitLab container registry is present.
  Variables marked with limited availabilty within official documentation returns String or None.
  All variables which are documented as always present return String.
* If the gcip code is executed outside a pipeline ($CI is empty) then for all expected `CI_*` variables
  a dummy string is returned instead of raising a KeyError.
* The `gcip.Pipeline` has now an `add_services()` method instead `add_service()` allowing to pass multiple
  services at once.
* Now jobs with hardcoded images, now using PredefinedImages images instead.


## [0.5.0] - 2021-03-16

### Added

* The CHANGELOG.md itself.
* Bug, Feature and Pull request templates (#9)

### Changed

* **BREAKING:** The signature of `gcip.addons.python.jobs.twine_upload()` has changed. The parameters `twine_repository_url`,
  `twine_username_env_var` and `twine_username_env_var` substitute the parameters `repository_url`, `user` and `varname_password`.
  Check the API documentation for the new parameters.
* **BREAKING:** Renamed all occurences of `pep404` to `pep440` as PEP 440 is the right specification number.

## [Template]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security
