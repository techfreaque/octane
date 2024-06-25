FROM python:3.11-slim-buster AS base

VOLUME /octobot/backtesting
VOLUME /octobot/logs
VOLUME /octobot/tentacles
VOLUME /octobot/user

# requires git to install requirements with git+https
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl libxslt-dev libxcb-xinput0 libjpeg62-turbo-dev zlib1g-dev libblas-dev liblapack-dev libatlas-base-dev libopenjp2-7 libtiff-dev build-essential git gcc libffi-dev rsync libssl-dev libxml2-dev libxslt1-dev libxslt-dev libjpeg62-turbo-dev zlib1g-dev \
    && python -m venv /opt/venv

# skip cryptography rust compilation (required for armv7 builds)
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1


# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# install dependencies before to use caching
WORKDIR /octobot-requirements
RUN pip install -U setuptools wheel pip>=20.0.0
COPY ./octobot-packages/OctoBot/requirements.txt ./OctoBot/requirements.txt
RUN pip install --prefer-binary -r OctoBot/requirements.txt
COPY ./octobot-packages/Async-Channel/requirements.txt ./Async-Channel/requirements.txt
RUN pip install --prefer-binary -r Async-Channel/requirements.txt
COPY ./octobot-packages/OctoBot-Backtesting/requirements.txt ./OctoBot-Backtesting/requirements.txt
RUN pip install --prefer-binary -r OctoBot-Backtesting/requirements.txt
COPY ./octobot-packages/OctoBot-Commons/requirements.txt ./OctoBot-Commons/requirements.txt
RUN pip install --prefer-binary -r OctoBot-Commons/requirements.txt
COPY ./octobot-packages/OctoBot-evaluators/requirements.txt ./OctoBot-evaluators/requirements.txt
RUN pip install --prefer-binary -r OctoBot-evaluators/requirements.txt
COPY ./octobot-packages/OctoBot-Services/requirements.txt ./OctoBot-Services/requirements.txt
RUN pip install --prefer-binary -r OctoBot-Services/requirements.txt
COPY ./octobot-packages/OctoBot-Tentacles-Manager/requirements.txt ./OctoBot-Tentacles-Manager/requirements.txt
RUN pip install --prefer-binary -r OctoBot-Tentacles-Manager/requirements.txt
COPY ./octobot-packages/OctoBot-Trading/requirements.txt ./OctoBot-Trading/requirements.txt
RUN pip install --prefer-binary -r OctoBot-Trading/requirements.txt
COPY ./octobot-packages/trading-backend/requirements.txt ./trading-backend/requirements.txt
RUN pip install --prefer-binary -r trading-backend/requirements.txt
COPY ./octobot-packages/OctoBot/strategy_maker_requirements.txt ./OctoBot/strategy_maker_requirements.txt
RUN pip install --prefer-binary -r OctoBot/strategy_maker_requirements.txt

WORKDIR /
COPY . .
WORKDIR /octobot-packages
RUN mkdir -p /octobot
RUN cp /.env /octobot/.env

WORKDIR /octobot-packages/Async-Channel
RUN pip install ./
WORKDIR /octobot-packages/trading-backend
RUN pip install ./
WORKDIR /octobot-packages/OctoBot-Commons
RUN pip install ./
WORKDIR /octobot-packages/OctoBot-Tentacles-Manager
RUN pip install ./
WORKDIR /octobot-packages/OctoBot-Backtesting
RUN pip install ./
WORKDIR /octobot-packages/OctoBot-Trading
RUN pip install ./
WORKDIR /octobot-packages/OctoBot-Services
RUN pip install ./
WORKDIR /octobot-packages/OctoBot-evaluators
RUN pip install ./

WORKDIR /octobot-packages/OctoBot
RUN python setup.py install

WORKDIR /
RUN pip install --prefer-binary -r /custom_requirements.txt

# FROM python:3.11-slim-buster

ARG TENTACLES_URL_TAG=""
ENV TENTACLES_URL_TAG=$TENTACLES_URL_TAG
ENV SHARE_YOUR_OCOBOT=

WORKDIR /octobot
# Import python dependencies

# COPY --from=base /opt/venv /opt/venv
# # Import built dependencies
# COPY --from=base /opt/efs/build /opt/efs/build

# COPY /octobot-packages/OctoBot/octobot/config /octobot/octobot/config
COPY /octobot-packages/OctoBot/docker-entrypoint.sh docker-entrypoint.sh

RUN rm -rf /var/lib/apt/lists/* \
    && ln -s /opt/venv/bin/Octane Octane # Make sure we use the virtualenv
RUN chmod +x docker-entrypoint.sh
RUN chmod +x Octane

EXPOSE 5001

HEALTHCHECK --interval=1m --timeout=30s --retries=3 CMD curl --fail http://localhost:5001 || exit 1
ENTRYPOINT ["sh","./docker-entrypoint.sh"]
