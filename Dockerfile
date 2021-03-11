FROM python:3.9-slim

WORKDIR /usr/src/app

COPY docker docker
COPY gcip gcip
COPY LICENCE .
COPY requirements.txt .
COPY README.adoc .
COPY setup.py .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /workdir

ENTRYPOINT /usr/src/app/docker/entrypoint.sh
