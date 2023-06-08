.venv\Scripts\Activate.ps1

cd octobot-packages/trading-backend
pip install -e ./
cd ..
cd ..
cd octobot-packages/Async-Channel
pip install -e ./
cd ..
cd ..
cd octobot-packages/OctoBot-Commons
pip install -e ./
cd ..
cd ..
cd octobot-packages/OctoBot-Tentacles-Manager
pip install -e ./
cd ..
cd ..
cd octobot-packages/OctoBot-Backtesting
pip install -e ./
cd ..
cd ..
cd octobot-packages/OctoBot-Trading
pip install -e ./
cd ..
cd ..
cd octobot-packages/OctoBot-Services
pip install -e ./
cd ..
cd ..
cd octobot-packages/OctoBot-evaluators
pip install -e ./
cd ..
cd ..
cd octobot-packages/OctoBot
pip install -e ./
cd ..
cd ..
