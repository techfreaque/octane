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
    user_select_candle_source_name,
)
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_indicator_data,
    allow_enable_plot,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)


async def get_ALMA(maker, indicator, evaluator):
    length = await user_input2(maker, indicator, "ALMA length", "int", 50, 0)
    offset = await user_input2(maker, indicator, "Offset", "float", 0.85)
    sigma = await user_input2(maker, indicator, "Sigma", "int", 6)
    candle_source = await user_select_candle_source_name(
        maker, indicator, "Select ALMA Candle Source"
    )
    await allow_enable_plot(maker, indicator, f"Plot ALMA")
    m_time = utilities.start_measure_time(message=None)
    candle_data = pd.Series(await get_candles_(maker, candle_source))
    alma_series = pta.alma(
        close=candle_data, length=length, distribution_offset=offset, sigma=sigma
    )
    alma_series = alma_series.dropna()
    data_source = {
        "v": {
            "title": f"ALMA {length}-{offset}-{sigma}",
            "data": alma_series.to_list()[1:],
            "chart_location": "main-chart",
        }
    }
    utilities.end_measure_time(
        m_time, message="Alma took longer than expected", min_duration=10
    )
    return await store_indicator_data(maker, indicator, data_source)
