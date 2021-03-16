# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* Added config.yml to .github dir to force using issue templates.
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
