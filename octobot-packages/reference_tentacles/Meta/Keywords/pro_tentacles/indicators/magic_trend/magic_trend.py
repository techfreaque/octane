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

import numpy as numpy
import tulipy
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    cut_data_to_same_len,
    store_indicator_data,
    allow_enable_plot,
)


async def get_magic_trend(maker, indicator, evaluator):
    cci_length = await user_input2(maker, indicator, "CCI length", "int", 20, 1)
    atr_multiplier = await user_input2(
        maker, indicator, "ATR multiplier", "float", 1, 0.001
    )
    atr_length = await user_input2(maker, indicator, "ATR length", "int", 5, 1)
    await allow_enable_plot(maker, indicator, "Plot Magic trend")

    highs = await get_candles_(maker, PriceDataSources.HIGH.value)
    lows = await get_candles_(maker, PriceDataSources.LOW.value)
    closes = await get_candles_(maker, PriceDataSources.CLOSE.value)
    tr = tulipy.tr(
        highs,
        lows,
        closes,
    )
    atr = tulipy.sma(tr, atr_length)
    cci = tulipy.cci(highs, lows, closes, cci_length)
    highs, tr, atr, lows, closes, cci = cut_data_to_same_len(
        (highs, tr, atr, lows, closes, cci)
    )
    up_t = lows - atr * atr_multiplier
    down_t = highs + atr * atr_multiplier
    cci_above_o = cci >= 0
    magic_trend = []
    for index, this_cci_above_0 in enumerate(cci_above_o):
        this_magic_trend = magic_trend[-1] if len(magic_trend) else 0
        if this_cci_above_0:
            upt_above_mi = up_t[index] < this_magic_trend
            if upt_above_mi:
                magic_trend.append(this_magic_trend)
            else:
                magic_trend.append(up_t[index])
        else:
            upt_above_mi = down_t[index] > this_magic_trend
            if upt_above_mi:
                magic_trend.append(this_magic_trend)
            else:
                magic_trend.append(down_t[index])
    data_source = {
        "v": {
            "title": f"Magic trend {cci_length}-{atr_multiplier}-{atr_length}",
            "data": magic_trend[3:],  # remove first few as there are zeros
            "chart_location": "main-chart",
        }
    }
    return await store_indicator_data(maker, indicator, data_source)
