FROM python:3.11-slim-buster AS base

VOLUME /octobot/backtesting
VOLUME /octobot/logs
VOLUME /octobot/tentacles
VOLUME /octobot/reference_tentacles
VOLUME /octobot/reference_profiles
VOLUME /octobot/user

# requires git to install requirements with git+https
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git gcc libffi-dev rsync libssl-dev libxml2-dev libxslt1-dev libxslt-dev libjpeg62-turbo-dev zlib1g-dev \
    && python -m venv /opt/venv

# skip cryptography rust compilation (required for armv7 builds)
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1


# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY . /octobot-packages
WORKDIR /octobot-packages
RUN cp .env /octobot/.env

RUN pip install -U setuptools wheel pip>=20.0.0
RUN pip install --prefer-binary -r requirements.txt
RUN pip install --prefer-binary -r strategy_maker_requirements.txt
RUN pip install --prefer-binary -r octobot-packages/Async-Channel/requirements.txt
RUN pip install --prefer-binary -r octobot-packages/OctoBot-Backtesting/requirements.txt
RUN pip install --prefer-binary -r octobot-packages/OctoBot-Commons/requirements.txt
RUN pip install --prefer-binary -r octobot-packages/OctoBot-evaluators/requirements.txt
RUN pip install --prefer-binary -r octobot-packages/OctoBot-Services/requirements.txt
RUN pip install --prefer-binary -r octobot-packages/OctoBot-Tentacles-Manager/requirements.txt
RUN pip install --prefer-binary -r octobot-packages/OctoBot-Trading/requirements.txt
RUN pip install --prefer-binary -r octobot-packages/trading-backend/requirements.txt

WORKDIR /octobot-packages/octobot-packages/Async-Channel
RUN pip install ./
WORKDIR /octobot-packages/octobot-packages/trading-backend
RUN pip install ./
WORKDIR /octobot-packages/octobot-packages/OctoBot-Commons
RUN pip install ./
WORKDIR /octobot-packages/octobot-packages/OctoBot-Tentacles-Manager
RUN pip install ./
WORKDIR /octobot-packages/octobot-packages/OctoBot-Backtesting
RUN pip install ./
WORKDIR /octobot-packages/octobot-packages/OctoBot-Trading
RUN pip install ./
WORKDIR /octobot-packages/octobot-packages/OctoBot-Services
RUN pip install ./
WORKDIR /octobot-packages/octobot-packages/OctoBot-evaluators
RUN pip install ./

WORKDIR /octobot-packages
RUN python setup.py install

# FROM python:3.11-slim-buster

ARG TENTACLES_URL_TAG=""
ENV TENTACLES_URL_TAG=$TENTACLES_URL_TAG
ENV SHARE_YOUR_OCOBOT=

WORKDIR /octobot
# Import python dependencies

# COPY --from=base /opt/venv /opt/venv
# # Import built dependencies
# COPY --from=base /opt/efs/build /opt/efs/build

COPY octobot/config /octobot/octobot/config
COPY docker-entrypoint.sh docker-entrypoint.sh

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl libxslt-dev libxcb-xinput0 libjpeg62-turbo-dev zlib1g-dev libblas-dev liblapack-dev libatlas-base-dev libopenjp2-7 libtiff-dev \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /opt/venv/bin/OctoBot OctoBot # Make sure we use the virtualenv
RUN chmod +x docker-entrypoint.sh
RUN chmod +x OctoBot

EXPOSE 5001

HEALTHCHECK --interval=1m --timeout=30s --retries=3 CMD curl --fail http://localhost:5001 || exit 1
ENTRYPOINT ["sh","./docker-entrypoint.sh"]
