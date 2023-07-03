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

from finta import TA as fta
import pandas as pd
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


async def get_ichimoku(maker, indicator, evaluator):
    conversion_line_length = await user_input2(
        maker, indicator, "conversion line length", "int", 9
    )
    base_line_length = await user_input2(
        maker, indicator, "base line length", "int", 26
    )
    leading_span_b_length = await user_input2(
        maker, indicator, "leading span b length", "int", 52
    )
    displacement = await user_input2(maker, indicator, "displacement", "int", 26)
    await allow_enable_plot(maker, indicator, "Plot ichimoku")
    df = pd.DataFrame(
        {
            "open": await get_candles_(maker, PriceDataSources.OPEN.value),
            "high": await get_candles_(maker, PriceDataSources.HIGH.value),
            "low": await get_candles_(maker, PriceDataSources.LOW.value),
            "close": await get_candles_(maker, PriceDataSources.CLOSE.value),
        }
    )
    ichimoku_df = fta.ICHIMOKU(
        df,
        tenkan_period=conversion_line_length,
        kijun_period=base_line_length,
        senkou_period=leading_span_b_length,
        chikou_period=displacement,
    )
    ichimoku_df = ichimoku_df.drop(["CHIKOU"], axis=1)
    ichimoku_df = ichimoku_df.dropna()
    data = {
        "v": {
            "title": "ichimoku conversion line",
            "data": list(ichimoku_df["TENKAN"]),
            "chart_location": "main-chart",
        },
        "b": {
            "title": "ichimoku base line",
            "data": list(ichimoku_df["KIJUN"]),
            "chart_location": "main-chart",
        },
        "lsb": {
            "title": "ichimoku leading span b",
            "data": list(ichimoku_df["SENKOU"]),
            "chart_location": "main-chart",
        },
        "lsa": {
            "title": "ichimoku leading span a",
            "data": list(ichimoku_df["senkou_span_a"]),
            "chart_location": "main-chart",
        },
    }
    return await store_indicator_data(maker, indicator, data)
