# install tentacles to bump versions
source .venv/bin/activate
export PYTHONPATH=${PWD}/octobot-packages/Async-Channel:${PWD}/octobot-packages/OctoBot-Tentacles-Manager:${PWD}/octobot-packages/OctoBot-Commons:${PWD}/octobot-packages/OctoBot-Trading:${PWD}/octobot-packages/OctoBot-Backtesting:${PWD}/octobot-packages/OctoBot-evaluators:${PWD}/octobot-packages/OctoBot-Services:${PWD}/octobot-packages/trading-backend
python octobot-packages/OctoBot/start.py tentacles -p ./any_platform.zip -d ./octobot-packages/reference_tentacles
python octobot-packages/OctoBot/start.py tentacles --install --all --location ./output/any_platform.zip

# clean
rm -R ./output