#!/bin/bash
asciidoctor docs/index.adoc -o docs/index.html
asciidoctor docs/user/index.adoc -o docs/user/index.html
pdoc3 --html -f --skip-errors --output-dir docs/api gcip
