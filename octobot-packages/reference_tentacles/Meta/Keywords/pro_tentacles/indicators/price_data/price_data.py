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

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
    user_select_candle_source_name,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_indicator_data,
    allow_enable_plot,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)


async def get_price_data(maker, indicator, evaluator):
    candle_source = await user_select_candle_source_name(
        maker, indicator, "Select Candle Source", enable_volume=True
    )
    await allow_enable_plot(maker, indicator, f"Plot Candle {candle_source}")
    candle_data = await get_candles_(maker, candle_source)
    data_source = {
        "v": {
            "title": f"Candle {candle_source}",
            "data": candle_data,
            "chart_location": "sub-chart"
            if candle_source == PriceDataSources.VOLUME.value
            else "main-chart",
        }
    }
    return await store_indicator_data(maker, indicator, data_source)
