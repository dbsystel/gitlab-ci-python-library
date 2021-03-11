#!/bin/sh

PIPELINE_PY="${*:-.gitlab-ci.py}"
python3 "$PIPELINE_PY"
