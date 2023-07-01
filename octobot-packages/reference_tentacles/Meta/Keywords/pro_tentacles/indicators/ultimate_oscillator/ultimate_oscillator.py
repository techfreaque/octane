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


async def get_ultimate_oscillator(maker, indicator, evaluator):
    short_length = await user_input2(
        maker,
        indicator,
        "ultimate oscillator short period",
        "int",
        def_val=20,
        min_val=1,
    )
    medium_length = await user_input2(
        maker,
        indicator,
        "ultimate oscillator medium period",
        "int",
        def_val=30,
        min_val=2,
    )
    long_length = await user_input2(
        maker,
        indicator,
        "ultimate oscillator long period",
        "int",
        def_val=40,
        min_val=3,
    )
    await allow_enable_plot(maker, indicator, "Plot ultimate oscillator")
    data = tulipy.ultosc(
        await get_candles_(maker, PriceDataSources.HIGH.value),
        await get_candles_(maker, PriceDataSources.LOW.value),
        await get_candles_(maker, PriceDataSources.CLOSE.value),
        short_length,
        medium_length,
        long_length,
    )
    data_source = {
        "v": {
            "title": f"ultimate oscillator {short_length}-{medium_length}-{long_length}",
            "data": data,
            "chart_location": "main-chart",
        }
    }
    return await store_indicator_data(maker, indicator, data_source)
