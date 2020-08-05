# Gitlab CI Python Library

A Python Library for creating dynamic pipelines for Gitlab CI in Python.

Furthermore the Gitlab Ci Python Library is called _gcip_.

[[_TOC_]]

# Configuring your project to use gcip

Create a `.gitlab-ci.yaml` with following static content:

```
---
variables:
  GCIP_VERSION: "<gcip release>"

include:
  - project: gitlab-ci-python-library
    file: gcip-pipeline.yml
```

Your gcip pipeline code then goes into a file named `.gitlab-ci.py`.

# Hints regarding the following examples

* Both, input code and output, is shortened to show the essence of the examples.
* Once an import was shown in a code example it is left out in subsequent examples.
* The command `pypeline.print_yaml()` is requred at the end of every pipeline script for
  synthesizing the Giltab CI pipeline code, but only shown in the first example.
* The real output of a code snippet may containe more defaults not shown here in the documentation.
* Before every code example there is a link to a working code snipped as pytest. It could be executed
  with `pytest -s tests/unit/test_readme_<code-snippet>.py`

# Create a pipeline with one job

[Input](./tests/unit/test_readme_pipe_with_one_job.py):

```
import gcip

pipeline = gcip.Pipeline()
pipeline.add_job(gcip.Job(name="print_date", script="date"))
pipeline.print_yaml()
```

Output:

```
stages:
- print_date
print_date:
  script:
  - date
  stage: print_date
```

# Configure jobs

Jobs can be configured by calling following methods:

[Input](./tests/unit/test_readme_configure_jobs.py):

```
pipeline = gcip.Pipeline()

job = gcip.Job(name="print_date", script="date")
job.set_image("docker/image:example")
job.prepend_script("./before-script.sh")
job.append_script("./after-script.sh")
job.add_variables(USER="Max Power", URL="https://example.com")
job.add_tags("test", "europe")
job.add_rules(gcip.Rule(if_statement="$MY_VARIABLE_IS_PRESENT"))

pipeline.add_job(job)
```

The `prepend_script`, `append_script` and all `add_*` methods allow an arbitrary number of positional arguments.

Output:

```
stages:
- print_date
print_date:
  image: docker/image:example
  rules:
  - if: $MY_VARIABLE_IS_PRESENT
  script:
  - ./before-script.sh
  - date
  - ./after-script.sh
  variables:
    USER: Max Power
    URL: https://example.com
  tags:
  - europe
  - test
  stage: print_date
```

# Bundling jobs as sequence

You can bundle jobs to a sequence to apply a common configuration for all jobs included.
A job sequence has the same configuration methods as shown in the previous example for jobs.

[Input](./tests/unit/test_readme_bundling_jobs.py):

```
job_sequence = gcip.JobSequence()

job1 = gcip.Job(name="job1", script="script1.sh")
job1.prepend_script("from-job-1.sh")

job_sequence.add_job(job1)
job_sequence.add_job(gcip.Job(name="job2", script="script2.sh"))

job_sequence.prepend_script("from-sequence.sh")

pipeline = gcip.Pipeline()
pipeline.add_job(job_sequence)
```

As you will see in the output, jobs can have their own configuration (`job1.prepend_script(...`)
as well as a common configuration from their sequence (`job_sequence.prepend_script(...`).

Output:

```
stages:
- job1
- job2
job1:
  script:
  - from-sequence.sh
  - from-job-1.sh
  - script1.sh
  stage: job1
job2:
  script:
  - from-sequence.sh
  - script2.sh
  stage: job2
```

# Stacking sequences

[Input](./tests/unit/test_readme_stacking_sequences.py):

```
sequence_a = gcip.JobSequence()
sequence_a.add_job(gcip.Job(name="job1", script="script1.sh"))
sequence_a.prepend_script("from-sequence-a.sh")

sequence_b = gcip.JobSequence()
sequence_b.add_sequence(sequence_a)
sequence_b.add_job(gcip.Job(name="job2", script="script2.sh"))
sequence_b.prepend_script("from-sequence-b.sh")

pipeline = gcip.Pipeline()
pipeline.add_job(sequence_b)
```

Output:

```
stages:
- job1
- job2
job1:
  script:
  - from-sequence-b.sh
  - from-sequence-a.sh
  - script1.sh
  stage: job1
job3:
  script:
  - from-sequence-b.sh
  - script2.sh
  stage: job2
```

