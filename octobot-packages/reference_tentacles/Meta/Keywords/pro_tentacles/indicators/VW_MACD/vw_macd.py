# a42.ch CONFIDENTIAL
# __________________
#
#  [2021] - [∞] a42.ch Incorporated
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of a42.ch Incorporated and its suppliers,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to a42.ch Incorporated
# and its suppliers and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from a42.ch Incorporated.
#
# If you want to use any code for commercial purposes,
# or you want your own custom solution,
# please contact me at max@a42.ch

import pandas as pd
from finta import TA as fta
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_indicator_data,
    allow_enable_plot,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)


async def get_VW_MACD(maker, indicator, evaluator):
    fast_length = await user_input2(maker, indicator, "VW MACD fast length", "int", 12)
    slow_length = await user_input2(maker, indicator, "VW MACD slow length", "int", 26)
    signal_smoothing = await user_input2(
        maker, indicator, "VW MACD signal smoothing", "int", 9
    )
    await allow_enable_plot(maker, indicator, "Plot VW MACD")
    df = pd.DataFrame(
        {
            "open": await get_candles_(maker, PriceDataSources.OPEN.value),
            "high": await get_candles_(maker, PriceDataSources.HIGH.value),
            "low": await get_candles_(maker, PriceDataSources.LOW.value),
            "close": await get_candles_(maker, PriceDataSources.CLOSE.value),
            "volume": await get_candles_(maker, PriceDataSources.VOLUME.value),
        }
    )
    macd_df = fta.VW_MACD(
        df, period_fast=fast_length, period_slow=slow_length, signal=signal_smoothing
    )
    data = {
        "v": {
            "title": f"VW MACD ({signal_smoothing}-{fast_length}-{slow_length})",
            "data": list(macd_df.iloc[slow_length * 2 :, 1]),
            "chart_location": "sub-chart",
        },
        "s": {
            "title": f"VW MACD Signal ({signal_smoothing}-{fast_length}-{slow_length})",
            "data": list(macd_df.iloc[slow_length * 2 :, 0]),
            "chart_location": "sub-chart",
        },
    }
    return await store_indicator_data(maker, indicator, data)
