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

## Create a Pipeline with one job

[Input](./tests/unit/readme-pipe-with-one-job.py):

```
import gcip

pipeline = gcip.Pipeline()
pipeline.add_job(
    gcip.Job(name="print_date", script="date")
    )
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

## Configure Jobs

[Input](./tests/unit/readme-configure-jobs.py):

Output:

```
stages:
- print_date
print_date:
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
