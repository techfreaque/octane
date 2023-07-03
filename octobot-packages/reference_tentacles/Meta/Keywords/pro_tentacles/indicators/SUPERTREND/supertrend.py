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
import pandas_ta as pta
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


async def get_supertrend(maker, indicator, evaluator):
    multiplier = await user_input2(
        maker, indicator, "supertrend ATR multiplier", "int", 3
    )
    length = await user_input2(maker, indicator, "supertrend ATR period", "int", 10)
    await allow_enable_plot(maker, indicator, "Plot Supertrend")
    highs = pd.Series(await get_candles_(maker, PriceDataSources.HIGH.value))
    lows = pd.Series(await get_candles_(maker, PriceDataSources.LOW.value))
    closes = pd.Series(await get_candles_(maker, PriceDataSources.CLOSE.value))
    strend_df = pta.supertrend(
        highs, lows, closes, length=length, multiplier=multiplier
    )
    try:
        strend_df = strend_df.drop(strend_df.columns[[2, 3]], axis=1)
    except AttributeError as error:
        raise RuntimeError("Supertrend doesnt have enough data") from error
    strend_df = strend_df.dropna()
    supert = strend_df.iloc[1:, 0]
    data_sources = {
        "v": {
            "title": f"supertrend (m:{multiplier}-l:{length})",
            "data": list(supert),
            "chart_location": "main-chart",
        }
    }
    return await store_indicator_data(maker, indicator, data_sources)
