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
from tentacles.Meta.Keywords.indicator_keywords.moving.moving_up_down import (
    moving_down_,
)
from tentacles.Meta.Keywords.pro_tentacles.indicators.indicator_handling import (
    get_configurable_indicator,
    activate_configurable_indicator,
)


async def get_is_falling(maker, evaluator):
    selected_indicator = await activate_configurable_indicator(
        maker, evaluator, enable_static_value=False
    )
    signal_lag = await user_input2(
        maker,
        evaluator,
        "Amount of consecutive falling candles before flashing a signal",
        "int",
        2,
        1,
    )
    sideways_is_falling = await user_input2(
        maker, evaluator, "Sideways counts as falling", "boolean", True
    )
    only_one_signal = await user_input2(
        maker, evaluator, "Flash signals only on the first candle", "boolean", False
    )
    await allow_enable_plot(
        maker, evaluator, f"Plot when {selected_indicator} is falling"
    )

    (
        evaluator.values,
        evaluator.chart_location,
        indicator_title,
    ) = await get_configurable_indicator(maker, evaluator)
    evaluator.signals = moving_down_(
        evaluator.values,
        signal_lag,
        sideways_is_falling=sideways_is_falling,
        calculate_full_history=not maker.live_recording_mode,
        only_first_signal=only_one_signal,
    )
    evaluator.title = f"{indicator_title} is falling"
    return await store_evaluator_data(maker, evaluator)
