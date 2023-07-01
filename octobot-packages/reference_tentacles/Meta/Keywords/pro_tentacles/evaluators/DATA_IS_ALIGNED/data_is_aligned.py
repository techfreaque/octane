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


async def get_data_is_aligned(maker, evaluator):
    (
        values_to_cross_titles,
        selected_indicator_ids,
    ) = await activate_multiple_configurable_indicators(
        maker,
        evaluator,
        data_source_name="Indicator that need to be aligned",
        def_val=["EMA"],
        indicator_group_id=2,
        min_indicators=2,
    )
    signal_delay = await user_input2(maker, evaluator, "Signal delay", "int", 0)
    first_signal_only = await user_input2(
        maker, evaluator, "First signal only", "boolean", True
    )

    values_to_cross_indicators_data = await get_configurable_indicators(
        maker, evaluator, indicator_ids=selected_indicator_ids
    )
    indicators_values = []
    evaluator.title = ""
    # indicator_titles: list = []
    data_source_index = 0
    for (
        indicator_data,
        chart_location,
        indicator_title,
    ) in values_to_cross_indicators_data:
        data_source_index += 1
        evaluator.title += (
            f"{indicator_title}"
            if data_source_index == len(values_to_cross_indicators_data)
            else f"{indicator_title} is above "
        )
        evaluator.chart_location = chart_location
        indicators_values.append(indicator_data)
        # indicator_titles.append(indicator_title)

    await allow_enable_plot(maker, evaluator, f"Plot when {evaluator.title}")
    # indicators_values = [
    #     [1, 4, 2, 6],
    #     [1, 3, 5, 6],
    #     [
    #         1,
    #         2,
    #         4,
    #         6,
    #         8,
    #     ],
    # ]

    min_len = min(len(indicator_values) for indicator_values in indicators_values)
    indicator_values = [
        indicator_values[-min_len:] for indicator_values in indicators_values
    ]
    # aligned_data = [
    #     all(
    #         array[indicator_index][candle_index]
    #         <= array[indicator_index + 1][candle_index]
    #         for indicator_index in range(len(array) - 1)
    #     )
    #     for candle_index in range(min_len)
    # ]

    # # truncate all arrays to the minimum length
    # array = [indicator_values[:min_len] for indicator_values in indicators_values]

    # # create a new array of booleans
    aligned_data = []
    aligned_data_unfiltered = [False]
    for candle_index in range(min_len):
        is_aligned = True
        for indicator_index in range(len(indicator_values) - 1):
            is_aligned = (
                is_aligned
                and indicator_values[indicator_index][candle_index]
                >= indicator_values[indicator_index + 1][candle_index]
            )
            if not is_aligned:
                break
        aligned_data.append(
            is_aligned
            and (
                (
                    all(aligned_data_unfiltered[-signal_delay:])
                    if len(aligned_data_unfiltered) > signal_delay
                    else False
                )
                if signal_delay
                else True
            )
            and (
                not first_signal_only
                or (
                    not aligned_data_unfiltered[-1 - (signal_delay)]
                    if len(aligned_data_unfiltered) > signal_delay
                    else True
                )
            )
        )
        aligned_data_unfiltered.append(is_aligned)

    evaluator.values = indicators_values[0]
    evaluator.signals = aligned_data
    # indicators_values = cut_data_to_same_len(indicators_values, get_list=True)
    # stacked_values_to_cross = numpy.dstack(indicators_values)

    # if crossing_direction == "crossing up":
    #     evaluator.values = stacked_values_to_cross.max(axis=2)[0]
    #     evaluator.signals = await crossing_up_(
    #         maker=maker,
    #         values_to_cross=evaluator.values,
    #         crossing_values=data_crossing_values,
    #         delay=crossing_delay,
    #         max_cross_down=max_crossing,
    #         max_cross_down_lookback=max_crossing_lookback,
    #         max_history=not maker.live_recording_mode,
    #     )

    # elif crossing_direction == "crossing down":
    #     evaluator.values = stacked_values_to_cross.min(axis=2)[0]
    #     evaluator.signals = await crossing_down_(
    #         maker=maker,
    #         values_to_cross=evaluator.values,
    #         crossing_values=data_crossing_values,
    #         delay=crossing_delay,
    #         max_cross_up=max_crossing,
    #         max_cross_up_lookback=max_crossing_lookback,
    #         max_history=not maker.live_recording_mode,
    #     )
    # else:  # crossing up or down
    #     evaluator.values = values_to_cross_indicators_data[0][0]
    #     evaluator.signals = await crossing_(
    #         maker=maker,
    #         values_to_cross=evaluator.values,
    #         crossing_values=data_crossing_values,
    #         delay=crossing_delay,
    #         max_cross=max_crossing,
    #         max_cross_lookback=max_crossing_lookback,
    #         max_history=not maker.live_recording_mode,
    #     )
    return await store_evaluator_data(maker, evaluator, allow_signal_extension=True)
