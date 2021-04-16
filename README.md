# gcip - Write your Gitlab CI pipelines in Python

The Gitlab CI Python Library (gcip) is a Library to create dynamic pipelines for Gitlab CI.

[User Documentation](https://dbsystel.github.io/gitlab-ci-python-library/user/index.html) | [API Reference](https://dbsystel.github.io/gitlab-ci-python-library/api/gcip/index.html)

With the gcip and the ease and power of Python you can write Gitlab CI pipelines
of any complexity in well manageable Python code.

A simple starting pipeline could look like following:

```
from gcip import Pipeline, Job

pipeline = Pipeline()
pipeline.add_children(Job(namespace="build", script="docker build ."))
pipeline.write_yaml()
```

Here is a prospect of how you can handle complex pipelines in Python:

```
from gcip import Pipeline, JobSequence, Job
from gcip.addons.gitlab import job_scripts as gitlab


def get_build_deploy_sequence(environment: str):
    return JobSequence().add_children(
        Job(namespace="build", script=f"docker build -t myimage-{environment} ."),
        Job(namespace="deploy", script=["docker login", f"docker push myimage-{environment}"]),
    )


pipeline = Pipeline()
pipeline.initialize_image("my/enterprise/build-image:stable")

for environment in ("develop", "test", "production"):
    jobs = get_build_deploy_sequence(environment)
    jobs.prepend_scripts(
        gitlab.clone_repository(path="projectx/configuration", branch=environment),
        f"source {environment}.env",
    )
    jobs.add_tags(environment)

    pipeline.add_children(jobs, namespace=environment)

pipeline.write_yaml("generated-config.yml")
```

Do you really want to see the [generated-config.yml](docs/user/generated-config.yml) ? :)

## Documentation

Please read the [User Documentation](https://dbsystel.github.io/gitlab-ci-python-library/user/index.html) to get a quick introduction into most
features of the gcip.

You can consult the [API Reference](https://dbsystel.github.io/gitlab-ci-python-library/api/gcip/index.html) to get an overview of all classes and methods
and a deeper view into their paramters.

## IDE setup hints

To participate onto this project and get into it as quick as possible, we advice to use our Visual Studio Code configuration shipped with this project. To activate:

* Install Docker.
* In VSCode CMD+Shift+P and select "Remote-Containers: Reopen in Container"

Feel free to use any other editor you like, as long as you will ensure following quality requirements before contributing your commits:

* Organizing and sorting imports with `isort`.
* Formatting code with `black`.
* Type checking with `mypy`.
* Unit testing with `pytest`.

The VSCode settings delivered will do most of that automatically (organize imports, formatting, type checking) or setup the required tools (unit testing with code coverage).

## Why is this Gitlab Project hosted on Github?

The [DB Systel GmbH](https://github.com/dbsystel) organization sponsoring this project is currently only present on Github.
This may be change in future.


## Author

gcip was created by [Thomas Steinbach](mailto:thomas.t.steinbach@deutschebahn.com) in 2020.

Thanks to initial contributions from [Daniel von Eßen](mailto:daniel.von-essen@deutschebahn.com)

## Licence

The content of this repository is licensed under the [Apache 2.0 license](http://www.apache.org/licenses/LICENSE-2.0).

Copyright DB Systel GmbH
