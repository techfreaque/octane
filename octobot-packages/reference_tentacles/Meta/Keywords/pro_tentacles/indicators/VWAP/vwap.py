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

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)
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
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.vwap_lib.vwap_library import (
    calculate_historical_VWAP,
)


async def get_VWAP(maker, indicator, evaluator):
    selected_vwap_timeframe = await user_input2(
        maker,
        indicator,
        "VWAP time Window",
        "options",
        "24h",
        options=["24h", "session", "week", "month"],
    )
    candle_source = await user_select_candle_source_name(
        maker, indicator, "Select VWAP Candle Source", PriceDataSources.HLC3.value
    )
    await allow_enable_plot(maker, indicator, "Plot VWAP")
    vwap_data = calculate_historical_VWAP(
        await get_candles_(maker, candle_source),
        await get_candles_(maker, PriceDataSources.VOLUME.value),
        time_data=await get_candles_(maker, PriceDataSources.TIME.value),
        window=selected_vwap_timeframe,
        time_frame=maker.ctx.time_frame,
    )
    data_source = {
        "v": {
            "title": f"VWAP {selected_vwap_timeframe}",
            "data": vwap_data,
            "chart_location": "main-chart",
        }
    }
    return await store_indicator_data(maker, indicator, data_source)
