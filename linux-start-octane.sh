source ${PWD}/.venv/bin/activate
export PYTHONPATH=${PWD}/octobot-packages/Async-Channel:${PWD}/octobot-packages/OctoBot-Tentacles-Manager:${PWD}/octobot-packages/OctoBot-Commons:${PWD}/octobot-packages/OctoBot-Trading:${PWD}/octobot-packages/OctoBot-Backtesting:${PWD}/octobot-packages/OctoBot-evaluators:${PWD}/octobot-packages/OctoBot-Services:${PWD}/octobot-packages/trading-backend
python octobot-packages/OctoBot/start.py
