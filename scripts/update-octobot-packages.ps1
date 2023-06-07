.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -U wheel
pip install -r strategy_maker_requirements.txt

pip install -r requirements.txt
pip install -r octobot-packages/Async-Channel/requirements.txt
pip install -r octobot-packages/OctoBot-Backtesting/requirements.txt
pip install -r octobot-packages/OctoBot-Commons/requirements.txt
pip install -r octobot-packages/OctoBot-evaluators/requirements.txt
pip install -r octobot-packages/OctoBot-Services/requirements.txt
pip install -r octobot-packages/OctoBot-Tentacles-Manager/requirements.txt
pip install -r octobot-packages/OctoBot-Trading/requirements.txt
pip install -r octobot-packages/trading-backend/requirements.txt
