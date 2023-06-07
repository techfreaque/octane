#!/bin/bash

# if [[ -n "${OCTOBOT_CONFIG}" ]]; then
#   echo "$OCTOBOT_CONFIG" | tee /octobot/octobot/user/config.json > /dev/null
# fi

/octobot/OctoBot tentacles -p /octobot/output/any_platform.zip -d /octobot-packages/octobot-packages/reference_tentacles
/octobot/OctoBot tentacles --install --all --location /octobot/output/any_platform.zip

/octobot/OctoBot
