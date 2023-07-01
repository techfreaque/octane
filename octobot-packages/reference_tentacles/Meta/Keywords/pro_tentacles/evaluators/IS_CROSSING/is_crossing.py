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
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.crossing import (
    crossing_up_,
    crossing_down_,
    crossing_,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    cut_data_to_same_len,
    store_evaluator_data,
    allow_enable_plot,
)
from tentacles.Meta.Keywords.pro_tentacles.indicators.indicator_handling import (
    activate_multiple_configurable_indicators,
    get_configurable_indicator,
    activate_configurable_indicator,
    get_configurable_indicators,
)


async def get_is_crossing(maker, evaluator):
    crossing_values_title = await activate_configurable_indicator(
        maker,
        evaluator,
        data_source_name="crossing values",
        def_val="price_data",
        enable_static_value=False,
    )
    (
        values_to_cross_titles,
        selected_indicator_ids,
    ) = await activate_multiple_configurable_indicators(
        maker,
        evaluator,
        data_source_name="values to cross",
        def_val=["EMA"],
        indicator_group_id=2,
    )
    if len(values_to_cross_titles) > 1:
        crossing_options = ["crossing up", "crossing down"]
    else:
        crossing_options = ["crossing up", "crossing down", "crossing up and down"]
    crossing_direction = await user_input2(
        maker,
        evaluator,
        "crossing direction",
        "options",
        "crossing up",
        options=crossing_options,
    )
    crossing_delay = await user_input2(
        maker, evaluator, "crossing signal delay", "int", 0
    )
    max_crossing_lookback = await user_input2(
        maker,
        evaluator,
        "history length for maximum dump/pump (0 = disabled)",
        "int",
        0,
        0,
    )
    max_crossing = 0
    if int(max_crossing_lookback) != 0:
        max_crossing = await user_input2(
            maker,
            evaluator,
            "maximum % dump/pump before cross up/down (0 = disabled)",
            "float",
            0,
        )
    max_crossing_count = 50
    max_crossing = (
        None
        if int(max_crossing_lookback) == 0 or int(max_crossing) == 0
        else str(max_crossing) + "%"
    )
    max_crossing_count_lookback = await user_input2(
        maker,
        evaluator,
        "history length for nearby signals (0 = disabled)",
        "int",
        0,
        0,
    )
    if int(max_crossing_count_lookback) != 0:
        max_crossing_count = await user_input2(
            maker, evaluator, "maximum nearby signals", "int", 1, min_val=1
        )
        max_crossing_count = max_crossing_count if int(max_crossing_count) != 0 else 50

    max_crossing_count_lookback = (
        max_crossing_count_lookback if max_crossing_count_lookback != 0 else 1
    )

    (
        data_crossing_values,
        evaluator.chart_location,
        crossing_values_title,
    ) = await get_configurable_indicator(maker, evaluator)
    # evaluator.values, _, values_to_cross_title
    values_to_cross_indicators_data = await get_configurable_indicators(
        maker, evaluator, indicator_ids=selected_indicator_ids
    )
    all_values_to_cross = []
    indicator_titles: list = []
    for indicator_data, _, indicator_title in values_to_cross_indicators_data:
        all_values_to_cross.append(indicator_data)
        indicator_titles.append(indicator_title)
    evaluator.title = (
        f"{crossing_values_title} is {crossing_direction} {indicator_titles}"
    )
    await allow_enable_plot(maker, evaluator, f"Plot when {evaluator.title}")
    all_values_to_cross = cut_data_to_same_len(all_values_to_cross, get_list=True)
    stacked_values_to_cross = numpy.dstack(all_values_to_cross)

    if crossing_direction == "crossing up":
        evaluator.values = stacked_values_to_cross.max(axis=2)[0]
        evaluator.signals = await crossing_up_(
            maker=maker,
            values_to_cross=evaluator.values,
            crossing_values=data_crossing_values,
            delay=crossing_delay,
            max_cross_down=max_crossing,
            max_cross_down_lookback=max_crossing_lookback,
            max_history=not maker.live_recording_mode,
        )

    elif crossing_direction == "crossing down":
        evaluator.values = stacked_values_to_cross.min(axis=2)[0]
        evaluator.signals = await crossing_down_(
            maker=maker,
            values_to_cross=evaluator.values,
            crossing_values=data_crossing_values,
            delay=crossing_delay,
            max_cross_up=max_crossing,
            max_cross_up_lookback=max_crossing_lookback,
            max_history=not maker.live_recording_mode,
        )
    else:  # crossing up or down
        evaluator.values = values_to_cross_indicators_data[0][0]
        evaluator.signals = await crossing_(
            maker=maker,
            values_to_cross=evaluator.values,
            crossing_values=data_crossing_values,
            delay=crossing_delay,
            max_cross=max_crossing,
            max_cross_lookback=max_crossing_lookback,
            max_history=not maker.live_recording_mode,
        )
    return await store_evaluator_data(maker, evaluator, allow_signal_extension=True)
