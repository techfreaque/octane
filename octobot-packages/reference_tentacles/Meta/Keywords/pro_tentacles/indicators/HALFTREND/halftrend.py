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


async def get_halftrend(maker, indicator, evaluator):
    amplitude = await user_input2(maker, indicator, "amplitude", "int", 2)
    channel_deviation = await user_input2(
        maker, indicator, "channel deviation", "float", 2
    )
    await allow_enable_plot(maker, indicator, "plot Halftrend")
    highs = await get_candles_(maker, PriceDataSources.HIGH.value)
    lows = await get_candles_(maker, PriceDataSources.LOW.value)
    closes = await get_candles_(maker, PriceDataSources.CLOSE.value)
    atr = tulipy.atr(highs, lows, closes, 100) / 2
    atr_with_deviation = atr * channel_deviation
    high_prices = tulipy.max(highs, amplitude)
    low_prices = tulipy.min(highs, amplitude)
    high_ma = tulipy.sma(highs, amplitude)
    low_ma = tulipy.sma(lows, amplitude)
    data_length = min(
        highs.size,
        lows.size,
        closes.size,
        atr.size,
        atr_with_deviation.size,
        high_prices.size,
        low_prices.size,
        high_ma.size,
        low_ma.size,
    )
    (
        highs,
        lows,
        closes,
        atr,
        atr_with_deviation,
        high_prices,
        high_prices,
        high_ma,
        low_ma,
    ) = (
        highs[-data_length:],
        lows[-data_length:],
        closes[-data_length:],
        atr[-data_length:],
        atr_with_deviation[-data_length:],
        low_prices[-data_length:],
        high_prices[-data_length:],
        high_ma[-data_length:],
        low_ma[-data_length:],
    )
    half_trend = []
    next_trend = 0
    trend = 0
    next_trends = [0]
    trends = [0]
    max_low_price = lows[0]
    min_high_price = highs[0]
    up = 0.0
    down = 0.0
    ups = []
    downs = []
    atr_highs = []
    atr_lows = []
    arrow_up = []
    arrow_down = []
    for index in range(1, data_length):
        if next_trend == 1:
            max_low_price = max(low_prices[index], max_low_price)
            if high_ma[index] < max_low_price and closes[index - 1] < lows[index]:
                trend = 1
                next_trend = 0
                min_high_price = high_prices[index]
        else:
            min_high_price = min(high_prices[index], min_high_price)
            if low_ma[index] > min_high_price and closes[index - 1] > highs[index]:
                trend = 0
                next_trend = 1
                max_low_price = low_prices[index]
        next_trends.append(next_trend)
        trends.append(trend)
        if trend == 0:
            if trends[index - 1] != 0:
                up = downs[-1]
                arrow_up = up - atr[index]
            else:
                try:
                    up = max(max_low_price, ups[-1])
                except IndexError:
                    up = max_low_price
            atr_lows.append(up + atr_with_deviation[index])
            atr_highs.append(up - atr_with_deviation[index])
        else:
            if trends[index - 1] != 1:
                down = ups[-1]
                arrow_down = down + atr[index]
            else:
                down = max(min_high_price, downs[-1])
            atr_lows.append(down + atr_with_deviation[index])
            atr_highs.append(down - atr_with_deviation[index])
        ups.append(up)
        downs.append(down)
        half_trend.append(up if trend == 0 else down)
    data = {
        "v": {
            "title": f"Half Trend ({amplitude}-{channel_deviation})",
            "data": half_trend,
            "chart_location": "main-chart",
        },
        "h": {
            "title": f"ATR High ({amplitude}-{channel_deviation})",
            "data": atr_highs,
            "chart_location": "main-chart",
        },
        "l": {
            "title": f"ATR Low ({amplitude}-{channel_deviation})",
            "data": atr_lows,
            "chart_location": "main-chart",
        },
    }
    return await store_indicator_data(maker, indicator, data)
