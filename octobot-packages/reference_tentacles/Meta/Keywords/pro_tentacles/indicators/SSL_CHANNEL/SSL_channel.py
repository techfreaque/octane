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
    store_indicator_data,
    allow_enable_plot,
)


async def get_SSL_channel(maker, indicator, evaluator):
    length = await user_input2(maker, indicator, "SSL length", "int", 50, 0)
    await allow_enable_plot(maker, indicator, "Plot SSL Channel")
    lows = await get_candles_(maker, PriceDataSources.LOW.value)
    highs = await get_candles_(maker, PriceDataSources.HIGH.value)
    closes = await get_candles_(maker, PriceDataSources.CLOSE.value)
    ssl_down, ssl_up = compute_ssl_channel(highs, lows, closes, length)
    data = {
        "v": {
            "title": f"SSL Down l:{length}",
            "data": ssl_down,
            "chart_location": "main-chart",
        },
        "s": {
            "title": f"SSL UP l:{length}",
            "data": ssl_up,
            "chart_location": "main-chart",
        },
    }
    return await store_indicator_data(maker, indicator, data)


def compute_ssl_channel(highs, lows, closes, length):
    sma_high = tulipy.ema(highs, length)
    sma_low = tulipy.ema(lows, length)
    ssl_down = []
    ssl_up = []
    hlv = []
    data_length = len(sma_high)
    closes = closes[-data_length:]
    for index in range(1, len(sma_high)):
        if closes[index] > sma_high[index]:
            hlv.append(1)
            ssl_down.append(sma_low[index])
            ssl_up.append(sma_high[index])
        elif closes[index] < sma_low[index]:
            hlv.append(-1)
            ssl_down.append(sma_high[index])
            ssl_up.append(sma_low[index])
        elif hlv:
            if hlv[-1] > 0:
                hlv.append(1)
                ssl_down.append(sma_low[index])
                ssl_up.append(sma_high[index])
            elif hlv[-1] < 0:
                hlv.append(-1)
                ssl_down.append(sma_high[index])
                ssl_up.append(sma_low[index])
            else:
                ssl_down.append(0)
                ssl_up.append(0)
    return ssl_down, ssl_up
