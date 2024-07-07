git stash
git pull
git checkout dev
git pull

timedatectl set-ntp true

chmod u+x scripts/update-octobot-packages.sh
chmod u+x scripts/build-and-install-octobot-tentacles.sh
chmod u+x scripts/cythonize-octobot-packages.sh
chmod u+x linux-docker_install_or_update.sh
chmod u+x linux-start-octane.sh
chmod u+x linux-install-update-and-repair-BETA-octane.sh
chmod u+x linux-install-update-and-repair-STABLE-octane.sh

mkdir -p user
cp -n ./octobot-packages/OctoBot/octobot/config/default_config.json user/config.json
cp -n scripts/.env-example-unix .env


python -m venv .venv
python3 -m venv .venv
source .venv/bin/activate
export PYTHONPATH=${PWD}/octobot-packages/Async-Channel:${PWD}/octobot-packages/OctoBot-Tentacles-Manager:${PWD}/octobot-packages/OctoBot-Commons:${PWD}/octobot-packages/OctoBot-Trading:${PWD}/octobot-packages/OctoBot-Backtesting:${PWD}/octobot-packages/OctoBot-evaluators:${PWD}/octobot-packages/OctoBot-Services:${PWD}/octobot-packages/trading-backend
pip uninstall -y octane OctoBot OctoBot-Backtesting OctoBot-Trading Async-Channel OctoBot-Evaluators OctoBot-Commons OctoBot-Tentacles-Manager OctoBot-Services
# install dev dependencies
pip install -r octobot-packages/OctoBot-Backtesting/dev_requirements.txt
pip install -r octobot-packages/OctoBot-Commons/dev_requirements.txt
pip install -r octobot-packages/OctoBot-evaluators/dev_requirements.txt
pip install -r octobot-packages/OctoBot-Services/dev_requirements.txt
pip install -r octobot-packages/OctoBot-Tentacles-Manager/dev_requirements.txt
pip install -r octobot-packages/OctoBot-Trading/dev_requirements.txt
pip install -r octobot-packages/OctoBot/dev_requirements.txt
./scripts/update-octobot-packages.sh
./scripts/build-and-install-octobot-tentacles.sh

./linux-start-octane.sh