# Pipelines are sequences

Pipelines are a extended version of sequences and have all their abilities
(plus piplipe specific abilities), like their configuration options and
stacking other sequences.

[Input](./tests/unit/test_readme_pipelines_are_sequences.py):

```
sequence_a = gcip.JobSequence()
sequence_a.add_job(gcip.Job(name="job1", script="script1.sh"))
sequence_a.prepend_script("from-sequence.sh")

pipeline = gcip.Pipeline()
pipeline.add_sequence(sequence_a)
pipeline.add_job(gcip.Job(name="job2", script="script2.sh"))
pipeline.prepend_script("from-pipeline.sh")
```

Output:

```
stages:
- job1
- job2
job1:
  script:
  - from-pipeline.sh
  - from-sequence.sh
  - script1.sh
  stage: job1
job2:
  script:
  - from-pipeline.sh
  - script2.sh
  stage: job2
```

# Namespaces allow reuse of jobs and sequences

Assume you want to reuse a parameterized job. Following [Input](./tests/unit/test_readme_missing_namespace.py) is an **incorrect** example:

```
def job_for(environment: str) -> gcip.Job:
    return gcip.Job(name="do_something", script=f"./do-something-on.sh {environment}")

pipeline = gcip.Pipeline()
for env in ["development", "test"]:
    pipeline.add_job(job_for(env))
```

The output is obviously **wrong** as we expect two jobs but just get one:

```
stages:
- do_something
do_something:
  script:
  - ./do-something-on.sh test
  variables: {}
  tags: []
  stage: do_something
```

Instead the `.add_job(...)` and `.add_sequence(...)` methods of sequences accept a `namespace` parameter,
whose value will be appended to the Gitlab CI job name and stage.

[Input](./tests/unit/test_readme_namespace_job.py):

```
def job_for(environment: str) -> gcip.Job:
    return gcip.Job(name="do_something", script=f"./do-something-on.sh {environment}")

pipeline = gcip.Pipeline()
for env in ["development", "test"]:
    pipeline.add_job(job_for(env), namespace=env)
```

Thus in the output we correctly populate the one job per environment:

Output:

```
stages:
- do_something_development
- do_something_test
do_something_development:
  script:
  - ./do-something-on.sh development
  stage: do_something_development
do_something_test:
  script:
  - ./do-something-on.sh test
  stage: do_something_test
```

Namespacing is much more useful for reusing sequences. You can define a whole
Gitlab CI pipeline within a stage - but need that to do for just one environment.
Then you simply repeat that pipeline in a loop for all environments. Namespacing
allows that all jobs of the pipeline are populated per environment.

[Input](./tests/unit/test_readme_namespace_sequence.py):

```
def environment_pipeline(environment: str) -> gcip.JobSequence:
    sequence = gcip.JobSequence()
    sequence.add_job(gcip.Job(name="job1", script=f"job-1-on-{environment}"))
    sequence.add_job(gcip.Job(name="job2", script=f"job-2-on-{environment}"))
    return sequence

pipeline = gcip.Pipeline()
for env in ["development", "test"]:
    pipeline.add_sequence(environment_pipeline(env), namespace=env)
```

Output:

```
stages:
- job1_development
- job2_development
- job1_test
- job2_test
job1_development:
  script:
  - job-1-on-development
  stage: job1_development
job2_development:
  script:
  - job-2-on-development
  stage: job2_development
job1_test:
  script:
  - job-1-on-test
  stage: job1_test
job2_test:
  script:
  - job-2-on-test
  stage: job2_test
```

# Parallelization

As you may have mentioned from the previous examples, all jobs have a distinct stage and thus run in sequence.
This is because by default:

* A jobs stage has the same initial value as the jobs name.
* Both, the jobs name and stage, are extended by the namespace.

Because a jobs stage has the same value as the jobs name, to run jobs in parallel you have to set a different
value for the jobs stage on its initialization:

[Input](./tests/unit/test_readme_parallel_jobs.py)

```
pipeline = gcip.Pipeline()
pipeline.add_job(gcip.Job(name="job1", stage="single-stage", script="date"))
pipeline.add_job(gcip.Job(name="job2", stage="single-stage", script="date"))
```

Output:

```
stages:
- single-stage
job1:
  script:
  - date
  stage: single-stage
job2:
  script:
  - date
  stage: single-stage
```

