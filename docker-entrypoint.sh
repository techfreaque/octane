#!/bin/bash

# if [[ -n "${OCTOBOT_CONFIG}" ]]; then
#   echo "$OCTOBOT_CONFIG" | tee /octobot/octobot/user/config.json > /dev/null
# fi

/octobot/OctoBot tentacles -p /octobot/output/any_platform.zip -d /octobot/reference_tentacles
/octobot/OctoBot tentacles --install --all --location /octobot/output/any_platform.zip

mkdir /octobot/user/profiles

rsync -a --delete -vh reference_profiles/Arbitrage_Strategy_Maker_Strategy/ user/profiles/Arbitrage_Strategy_Maker_Strategy/
rsync -a --delete -vh reference_profiles/arbitrage_trading/ user/profiles/arbitrage_trading/
rsync -a --delete -vh reference_profiles/Break_out_strategy/ user/profiles/Break_out_strategy/
rsync -a --delete -vh reference_profiles/camarilla_strategy_v2_default user/profiles/camarilla_strategy_v2_default/
rsync -a --delete -vh reference_profiles/copy_trading/ user/profiles/copy_trading/
rsync -a --delete -vh reference_profiles/daily_trading/ user/profiles/daily_trading/
rsync -a --delete -vh reference_profiles/dip_analyser/ user/profiles/dip_analyser/
rsync -a --delete -vh reference_profiles/Deep_Convolution_Neural_Net_Strategy/ user/profiles/Deep_Convolution_Neural_Net_Strategy/
rsync -a --delete -vh reference_profiles/EMA_Grid_Strategy/ user/profiles/EMA_Grid_Strategy/
rsync -a --delete -vh reference_profiles/gpt_trading/ user/profiles/gpt_trading/
rsync -a --delete -vh reference_profiles/grid_trading/ user/profiles/grid_trading/
rsync -a --delete -vh reference_profiles/investobot_apollo/ user/profiles/investobot_apollo/
rsync -a --delete -vh reference_profiles/Hypertrend_Strategy/ user/profiles/Hypertrend_Strategy/
rsync -a --delete -vh reference_profiles/investobot_zeus/ user/profiles/investobot_zeus/
rsync -a --delete -vh reference_profiles/Lorentzian_Classification_with_Tokens/ user/profiles/Lorentzian_Classification_with_Tokens/
rsync -a --delete -vh reference_profiles/Lorentzian_Strategy_Maker/ user/profiles/Lorentzian_Strategy_Maker/
rsync -a --delete -vh reference_profiles/Multi_Time_EMA_Aligned_Strategy/ user/profiles/Multi_Time_EMA_Aligned_Strategy/
rsync -a --delete -vh reference_profiles/Multi_Time_EMA_Claim_Strategy/ user/profiles/Multi_Time_EMA_Claim_Strategy/
rsync -a --delete -vh reference_profiles/magic_trend/ user/profiles/magic_trend/
rsync -a --delete -vh reference_profiles/My_Lorentzian_Classification/ user/profiles/My_Lorentzian_Classification/
rsync -a --delete -vh reference_profiles/my_spot_master_3000/ user/profiles/my_spot_master_3000/
rsync -a --delete -vh reference_profiles/non-trading/ user/profiles/non-trading/
rsync -a --delete -vh reference_profiles/Semi_Auto_Trading_Strategy/ user/profiles/Semi_Auto_Trading_Strategy/
rsync -a --delete -vh reference_profiles/signal_trading/ user/profiles/signal_trading/
rsync -a --delete -vh reference_profiles/simple_dca/ user/profiles/simple_dca/
rsync -a --delete -vh reference_profiles/spot_master_3000_strategy/ user/profiles/spot_master_3000_strategy/
rsync -a --delete -vh reference_profiles/staggered_orders_trading/ user/profiles/staggered_orders_trading/
rsync -a --delete -vh reference_profiles/tradingview_trading/ user/profiles/tradingview_trading/


/octobot/OctoBot
