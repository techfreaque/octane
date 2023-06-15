.venv\Scripts\Activate.ps1
$Env:PYTHONPATH = "./octobot-packages/Async-Channel;./octobot-packages/OctoBot-Tentacles-Manager;./octobot-packages/OctoBot-Commons;./octobot-packages/OctoBot-Trading;./octobot-packages/OctoBot-Backtesting;./octobot-packages/OctoBot-evaluators;./octobot-packages/OctoBot-Services;./octobot-packages/trading-backend"
$Env:EXIT_BEFORE_TENTACLES_AUTO_REINSTALL="True"
python ./octobot-packages/OctoBot/start.py
