ARG DOCKER_PYTHON_VERSION
FROM python:${DOCKER_PYTHON_VERSION}-slim-buster AS base

VOLUME /octane
VOLUME /octane/users

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl libxslt-dev libxcb-xinput0 libjpeg62-turbo-dev zlib1g-dev libblas-dev liblapack-dev libatlas-base-dev libopenjp2-7 libtiff-dev build-essential git gcc libffi-dev rsync libssl-dev libxml2-dev libxslt1-dev libxslt-dev libjpeg62-turbo-dev zlib1g-dev \
    && python -m venv /opt/venv

# skip cryptography rust compilation (required for armv7 builds)
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1


# Octane management port
EXPOSE 5000

# Octane VSCode port
EXPOSE 6000

# To make sure we can create enough instances of Octane
EXPOSE 5001-5500

WORKDIR /octane-entrypoint
COPY ./source/Octane-Installer/installer_utils/docker-entrypoint.sh /octane-entrypoint/docker-entrypoint.sh

WORKDIR /octane

HEALTHCHECK --interval=1m --timeout=30s --retries=50 CMD curl --fail http://localhost:5000/ping || exit 1
ENTRYPOINT ["sh","/octane-entrypoint/docker-entrypoint.sh"]
