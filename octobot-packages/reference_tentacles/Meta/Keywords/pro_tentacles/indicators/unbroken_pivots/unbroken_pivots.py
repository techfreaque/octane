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

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)
from tentacles.Meta.Keywords.pro_tentacles.indicators.indicator_handling import (
    activate_configurable_indicator,
    get_configurable_indicator,
)
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.pivots_lib.multi_pivots_lib as multi_pivots_lib
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_indicator_data,
    allow_enable_plot,
    store_and_plot_indicator,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)


async def get_unbroken_pivots(maker, indicator, evaluator):
    await allow_enable_plot(maker, indicator, "Plot unbroken pivots")
    confirmation_time = int(
        await user_input2(
            maker,
            indicator,
            "Bars it takes to confirm a pivot break",
            "int",
            def_val=1,
            min_val=0,
        )
    )

    min_pivot_age = int(
        await user_input2(
            maker, indicator, "minimum pivot age", "int", def_val=0, min_val=0
        )
    )
    indicator.pivot_lookback = (
        evaluator.pivot_lookback if hasattr(evaluator, "pivot_lookback") else None
    ) or await user_input2(maker, indicator, f"pivot lookback length", "int", 2, 1)
    unbroken_pivots_per_side = int(
        await user_input2(
            maker, indicator, "Amount of unbroken Pivots per side", "int", def_val=2
        )
    )
    max_pivot_lookback = int(
        await user_input2(
            maker,
            indicator,
            "amounts of bars to go back and check for Pivots",
            "int",
            def_val=800,
        )
    )
    _ = await activate_configurable_indicator(
        maker,
        indicator,
        enable_force_def_val=True,
        data_source_name="Pivots source",
        def_val="pivots",
    )
    (
        pivot_data,
        chart_location,
        both_title,
    ) = await get_configurable_indicator(maker, indicator)

    data: dict = {}
    if pivot_highs_data := pivot_data.get(PriceDataSources.HIGH.value):
        pivot_highs = pivot_highs_data["pivots"]
        pivot_values = pivot_highs_data["pivots_val"]
        high_indicator_values = pivot_highs_data["values"]
        pivot_highs_title = pivot_highs_data["title"]
        (
            unbroken_pivot_highs_data,
            unbroken_pivot_high_price_data,
        ) = multi_pivots_lib.unbroken_pivot_highs(
            pivot_highs,
            high_indicator_values,
            pivots_len=unbroken_pivots_per_side,
            confirmation=confirmation_time,
            min_pivot_age=min_pivot_age,
            max_pivot_lookback=max_pivot_lookback,
            pivot_lookback=indicator.pivot_lookback,
        )
        title = f"Unbroken {pivot_highs_title} highs ({confirmation_time}-{min_pivot_age}_{unbroken_pivots_per_side})"
        data[PriceDataSources.HIGH.value] = {
            "title": title,
            "pivots": unbroken_pivot_high_price_data,
            "chart_location": chart_location,
            "values": high_indicator_values,
        }
        await store_and_plot_indicator(
            maker=maker,
            indicator=indicator,
            title=title,
            value_key=PriceDataSources.HIGH.value,
            main_data=unbroken_pivot_high_price_data,
            chart_location="main-chart",
            mode="markers",
            line_shape=None,
            enable_rounding=False,
        )

    if pivot_lows_data := pivot_data.get(PriceDataSources.LOW.value):
        pivot_lows = pivot_lows_data["pivots"]
        pivot_values = pivot_lows_data["pivots_val"]
        low_indicator_values = pivot_lows_data["values"]
        pivot_lows_title = pivot_lows_data["title"]

        (
            unbroken_pivot_lows_data,
            unbroken_pivot_low_price_data,
        ) = multi_pivots_lib.unbroken_pivot_lows(
            pivot_lows,
            low_indicator_values,
            pivots_len=unbroken_pivots_per_side,
            confirmation=confirmation_time,
            min_pivot_age=min_pivot_age,
            max_pivot_lookback=max_pivot_lookback,
            pivot_lookback=indicator.pivot_lookback,
        )
        title = f"Unbroken {pivot_lows_title} lows ({confirmation_time}-{min_pivot_age}_{unbroken_pivots_per_side})"
        data[PriceDataSources.LOW.value] = {
            "title": title,
            "pivots": unbroken_pivot_low_price_data,
            "chart_location": chart_location,
            "values": low_indicator_values,
        }
        await store_and_plot_indicator(
            maker=maker,
            indicator=indicator,
            title=title,
            value_key=PriceDataSources.LOW.value,
            main_data=unbroken_pivot_low_price_data,
            chart_location="main-chart",
            mode="markers",
            line_shape=None,
            enable_rounding=False,
        )

    data_sources = {
        "v": {
            "data": data,
            "title": "Unbroken " + both_title,
            "chart_location": chart_location,
        }
    }
    return await store_indicator_data(
        maker, indicator, data_sources, force_plot_disable=True
    )
