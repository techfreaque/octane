git checkout dev
git reset --hard origin/dev
git pull
scripts\update-octobot-packages.ps1

# install dev dependencies
.venv\Scripts\Activate.ps1
pip uninstall -y octane  OctoBot OctoBot-Backtesting OctoBot-Trading Async-Channel OctoBot-Evaluators OctoBot-Commons OctoBot-Tentacles-Manager OctoBot-Services
pip install -r octobot-packages/OctoBot-Backtesting/dev_requirements.txt
pip install -r octobot-packages/OctoBot-Commons/dev_requirements.txt
pip install -r octobot-packages/OctoBot-evaluators/dev_requirements.txt
pip install -r octobot-packages/OctoBot-Services/dev_requirements.txt
pip install -r octobot-packages/OctoBot-Tentacles-Manager/dev_requirements.txt
pip install -r octobot-packages/OctoBot-Trading/dev_requirements.txt
pip install -r octobot-packages/trading-backend/dev_requirements.txt
pip install -r octobot-packages/Async-Channel/dev_requirements.txt
pip install -r octobot-packages/OctoBot/dev_requirements.txt

scripts\build-and-install-octobot-tentacles.ps1