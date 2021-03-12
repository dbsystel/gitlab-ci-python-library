#!/bin/sh

set -x

PIPELINE_PY="${*:-.gitlab-ci.py}"

if test -f requirements.txt; then
  grep -v '^ *#\|^gcip' requirements.txt > /tmp/gcip_requirements.tmp
  cat /tmp/gcip_requirements.tmp
  pip3 install -r /tmp/gcip_requirements.tmp
  rm -rf /tmp/gcip_requirements.tmp
fi

python3 "$PIPELINE_PY"
