# install tentacles to bump versions
$Env:PYTHONPATH = "./octobot-packages/Async-Channel;./octobot-packages/OctoBot-Tentacles-Manager;./octobot-packages/OctoBot-Commons;./octobot-packages/OctoBot-Trading;./octobot-packages/OctoBot-Backtesting;./octobot-packages/OctoBot-evaluators;./octobot-packages/OctoBot-Services;./octobot-packages/trading-backend"
.\.venv\Scripts\python.exe octobot-packages/OctoBot/start.py tentacles -p ./any_platform.zip -d ./octobot-packages/reference_tentacles
.\.venv\Scripts\python.exe octobot-packages/OctoBot/start.py tentacles --install --all --location ./output/any_platform.zip

# clean
Remove-Item ./output -Force  -Recurse -ErrorAction SilentlyContinue