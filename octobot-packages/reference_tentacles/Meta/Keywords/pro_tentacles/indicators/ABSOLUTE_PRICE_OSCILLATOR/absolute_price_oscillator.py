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
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
    user_select_candle_source_name,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_indicator_data,
    allow_enable_plot,
)


async def get_absolute_price_oscillator(maker, indicator, evaluator):
    fast_length = await user_input2(
        maker, indicator, "Absolute Price Oscillator fast length", "int", 12
    )
    slow_length = await user_input2(
        maker, indicator, "Absolute Price Oscillator slow length", "int", 26
    )
    candle_source = await user_select_candle_source_name(
        maker, indicator, "Select Candle Source"
    )
    await allow_enable_plot(maker, indicator, "plot Absolute Price Oscillator")
    try:
        data = tulipy.apo(
            await get_candles_(maker, candle_source), fast_length, slow_length
        )
    except tulipy.lib.InvalidOptionError:
        raise RuntimeError(
            f"Absolute Price Oscillator (slow: {slow_length} fast: {fast_length}): "
            f"fast length cant be longer than slow length"
        )
    data = {
        "v": {
            "title": f"Absolute Price Oscillator ({fast_length}-{slow_length})",
            "data": data,
            "chart_location": "sub-chart",
        }
    }
    return await store_indicator_data(maker, indicator, data)
