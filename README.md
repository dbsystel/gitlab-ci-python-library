# Gitlab CI Python Library

A Python Library for creating dynamic pipelines for Gitlab CI in Python.

Furthermore the Gitlab Ci Python Library is called _gcip_.

## Configuring you project to use gcip

Create a `.gitlab-ci.yaml` with following static content:

```
---
include:
 - project: gitlab-ci-python-library
   file: gcip-pipeline.yml
```

Your gcip pipeline code then goes into a file named `.gitlab-ci.py`.

## Hints regarding the following examples

* Both, input code and output, is shortened to show the essence of the examples.
* Once an import was shown in a code example it is left out in subsequent examples.
* The command `pypeline.print_yaml()` is requred at the end of every pipeline script for
  synthesizing the Giltab CI pipeline code, but only shown in the first example.
* The real output of a code snippet may containe more defaults not shown here in the documentation.
* Before every code example there is a link to a working code snipped as pytest.

## Create a pipeline with one job

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

## Configure jobs

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

## Bundling jobs as sequence

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
