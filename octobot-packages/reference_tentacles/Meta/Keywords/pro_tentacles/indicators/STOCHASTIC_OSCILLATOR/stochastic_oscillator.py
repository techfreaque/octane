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


async def get_stochastic_oscillator(maker, indicator, evaluator):
    k_period = await user_input2(maker, indicator, "stochastic %k length", "int", 14)
    slowing_period = await user_input2(
        maker, indicator, "stochastic %k smoothing", "int", 1
    )
    d_period = await user_input2(maker, indicator, "stochastic %d smoothing", "int", 3)
    await allow_enable_plot(maker, indicator, "plot stochastic oscillator")
    stoch_k, stoch_d = tulipy.stoch(
        await get_candles_(maker, PriceDataSources.HIGH.value),
        await get_candles_(maker, PriceDataSources.LOW.value),
        await get_candles_(maker, PriceDataSources.CLOSE.value),
        k_period,
        slowing_period,
        d_period,
    )
    data = {
        "v": {
            "title": "stochastic oscillator k",
            "data": stoch_k,
            "chart_location": "sub-chart",
        },
        "d": {
            "title": "stochastic oscillator d",
            "data": stoch_d,
            "chart_location": "sub-chart",
        },
    }
    return await store_indicator_data(maker, indicator, data)
