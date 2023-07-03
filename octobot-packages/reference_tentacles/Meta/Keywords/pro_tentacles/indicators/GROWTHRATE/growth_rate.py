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

from tentacles.Meta.Keywords.pro_tentacles.indicators.indicator_handling import (
    activate_configurable_indicator,
    get_configurable_indicator,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_indicator_data,
    allow_enable_plot,
)
import numpy as np
import tulipy
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)


async def get_growth_rate(maker, indicator, evaluator):
    selected_indicator = await activate_configurable_indicator(
        maker,
        indicator,
        def_val="price_data",
        data_source_name="data source for growth rate",
    )
    length = await user_input2(
        maker,
        indicator,
        f"{selected_indicator} growth rate MA length",
        "int",
        5,
        min_val=1,
    )
    await allow_enable_plot(maker, indicator, f"Plot {selected_indicator} growth rate")
    data_source_values, _, data_source_title = await get_configurable_indicator(
        maker, indicator
    )
    growth_rates = np.exp(np.diff(np.log(data_source_values))) - 1
    growth_rates = growth_rates * 10000
    growth_rates_ma = tulipy.ema(growth_rates, length)
    data = {
        "v": {
            "title": f"{data_source_title} growth rate",
            "data": list(growth_rates),
            "chart_location": "sub-chart",
        },
        "ma": {
            "title": f"{data_source_title} growth rate MA",
            "data": list(growth_rates_ma),
            "chart_location": "sub-chart",
        },
    }
    return await store_indicator_data(maker, indicator, data, own_yaxis=True)
