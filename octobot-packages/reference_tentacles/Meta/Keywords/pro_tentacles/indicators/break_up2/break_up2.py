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

import numpy

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2.user_input2_ import (
    user_input2,
)
from tentacles.Meta.Keywords.pro_tentacles.indicators.indicator_handling import (
    activate_configurable_indicator,
    get_configurable_indicator,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    cut_data_to_same_len,
    store_indicator_data,
    allow_enable_plot,
)


async def get_break_up2(maker, indicator, evaluator):
    _ = await activate_configurable_indicator(
        maker,
        indicator,
        enable_force_def_val=True,
        data_source_name="Break up data source",
        def_val="break_up",
    )
    _ = await activate_configurable_indicator(
        maker,
        indicator,
        enable_force_def_val=True,
        indicator_id=2,
        data_source_name="H4 data source",
        def_val="special_highs",
    )
    fib_extension = await user_input2(
        maker, indicator, "Fib extension value", "float", 1.168
    )
    await allow_enable_plot(maker, indicator, "Plot break up 2")
    (
        indictaror_1_data,
        _,
        indictaror_1_title,
    ) = await get_configurable_indicator(maker, indicator)
    (
        indictaror_2_data,
        _,
        indictaror_2_title,
    ) = await get_configurable_indicator(maker, indicator, indicator_id=2)
    indictaror_1_data, indictaror_2_data = cut_data_to_same_len(
        (indictaror_1_data, indictaror_2_data)
    )
    indictaror_1_data = numpy.array(indictaror_1_data)
    indictaror_2_data = numpy.array(indictaror_2_data)
    data = indictaror_1_data + fib_extension * (indictaror_1_data - indictaror_2_data)
    data_source = {
        "v": {
            "title": f"Break up 2 (from {indictaror_2_title})",
            "data": data,
            "chart_location": "main-chart",
        }
    }
    return await store_indicator_data(maker, indicator, data_source)
