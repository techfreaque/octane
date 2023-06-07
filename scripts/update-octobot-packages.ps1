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

robocopy reference_profiles/Arbitrage_Strategy_Maker_Strategy/ user/profiles/Arbitrage_Strategy_Maker_Strategy/ /MIR
robocopy reference_profiles/arbitrage_trading/ user/profiles/arbitrage_trading/ /MIR
robocopy reference_profiles/Break_out_strategy/ user/profiles/Break_out_strategy/ /MIR
robocopy reference_profiles/camarilla_strategy_v2 user/profiles/camarilla_strategy_v2/ /MIR
robocopy reference_profiles/copy_trading/ user/profiles/copy_trading/ /MIR
robocopy reference_profiles/daily_trading/ user/profiles/daily_trading/ /MIR
robocopy reference_profiles/dip_analyser/ user/profiles/dip_analyser/ /MIR
robocopy reference_profiles/EMA_Grid_Strategy/ user/profiles/EMA_Grid_Strategy/ /MIR
robocopy reference_profiles/gpt_trading/ user/profiles/gpt_trading/ /MIR
robocopy reference_profiles/grid_trading/ user/profiles/grid_trading/ /MIR
robocopy reference_profiles/investobot_apollo/ user/profiles/investobot_apollo/ /MIR
robocopy reference_profiles/Hypertrend_Strategy/ user/profiles/Hypertrend_Strategy/ /MIR
robocopy reference_profiles/investobot_zeus/ user/profiles/investobot_zeus/ /MIR
robocopy reference_profiles/magic_trend/ user/profiles/magic_trend/ /MIR

robocopy reference_profiles/Lorentzian_Classification_with_Tokens/ user/profiles/Lorentzian_Classification_with_Tokens/ /MIR
robocopy reference_profiles/Lorentzian_Strategy_Maker/ user/profiles/Lorentzian_Strategy_Maker/ /MIR
robocopy reference_profiles/Multi_Time_EMA_Aligned_Strategy/ user/profiles/Multi_Time_EMA_Aligned_Strategy/ /MIR
robocopy reference_profiles/Multi_Time_EMA_Claim_Strategy/ user/profiles/Multi_Time_EMA_Claim_Strategy/ /MIR
robocopy reference_profiles/My_Lorentzian_Classification/ user/profiles/My_Lorentzian_Classification/ /MIR
robocopy reference_profiles/my_spot_master_3000/ user/profiles/my_spot_master_3000/ /MIR
robocopy reference_profiles/Deep_Convolution_Neural_Net_Strategy/ user/profiles/Deep_Convolution_Neural_Net_Strategy/ /MIR
robocopy reference_profiles/non-trading/ user/profiles/non-trading/ /MIR
robocopy reference_profiles/Semi_Auto_Trading_Strategy/ user/profiles/Semi_Auto_Trading_Strategy/ /MIR
robocopy reference_profiles/signal_trading/ user/profiles/signal_trading/ /MIR
robocopy reference_profiles/simple_dca/ user/profiles/simple_dca/ /MIR
robocopy reference_profiles/spot_master_3000_strategy/ user/profiles/spot_master_3000_strategy/ /MIR
robocopy reference_profiles/staggered_orders_trading/ user/profiles/staggered_orders_trading/ /MIR
robocopy reference_profiles/tradingview_trading/ user/profiles/tradingview_trading /MIR