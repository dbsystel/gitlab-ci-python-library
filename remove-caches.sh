#!/bin/bash

find . -type d -name '__pycache__' -exec rm -rf {} +
rm -rf dist
rm -rf build
rm -rf .pytest_cache
rm -rf .mypy_cache
rm -rf gcip.egg-info

# from gitlabci-local
rm -rf generated-config.yml
rm -rf dive.txt image/ trivi.txt