Because job name and stage values are both extended by the namespace equally, to run sequences in parallel you have
just to extend the name values of the jobs but not the stage values. So instead of passing the `namespace` parameter
to the `.add_job(...)` and `.add_sequence(...)` method you cann pass the `name` parameter.

Lets take the sequence example from the chapter [Namespaces allow reuse of jobs and sequence](#namespaces-allow-reuse-of-jobs-and-sequence)
and instead of using the `namespace` when adding the sequence several times to the pipeline we now use the `name` parameter.

[Input](./tests/unit/test_readme_parallel_sequence.py)

```
def environment_pipeline(environment: str) -> gcip.JobSequence:
    sequence = gcip.JobSequence()
    sequence.add_job(gcip.Job(name="job1", script=f"job-1-on-{environment}"))
    sequence.add_job(gcip.Job(name="job2", script=f"job-2-on-{environment}"))
    return sequence

pipeline = gcip.Pipeline()
for env in ["development", "test"]:
    pipeline.add_sequence(environment_pipeline(env), name=env)
```

Now the environments run in parallel, because just the job names are populated per environment but
not the stage names.

Output:

```
stages:
- job1
- job2
job1_development:
  script:
  - job-1-on-development
  stage: job1
job2_development:
  script:
  - job-2-on-development
  stage: job2
job1_test:
  script:
  - job-1-on-test
  stage: job1
job2_test:
  script:
  - job-2-on-test
  stage: job2
```

You can also mix the usage of `namespace` and `name`. This makes sense when adding a job or sequence more
than two times. Here an example with adding jobs:

[Input](./tests/unit/test_readme_mix_namespace_and_name.py)

```
def job_for(service: str) -> gcip.Job:
    return gcip.Job(name="update_service", script=f"./update-service.sh {service}")

pipeline = gcip.Pipeline()
for env in ["development", "test"]:
    pipeline.add_job(job_for(env), namespace=env, name="service1")
    pipeline.add_job(job_for(env), namespace=env, name="service2")
```

As output we get two services updated in parallel but in consecutive stages.

Output:

```
stages:
- update_service_development
- update_service_test
update_service_development_service1:
  script:
  - ./update-service.sh development
  stage: update_service_development
update_service_development_service2:
  script:
  - ./update-service.sh development
  stage: update_service_development
update_service_test_service1:
  script:
  - ./update-service.sh test
  stage: update_service_test
update_service_test_service2:
  script:
  - ./update-service.sh test
  stage: update_service_test
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

[Input](./tests/unit/test_readme_assets_scripts.py)

```
from gcip import scripts

pipeline = gcip.Pipeline()
pipeline.add_job(gcip.Job(name="download_artifacts", script=scripts.clone_repository("path/to/group")))
```

Output:

```
stages:
- download_artifacts
print_date:
  script:
  - git clone --branch master --single-branch https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/path/to/group.git
  stage: download_artifacts
```

## jobs

[Input](./tests/unit/test_readme_assets_jobs.py)

```
from gcip import jobs

pipeline = gcip.Pipeline()
pipeline.add_job(jobs.cdk_diff("my-cdk-stack"))
```

Output:

```
stages:
- cdk_diff
cdk_diff:
  script:
  - cdk synth my-cdk-stack
  - cdk diff my-cdk-stack
  stage: cdk_diff
```

## job_sequences

[Input](./tests/unit/test_readme_assets_job_sequences.py)

```
from gcip import job_sequences

pipeline = gcip.Pipeline()
pipeline.add_job(job_sequences.cdk_diff_deploy(stack="my-cdk-stack", toolkit_stack_name="cdk-toolkit"))
```

Output:

```
stages:
- cdk_diff
- cdk_deploy
cdk_diff:
  script:
  - cdk synth my-cdk-stack
  - cdk diff my-cdk-stack
  stage: cdk_diff
cdk_deploy:
  script:
  - cdk deploy --strict --require-approval 'never' --toolkit-stack-name cdk-toolkit
    my-cdk-stack
  stage: cdk_deploy
```

## rules

[Input](/.tests/unit/test_readme_assets/rules.py)

```
from gcip import rules

job = gcip.Job(name="print_date", script="date")
job.add_rules(rules.not_on_merge_request_events())

pipeline = gcip.Pipeline()
pipeline.add_job(job)
```

Output:

```
stages:
- print_date
print_date:
  script:
  - date
  rules:
  - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    when: never
  stage: print_date
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
