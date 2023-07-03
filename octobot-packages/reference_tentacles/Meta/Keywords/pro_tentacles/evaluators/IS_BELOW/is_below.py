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
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.above_below.is_above_below import (
    is_below,
)


async def get_is_below(maker, evaluator):
    below_values_title = await activate_configurable_indicator(
        maker, evaluator, data_source_name="data source below", def_val="EMA"
    )
    above_values_title = await activate_configurable_indicator(
        maker,
        evaluator,
        def_val="price_data",
        indicator_id=2,
        data_source_name="data source above",
    )
    confirmation_time = await user_input2(maker, evaluator, "signal delay", "int", 0)
    below_percent = await user_input2(
        maker,
        evaluator,
        f"percent {below_values_title} needs to be " f"below {above_values_title}",
        "int",
        0,
    )
    await allow_enable_plot(
        maker,
        evaluator,
        f"Plot when {below_values_title} is below {above_values_title}",
    )
    (
        data_below_values,
        evaluator.chart_location,
        above_values_detailed_title,
    ) = await get_configurable_indicator(maker, evaluator)
    evaluator.values, _, below_values_detailed_title = await get_configurable_indicator(
        maker, evaluator, indicator_id=2
    )
    evaluator.signals = is_below(
        above_data=evaluator.values,
        below_data=data_below_values,
        confirmation_time=confirmation_time,
        below_percent=below_percent,
        max_history=not maker.live_recording_mode,
    )
    evaluator.title = (
        f"{above_values_detailed_title} is below {below_values_detailed_title}"
    )
    return await store_evaluator_data(maker, evaluator)
