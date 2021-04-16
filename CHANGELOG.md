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
* Added `gcip.core.sequence.Sequence.initialize_artifacts_paths()` and `gcip.core.sequence.Sequence.override_artifacts_paths()`.
* Added defaulting to git tag or git branch for image_tag in `crane.push`.
* Added default `DockerClientConfig` in `crane.push`
* Added `|tee` to get `dive` output to stdout and to dive.txt. Updload dive.txt to GitLab artifacts store.
* Added `|tee` to get `trivy` output to stdout and to trivy.txt. Updload trivy.txt to GitLab artifacts store.
* Added new container sequence. Container sequence build, scans and pushes an container image.
* Added full API documentation of the `gcip.core.job` module.
* Added full API documentation of the `gcip.core.pipeline` module.
* Added full API documentation of the `gcip.core.image` module.
* Added full API documentation of the `gcip.core.include` module.
* Added documentation to the `gcip.core.variables` module.

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
* **BREAKING** Moved all function arguments of `crane.push` function to be keyword arguments.
* **BREAKING** Renamed `dst` to `dst_registry` in `crane.push` function.
* **BREAKING** Renamed `image_path` to `tar_path` keyword argument to aligne with kaniko module.
* **BREAKING** Renamed `dst` and `src` to `dst_registry` and `src_registry`.
* **BREAKING** `dive`: Replace "/" with "_" in image_name. Image names contains namespaces which are separated by "/" to ensure image name is a file instead of a directory structure.
* **BREAKING** `trivy`: Replace "/" with "_" in image_name. Image names contains namespaces which are separated by "/" to ensure image name is a file instead of a directory structure.
* **BREAKING** Renamed `gitlab_executor_image` to `kaniko_image` in `kaniko.execute()`. Moved argument to last argument in function signature.
* `kaniko`: Replaced "/" with "_" to convert image namspaces to filename instead of directory structure assigne it to image_path.
* `core.cache`: Changed PredefinedVariable from CI_PROJECT_PATH to CI_PROJECT_DIR to ensure its the directory instead of the "namespace" of the git repository.
* **BREAKING** Changed docker hub registry entry in `Registry` class.
* **BREAKING** Renamed all occurences of `namespace` to `stage`. Because 'stage' is what the current 'stage' really expresses. You could try following commands to align your
  gcip code with this breaking change:
  ```
  LC_ALL=C find . -type f ! -path './.git/*' ! -path '*/__pycache__/*' -exec sed -i '' s/Stage/Stage/g {} +
  LC_ALL=C find . -type f ! -path './.git/*' ! -path '*/__pycache__/*' -exec sed -i '' s/stage/stage/g {} +
  ```

### Removed
* Removed `date` call from dive job.
* Removed `gcip.core.pipeline.Pipeline.dump_yaml()` method. There is no need to print a pipeline to stdout. You should use `gcip.core.pipeline.Pipeline.write_yaml()` instead.

### Fixed
* Several linter issues has been fixed
* Fixed kaniko build in gitlabci-local.sh
* Kankio job's tar_path behavior fixed. If you specified tar_path in `kaniko.execute()`, the `tar_path` was added to the same line as the executor. Now it gets added to a item bevor `execute`.
* Fixed PredefinedImages entrypoints for GitLab CI runner.
* Fixed crane image, `latest` image does not have `sh` available. Using `debug` tag.
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
