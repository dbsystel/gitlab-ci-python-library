# Gitlab CI Python Library

A Python Library for creating dynamic pipelines for Gitlab CI in Python.

Furthermore the Gitlab Ci Python Library is called _gcip_.

[[_TOC_]]

# Code documentation

This page holds the user documentation of gcip.

For the code documentation please proceed to the [README.md within the gcip folder](./gcip/README.md)

# Configuring your project to use gcip

Create a `.gitlab-ci.yaml` with following static content:

```
---
generate-pipeline:
  stage: build
  image: python:3
  script:
    - pip3 install -r requirements.txt
    - python3 .gitlab-ci.py > generated-config.yml
  artifacts:
    paths:
      - generated-config.yml

run-pipeline:
  stage: deploy
  needs:
    - generate-pipeline
  trigger:
    include:
      - artifact: generated-config.yml
        job: generate-pipeline
    strategy: depend
```

Your gcip pipeline code then goes into a file named `.gitlab-ci.py`.

# Hints regarding the following examples

All the code examples in the following chapters are made for also be run with Pytest.
Thus to use the code for your real life Gitlab CI pipeline you have to change the following:

* Omit the import `from tests import conftest`.
* Put your pipeline code plain into the Python script and not within the `def test():` method.
* Instead of routing the pipeline output to the test method (`conftest.check(pipeline.render())`)
  print the resulting pipeline to STDOUT with `pipeline.print_yaml()`.

# Create a pipeline with one job


**Input:**

```py
# ./tests/unit/test_readme_pipe_with_one_job.py

import gcip
from tests import conftest


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(gcip.Job(namespace="print_date", script="date"))

    conftest.check(pipeline.render())

```

