FROM python:3.9-alpine

RUN apk add --update-cache \
    gcc musl-dev \
  && rm -rf /var/cache/apk/*

WORKDIR /usr/src/app

COPY docker docker
COPY gcip gcip
COPY LICENCE .
COPY requirements.txt .
COPY README.md .
COPY setup.py .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /workdir

CMD /usr/src/app/docker/gcip.sh
