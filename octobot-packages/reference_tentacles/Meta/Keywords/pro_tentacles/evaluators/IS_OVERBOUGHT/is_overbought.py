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

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_evaluator_data,
    allow_enable_plot,
)
from tentacles.Meta.Keywords.pro_tentacles.indicators.indicator_handling import (
    get_configurable_indicator,
    activate_configurable_indicator,
)


async def get_is_overbought(maker, evaluator):
    selected_indicator = await activate_configurable_indicator(
        maker,
        evaluator,
        def_val="MACD",
        enable_price_indicators=False,
        enable_price_data=False,
    )
    osc_is_ob_val = await user_input2(
        maker,
        evaluator,
        f"show signals if {selected_indicator} is currently above:",
        "int",
        40,
    )
    enable_was_ob = await user_input2(
        maker, evaluator, "enable was also above in the past", "boolean", False
    )
    osc_was_ob_val = osc_is_ob_val
    osc_was_within = 1
    if enable_was_ob:
        osc_was_within = await user_input2(
            maker, evaluator, "within the last x candles (0 = disabled)", "int", 3, 0
        )
        if int(osc_was_within) != 0:
            osc_was_ob_val = await user_input2(
                maker,
                evaluator,
                "show signals if the oscillator was " "above in the past:",
                "int",
                30,
            )
        else:
            osc_was_within = 1
    await allow_enable_plot(
        maker, evaluator, f"Plot when {selected_indicator} is above"
    )
    (
        evaluator.values,
        evaluator.chart_location,
        indicator_title,
    ) = await get_configurable_indicator(maker, evaluator)
    evaluator.signals = []
    indicator_d_length = len(evaluator.values)
    for i in range(osc_was_within, indicator_d_length):
        overbought_data = evaluator.values[i] > osc_is_ob_val
        overbought_data = (
            overbought_data
            and max(evaluator.values[i + 1 - osc_was_within : i + 1]) > osc_was_ob_val
        )
        evaluator.signals.append(1 if overbought_data else 0)

    evaluator.second_values = (
        [osc_is_ob_val] * indicator_d_length if evaluator.plot else []
    )
    evaluator.second_title = f"Overbought line ({osc_is_ob_val})"
    evaluator.second_chart_location = "sub-chart"

    evaluator.title = f"{indicator_title} is overbought"
    return await store_evaluator_data(maker, evaluator)