Remember: As stated in the [hints regarding the examples](#hints-regarding-the-following-examples),
your real pipeline code must end with `pipeline.print_yaml()` instead of `conftest.check(pipeline.render())`!

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_pipe_with_one_job_test.yml

stages:
- print_date
print-date:
  stage: print_date
  script:
  - date

```

# Configure jobs

Jobs can be configured by calling following methods:

**Input:**

```py
# ./tests/unit/test_readme_configure_jobs.py

import gcip
from tests import conftest


def test():
    pipeline = gcip.Pipeline()

    job = gcip.Job(namespace="print_date", script="date")
    job.set_image("docker/image:example")
    job.prepend_scripts("./before-script.sh")
    job.append_scripts("./after-script.sh")
    job.add_variables(USER="Max Power", URL="https://example.com")
    job.add_tags("test", "europe")
    job.add_artifacts_paths("binaries/", ".config")
    job.append_rules(gcip.Rule(if_statement="$MY_VARIABLE_IS_PRESENT"))

    pipeline.add_jobs(job)

    conftest.check(pipeline.render())

```

The `prepend_scripts`, `append_scripts` and all `add_*` methods allow an arbitrary number of positional arguments.
That means you can prepend/append/add a single script/variable/tag/... or a list of them.

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_configure_jobs_test.yml

stages:
- print_date
print-date:
  image: docker/image:example
  stage: print_date
  script:
  - ./before-script.sh
  - date
  - ./after-script.sh
  variables:
    USER: Max Power
    URL: https://example.com
  rules:
  - if: $MY_VARIABLE_IS_PRESENT
    when: on_success
    allow_failure: false
  artifacts:
    paths:
    - binaries/
    - .config
  tags:
  - test
  - europe

```

# Bundling jobs as sequence

You can bundle jobs to a sequence to apply a common configuration for all jobs included.
A job sequence has the same configuration methods as shown in the previous example for jobs.

**Input:**

```py
# ./tests/unit/test_readme_bundling_jobs.py

import gcip
from tests import conftest


def test():
    job_sequence = gcip.JobSequence()

    job1 = gcip.Job(namespace="job1", script="script1.sh")
    job1.prepend_scripts("from-job-1.sh")

    job_sequence.add_jobs(
        job1,
        gcip.Job(namespace="job2", script="script2.sh"),
    )

    job_sequence.prepend_scripts("from-sequence.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_jobs(job_sequence)

    conftest.check(pipeline.render())

```

As you will see in the output, jobs can have their own configuration (`job1.prepend_scripts(...`)
as well as a common configuration from their sequence (`job_sequence.prepend_scripts(...`).

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_bundling_jobs_test.yml

stages:
- job1
- job2
job1:
  stage: job1
  script:
  - from-sequence.sh
  - from-job-1.sh
  - script1.sh
job2:
  stage: job2
  script:
  - from-sequence.sh
  - script2.sh

```

# Stacking sequences

**Input:**

```py
# ./tests/unit/test_readme_stacking_sequences.py

import gcip
from tests import conftest


def test():
    sequence_a = gcip.JobSequence()
    sequence_a.add_jobs(gcip.Job(namespace="job1", script="script1.sh"))
    sequence_a.prepend_scripts("from-sequence-a.sh")

    sequence_b = gcip.JobSequence()
    sequence_b.add_sequences(sequence_a)
    sequence_b.add_jobs(gcip.Job(namespace="job2", script="script2.sh"))
    sequence_b.prepend_scripts("from-sequence-b.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_jobs(sequence_b)

    conftest.check(pipeline.render())

```

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_stacking_sequences_test.yml

stages:
- job1
- job2
job1:
  stage: job1
  script:
  - from-sequence-b.sh
  - from-sequence-a.sh
  - script1.sh
job2:
  stage: job2
  script:
  - from-sequence-b.sh
  - script2.sh

```

# Pipelines are sequences

Pipelines are a extended version of sequences and have all their abilities
(plus piplipe specific abilities), like their configuration options and
stacking other sequences.

**Input:**

```py
# ./tests/unit/test_readme_pipelines_are_sequences.py

import gcip
from tests import conftest


def test():
    sequence_a = gcip.JobSequence()
    sequence_a.add_jobs(gcip.Job(namespace="job1", script="script1.sh"))
    sequence_a.prepend_scripts("from-sequence.sh")

    pipeline = gcip.Pipeline()
    pipeline.add_sequences(sequence_a)
    pipeline.add_jobs(gcip.Job(namespace="job2", script="script2.sh"))
    pipeline.prepend_scripts("from-pipeline.sh")

    conftest.check(pipeline.render())

```

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_pipelines_are_sequences_test.yml

stages:
- job1
- job2
job1:
  stage: job1
  script:
  - from-pipeline.sh
  - from-sequence.sh
  - script1.sh
job2:
  stage: job2
  script:
  - from-pipeline.sh
  - script2.sh

```

# Namespaces allow reuse of jobs and sequences

Assume you want to reuse a parameterized job. Following [Input](./tests/unit/test_readme_missing_namespace.py) is an **incorrect** example:

```py
# ./tests/unit/test_readme_missing_namespace.py

import gcip
from tests import conftest


def job_for(environment: str) -> gcip.Job:
    return gcip.Job(namespace="do_something", script=f"./do-something-on.sh {environment}")


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_jobs(job_for(env))

    conftest.check(pipeline.render())

```

The output is obviously **wrong** as we expect two jobs but just get one:

```yaml
# ./tests/unit/comparison_files/test_readme_missing_namespace_test.yml

stages:
- do_something
do-something:
  stage: do_something
  script:
  - ./do-something-on.sh test

```

This is because both jobs were added with an identical name to the pipeline. The second job will
overwrite the first one.

When adding jobs or sequences to a sequence with

* `.add_jobs(...)`
* `.add_sequences(...)`

both methods accept the `namespace` parameter, you should use to modify the name of the jobs added.
The value of `namespaces` will be appended to the jobs `name` and `stage`. This only applies to
the jobs (sequences) added but not to the jobs (and sequences) already contained in the sequence.

## Reuse jobs

**Input:**

```py
# ./tests/unit/test_readme_namespace_job.py

import gcip
from tests import conftest


def job_for(environment: str) -> gcip.Job:
    return gcip.Job(namespace="do_something", script=f"./do-something-on.sh {environment}")


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_jobs(job_for(env), namespace=env)

    conftest.check(pipeline.render())

```

Mention that we added both jobs with a different `namespace` to the sequence.
Thus in the output we correctly populate the one job per environment:

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_namespace_job_test.yml

stages:
- do_something_development
- do_something_test
do-something-development:
  stage: do_something_development
  script:
  - ./do-something-on.sh development
do-something-test:
  stage: do_something_test
  script:
  - ./do-something-on.sh test

```

# Reuse sequences

Namespacing is much more useful for reusing sequences. You can define a whole
Gitlab CI pipeline within a sequence and reuse that sequence per environment.
You simply repeat that sequence in a loop for all environments. Namespacing
allows that all jobs of the sequence are populated per environment.

**Input:**

```py
# ./tests/unit/test_readme_namespace_sequence.py

import gcip
from tests import conftest


def environment_pipeline(environment: str) -> gcip.JobSequence:
    sequence = gcip.JobSequence()
    sequence.add_jobs(
        gcip.Job(namespace="job1", script=f"job-1-on-{environment}"),
        gcip.Job(namespace="job2", script=f"job-2-on-{environment}"),
    )
    return sequence


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_sequences(environment_pipeline(env), namespace=env)

    conftest.check(pipeline.render())

```

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_namespace_sequence_test.yml

stages:
- job1_development
- job2_development
- job1_test
- job2_test
job1-development:
  stage: job1_development
  script:
  - job-1-on-development
job2-development:
  stage: job2_development
  script:
  - job-2-on-development
job1-test:
  stage: job1_test
  script:
  - job-1-on-test
job2-test:
  stage: job2_test
  script:
  - job-2-on-test

```

# Parallelization - name, namespace (and stage)

As you may have mentioned from the previous examples, all jobs have a distinct stage and thus run in sequence.
This is because `namespace` will always extend the jobs `name` and `stage`. This applies to all `namespace`
parametes, either of the constructor of a Job object or to the `.add_*()` methods of a sequence.

So when adding jobs to a sequence (either directly or contained in a sequence itself) the goal is to just
extend the `name` of the jobs but not their `stage`, such that jobs with equal stages run in parallel.

This is possible by setting equal values for the `namespace` paramter but providing different values for the
`name` parameter when creating jobs or adding them to sequences. The value of the `name` parameter will extend
only the `name` of a job but not its `stage`.

## `name` parameter when creating jobs

**Input:**

```py
# ./tests/unit/test_readme_parallel_jobs.py

import gcip
from tests import conftest


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(
        gcip.Job(name="job1", namespace="single-stage", script="date"),
        gcip.Job(name="job2", namespace="single-stage", script="date"),
    )

    conftest.check(pipeline.render())

```

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_parallel_jobs_test.yml

stages:
- single_stage
single-stage-job1:
  stage: single_stage
  script:
  - date
single-stage-job2:
  stage: single_stage
  script:
  - date

```

This time we have chosen an equal value for `namespace`, such that the `stage`s of both jobs will be set equally. To avoid that also the
`name` values of both jobs are equal (and the second job overwrites the first one), we also have provided the `name` parameter, whose
value will be appended to the `name` of the jobs. Both jobs will run in parallel within the same stage.

First you might wonder, why there is nothing like a `stage` parameter. When thinking of sequences, the `namespace` parameter will extend
both, the `name` and `stage` of a job, and the `name` parameter will just extend the `name` of a job. Extends means their values will
be appended to the current values of `name` or `stage` of a job. However there is no need to extend just the `stage` of a job, such that
two jobs have distinct stages but unique names. Unique names means, that the latter job will overwrite all other jobs with the same name,
as a Job in Gitlab CI must have a unique name. It is only usefull to extend both values, such that two jobs are different and run in different
stages, or only to extend the `name` of jubs, such that two jobs are different but run in the same stage in parallel. To have the consistent
concpet of only the `name` and `namespace` parameter, this applies also to jobs.

Second you might wonder, why we haven't omit the `namespace` parameter when creating the jobs. This would be possible. But because of the
explanation in the previous paragraph, when creating jobs we can't set the `stage` value. Omitting the `namespace` parameter means we will
not set any value for `stage`. By default Gitlab CI jobs without a `stage` value will be in the `test` stage. To define a stage other than
`test`, we used the `namespace` parameter. Yes - that means that also the jobs `name` will include the value of the `namespace`. But this
design decision will make the concept of `name` and `namespace` much more clear that also providing a `stage` parameter for jobs while
sequences haven't such a (useless) `stage` parameter (because it makes no sense to extend the `stage` over the `name` of a job).

Sorry - that was a lot of theory - but simply keep in mind when creating Jobs:

* Set different values for just the `namespace` parameter when creating distinct jobs which will run in sequence (separate stages).
* Set different values for just the `name` parameter when creating distinct jobs which will run in parallel (equal stage).
* Set different values for the `name` parameters but equal values for the `namespace` parameters when creating distinct jobs which will run in parallel (equal stage) but defining the name of the stage.
* Setting different values for both parameters is nonsense and will lead to the first result of distinct jobs which will run in sequence.

## `name` parameter when adding jobs (and sequences) to sequences

Lets take the sequence example from the chapter [Namespaces allow reuse of jobs and sequence](#namespaces-allow-reuse-of-jobs-and-sequence)
and instead of using the `namespace` when adding the sequence several times to the pipeline we now use the `name` parameter.

**Input:**

```py
# ./tests/unit/test_readme_parallel_sequence.py

import gcip
from tests import conftest


def environment_pipeline(environment: str) -> gcip.JobSequence:
    sequence = gcip.JobSequence()
    sequence.add_jobs(
        gcip.Job(namespace="job1", script=f"job-1-on-{environment}"),
        gcip.Job(namespace="job2", script=f"job-2-on-{environment}"),
    )
    return sequence


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_sequences(environment_pipeline(env), name=env)

    conftest.check(pipeline.render())

```

Now the environments run in parallel, because just the job names are populated per environment but
not the stage names.

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_parallel_sequence_test.yml

stages:
- job1
- job2
job1-development:
  stage: job1
  script:
  - job-1-on-development
job2-development:
  stage: job2
  script:
  - job-2-on-development
job1-test:
  stage: job1
  script:
  - job-1-on-test
job2-test:
  stage: job2
  script:
  - job-2-on-test

```

You can also mix the usage of `namespace` and `name`. This makes sense when adding lots of jobs
where groups of jobs should run sequentially but jobs within a group in parallel.
Here an Example:

**Input:**

```py
# ./tests/unit/test_readme_mix_namespace_and_name.py

import gcip
from tests import conftest


def job_for(service: str) -> gcip.Job:
    return gcip.Job(namespace="update_service", script=f"./update-service.sh {service}")


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        for service in ["service1", "service2"]:
            pipeline.add_jobs(job_for(f"{service}_{env}"), namespace=env, name=service)

    conftest.check(pipeline.render())

```

As output we get two services updated in parallel but in consecutive stages.

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_mix_namespace_and_name_test.yml

stages:
- update_service_development
- update_service_test
update-service-development-service1:
  stage: update_service_development
  script:
  - ./update-service.sh service1_development
update-service-development-service2:
  stage: update_service_development
  script:
  - ./update-service.sh service2_development
update-service-test-service1:
  stage: update_service_test
  script:
  - ./update-service.sh service1_test
update-service-test-service2:
  stage: update_service_test
  script:
  - ./update-service.sh service2_test

```

# Batteries included

Until here you have learned everything about the logical functionality of gcip. But gcip does
also contain a library of predefined assets you can use for building your pipelines. Those
assets are contained in the following modules named by their type:

* [scripts](./gcip/scripts.py)
* [jobs](./gcip/jobs.py)
* [job_sequences](./gcip/job_sequences.py)
* [rules](./gcip/rules.py)

Following sub chapters provide an example for one asset out of every module.

## scripts

**Input:**

```py
# ./tests/unit/test_readme_assets_scripts.py

import gcip
from gcip import scripts
from tests import conftest


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(gcip.Job(namespace="print_date", script=scripts.clone_repository("path/to/group")))

    conftest.check(pipeline.render())

```

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_assets_scripts_test.yml

stages:
- print_date
print-date:
  stage: print_date
  script:
  - git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/path/to/group.git

```

## jobs

**Input:**

```py
# ./tests/unit/test_readme_assets_jobs.py

import gcip
from tests import conftest
from gcip.jobs import python


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(python.flake8())

    conftest.check(pipeline.render())

```

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_assets_jobs_test.yml

stages:
- lint
lint-flake8:
  stage: lint
  script:
  - pip3 install --upgrade flake8
  - flake8

```

## job_sequences

**Input:**

```py
# ./tests/unit/test_readme_assets_job_sequences.py

import gcip
from tests import conftest
from gcip.job_sequences import cdk


def test():
    pipeline = gcip.Pipeline()
    pipeline.add_jobs(cdk.diff_deploy("my-cdk-stack", toolkit_stack_name="cdk-toolkit"))

    conftest.check(pipeline.render())

```

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_assets_job_sequences_test.yml

stages:
- diff
- deploy
diff-cdk:
  stage: diff
  script:
  - cdk synth my-cdk-stack
  - cdk diff my-cdk-stack
deploy-cdk:
  needs:
  - job: diff-cdk
    artifacts: true
  stage: deploy
  script:
  - pip3 install gcip
  - python3 -m gcip.script_library.wait_for_cloudformation_stack_ready --stack-names
    'my-cdk-stack'
  - cdk deploy --strict --require-approval 'never' --toolkit-stack-name cdk-toolkit
    my-cdk-stack

```

## rules

**Input:**

```py
# ./tests/unit/test_readme_assets_rules.py

import gcip
from gcip import rules
from tests import conftest


def test():
    job = gcip.Job(namespace="print_date", script="date")
    job.append_rules(
        rules.on_merge_request_events().never(),
        rules.on_master(),
    )

    pipeline = gcip.Pipeline()
    pipeline.add_jobs(job)

    conftest.check(pipeline.render())

```

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_assets_rules_test.yml

stages:
- print_date
print-date:
  stage: print_date
  script:
  - date
  rules:
  - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    when: never
    allow_failure: false
  - if: $CI_COMMIT_BRANCH == "master"
    when: on_success
    allow_failure: false

```

# Do more with Python

NOTE: **Please note regarding the current version of gcip**
Currently not all functinality of Gitlab CI is provided by gcip. In the following section is described that you don't need all
the functionality from Gitlab CI, as you can cover some of this in Python. But some functionality must be part of gcip, like
configure caching or artifacts, which isn't implemented yet.

Until here you have learned everything about the functionality of _gcip_. That is, to sum it up:

* Creating jobs.
* Organizing job hierarchies with sequences.
* Configuring jobs directly or at hierarchy level over sequences.
* Namespacing and parallelization.
* Predefined assets.

With the few functionalities of gcip and the capabilities of Python, there is nothing left to create
every pipeline you can imagine. Gitlab CI provides much more constructs you may miss here, but most of
them are clunky workarounds as cause of the limited logic capabilities of the Domain Specific Script "Language"
of Gitlab CI. You don't need them, when you can design your pipelines in Python. Here a few examples:

* You don't need templates (the `extends` keyword or YAML anchors), because you can reuse jobs and sequences.
* You don't need `before_script`, `after_script` or global configurations, because you can do configurations
  at an arbitrary level in the sequences hierarchy. All configurations will finally be populated down to the jobs.
* You didn't have to keep struggling with rules at pipeline and job level. In gcipd you can configure rules at
  an arbitrary level in the sequences hierarchy.

Furthermore you can leverage all the power of a programming language, to dynamically design your pipelies. Here
some ideas:

* Bundle jobs in sequences and use loops to populate the sequences over a list of environments.
* Use if-then-else expressions to create jobs within job sequences depending on environment information or requirements.
* Access information from outside your pipeline script you use for decision making inside your pipeline script.

# Beyond the basics

This chapter covers further abilities of GCIP which suffices to be read after the basics.

## string Job / JobSequence modifications together

Every modification method of Job and JobSequence returns the appropriate Job / JobSequence object. Thus you can
string multiple modifications methods together. Here an example for the job configuration.

**Input:**

```py
# ./tests/unit/test_readme_string_together_job_configurations.py

from gcip import Job, Rule, Pipeline
from tests import conftest


def test():
    pipeline = Pipeline()

    # yapf: disable
    pipeline.add_jobs(
        Job(namespace="print_date", script="date")
        .set_image("docker/image:example")
        .prepend_scripts("./before-script.sh")
        .append_scripts("./after-script.sh")
        .add_variables(USER="Max Power", URL="https://example.com")
        .add_tags("test", "europe")
        .add_artifacts_paths("binaries/", ".config")
        .append_rules(Rule(if_statement="$MY_VARIABLE_IS_PRESENT"))
    )
    # yapf: enable

    conftest.check(pipeline.render())

```

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_string_together_job_configurations_test.py
```

The same works with sequences.

## TriggerJobs

Besides normal Jobs with GCIP you can define TriggerJobs which either run another projects pipeline or a child-pipeline.

Here an example for triggering another pipeline:

**Input:**

```py
# ./tests/unit/test_readme_trigger_project_pipeline.py

from gcip import Pipeline, TriggerJob, TriggerStrategy
from tests import conftest


def test():
    pipeline = Pipeline()
    pipeline.add_jobs(TriggerJob(
        namespace="trigger-banana",
        project="myteam/banana",
        branch="test",
        strategy=TriggerStrategy.DEPEND,
    ))

    conftest.check(pipeline.render())

```

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_trigger_project_pipeline_test.yml

stages:
- trigger_banana
trigger-banana:
  trigger:
    project: myteam/banana
    branch: test
    strategy: depend
  stage: trigger_banana

```

Here an example for triggering a child pipeline:

**Input:**

```py
# ./tests/unit/test_readme_trigger_child_pipeline.py

from gcip import (
    Pipeline,
    TriggerJob,
    IncludeLocal,
    TriggerStrategy,
)
from tests import conftest


def test():
    pipeline = Pipeline()
    pipeline.add_jobs(
        TriggerJob(
            namespace="trigger-subpipe",
            includes=IncludeLocal("./my-subpipe.yml"),
            strategy=TriggerStrategy.DEPEND,
        )
    )

    conftest.check(pipeline.render())

```

**Output:**

```yaml
# ./tests/unit/comparison_files/test_readme_trigger_child_pipeline_test.yml

stages:
- trigger_subpipe
trigger-subpipe:
  trigger:
    include:
    - local: ./my-subpipe.yml
    strategy: depend
  stage: trigger_subpipe

```

# Authors

GCIP was created by [Thomas Steinbach](mailto:thomas.t.steinbach@deutschebahn.com) in 2020.

Thanks to initial contributions from [Daniel von Eßen](mailto:daniel.von-essen@deutschebahn.com)

# Licence

The content of this repository is licensed under the [Apache 2.0 license](http://www.apache.org/licenses/LICENSE-2.0).

Copyright DB Systel GmbH
