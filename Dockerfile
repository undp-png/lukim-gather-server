# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM ubuntu:20.04 as base

# Non interactive frontend
ENV DEBIAN_FRONTEND=noninteractive

# Install requiremnts for python3.9
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    software-properties-common \
    git

# Add deadsnakes ppa
RUN add-apt-repository ppa:deadsnakes/ppa -y

# Install python3.9
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    python3.9 \
    python3.9-dev \
    python3.9-venv

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
RUN update-alternatives --set python /usr/bin/python3.9

FROM base as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Add poetry home to path
ENV PATH="$POETRY_HOME/bin:$PATH"

# OS dependencies for installing poetry and project dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libsqlite3-mod-spatialite \
    gettext

# Install pip
RUN curl -sSL https://bootstrap.pypa.io/get-pip.py | python

# Install virtualenv
RUN pip3.9 install -U virtualenv

# Add gis ppa
RUN add-apt-repository ppa:ubuntugis/ppa -y

# Install gdal
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    gdal-bin

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python

# Testing stage
FROM python-base as testing

WORKDIR /code

ENTRYPOINT ["/code/docker/entrypoint.test.sh"]

# Development stage
FROM python-base as development

WORKDIR /code

ENTRYPOINT ["/code/docker/entrypoint.dev.sh"]

# Production stage
FROM python-base as production

WORKDIR /code

COPY . /code/

# Install all dependencies
RUN poetry install --no-dev --extras asgi

ENTRYPOINT [ "/code/docker/entrypoint.prod.sh"]
