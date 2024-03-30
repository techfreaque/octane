source .venv/bin/activate
python -m pip install --upgrade pip
pip install -U wheel
pip install -r octobot-packages/OctoBot/strategy_maker_requirements.txt

pip install -r octobot-packages/OctoBot/requirements.txt
pip install -r octobot-packages/OctoBot-Backtesting/requirements.txt
pip install -r octobot-packages/OctoBot-Commons/requirements.txt
pip install -r octobot-packages/OctoBot-evaluators/requirements.txt
pip install -r octobot-packages/OctoBot-Services/requirements.txt
pip install -r octobot-packages/OctoBot-Tentacles-Manager/requirements.txt
pip install -r octobot-packages/OctoBot-Trading/requirements.txt
pip install -r octobot-packages/Async-Channel/requirements.txt
cp -n scripts/custom_requirements.txt.template custom_requirements.txt
pip install -r custom_requirements.txt
