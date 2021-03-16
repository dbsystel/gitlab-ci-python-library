# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* Added config.yml to .github dir to force using issue templates.
* Added gitlab_ci_environment_variables monkeypatch fixture. It allows patching environment variables.
* Added gitlab_ci_environmnet_variables fixture to tests.

### Changed

* **BREAKING** Renamed all occurences of 'job\w*sequence' to 'sequence'. Mainly this renames
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
