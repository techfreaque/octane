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

import tulipy as tulipy
import numpy as numpy
import octobot_trading.enums as trading_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
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


async def get_fib_line(maker, indicator, evaluator):
    fib_line_level = await user_input2(
        maker, indicator, "Fib line level", "float", 0.618
    )
    fib_line_ema_length = await user_input2(
        maker, indicator, "Fib line ema length", "float", 50, min_val=1
    )
    enable_0_line = await user_input2(
        maker,
        indicator,
        "Enable fib 0 line",
        "boolean",
        True,
    )
    enable_1_line = await user_input2(
        maker,
        indicator,
        "Enable fib 1 line",
        "boolean",
        True,
    )
    enable_both_line = await user_input2(
        maker,
        indicator,
        "Enable combined fib line",
        "boolean",
        True,
    )
    enable_ema_line = await user_input2(
        maker,
        indicator,
        "Enable ema fib line",
        "boolean",
        True,
    )
    enable_short_line = await user_input2(
        maker,
        indicator,
        "Enable short fib line",
        "boolean",
        True,
    )
    enable_long_line = await user_input2(
        maker,
        indicator,
        "Enable long fib line",
        "boolean",
        True,
    )
    await allow_enable_plot(maker, indicator, "Plot Fib line")

    _ = await activate_configurable_indicator(
        maker,
        indicator,
        enable_force_def_val=True,
        data_source_name="Unbroken pivots source",
        def_val="unbroken_pivots",
    )
    (
        pivot_data,
        chart_location,
        pivots_title,
    ) = await get_configurable_indicator(maker, indicator)

    fib_line_values = []
    fib_long_line_values = []
    fib_short_line_values = []
    fib_0line_values = []
    fib_1line_values = []
    fib_ema = []
    if (pivot_highs_data := pivot_data.get(PriceDataSources.HIGH.value)) and (
        pivot_lows_data := pivot_data.get(PriceDataSources.LOW.value)
    ):
        pivot_highs, pivot_lows, highs, lows = cut_data_to_same_len(
            (
                pivot_highs_data["pivots"],
                pivot_lows_data["pivots"],
                pivot_highs_data["values"],
                pivot_lows_data["values"],
            )
        )
        for index, pivot_high in enumerate(pivot_highs):
            lowest_low = None
            highest_high = None
            try:
                lowest_low = min(pivot_lows[index])
                highest_high = max(pivot_high)
            except ValueError:
                start_index = index - 50 if index - 50 > 0 else 0
                if not lowest_low:
                    lowest_low = min(lows[start_index : index + 1])
                if not highest_high:
                    highest_high = max(highs[start_index : index + 1])

            fib_side = detect_fib_side(highest_high, highs, lowest_low, lows, index)
            if fib_side == trading_enums.PositionSide.LONG:
                current_fib_line = (
                    (highest_high - lowest_low) * (1 - fib_line_level)
                ) + lowest_low
                current_long_fib_line = current_fib_line
                current_short_fib_line = numpy.nan
            else:
                current_fib_line = (
                    (highest_high - lowest_low) * (fib_line_level)
                ) + lowest_low
                current_long_fib_line = numpy.nan
                current_short_fib_line = current_fib_line

            fib_long_line_values.append(current_long_fib_line)
            fib_short_line_values.append(current_short_fib_line)
            fib_line_values.append(current_fib_line)
            fib_0line_values.append(lowest_low)
            fib_1line_values.append(highest_high)

        if enable_ema_line and len(fib_line_values):
            fib_line_values = numpy.asarray(fib_line_values)
            fib_ema = tulipy.ema(fib_line_values, fib_line_ema_length)

    data_source = {}

    # if enable_both_line:
    data_source["v"] = {
        "title": f"Fib line {pivots_title}",
        "data": fib_line_values,
        "chart_location": chart_location,
    }
    if enable_ema_line:
        data_source["e"] = {
            "title": f"Fib ema line {pivots_title}",
            "data": fib_ema,
            "chart_location": chart_location,
        }
    if enable_0_line:
        data_source["0"] = {
            "title": f"Fib 0 line {pivots_title}",
            "data": fib_0line_values,
            "chart_location": chart_location,
        }
    if enable_1_line:
        data_source["1"] = {
            "title": f"Fib 1 line {pivots_title}",
            "data": fib_1line_values,
            "chart_location": chart_location,
        }
    if enable_long_line:
        data_source["l"] = {
            "title": f"Fib long line {pivots_title}",
            "data": fib_long_line_values,
            "chart_location": chart_location,
            "mode": "markers",
            "line_shape": None,
        }
    if enable_short_line:
        data_source["s"] = {
            "title": f"Fib short line {pivots_title}",
            "data": fib_short_line_values,
            "chart_location": chart_location,
            "mode": "markers",
            "line_shape": None,
        }

    return await store_indicator_data(
        maker,
        indicator,
        data_source,
        enable_rounding=False,
        filter_nan_for_plots=True,
    )


def detect_fib_side(
    highest_high, highs, lowest_low, lows, index
) -> trading_enums.PositionSide:
    for sub_index in range(0, index):
        if highest_high == highs[index - sub_index]:
            return trading_enums.PositionSide.LONG
        if lowest_low == lows[index - sub_index]:
            return trading_enums.PositionSide.SHORT
