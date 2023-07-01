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
import tentacles.Meta.Keywords.pro_tentacles.indicators.indicator_handling as indicator_handling
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.pivots_lib.multi_pivots_lib as multi_pivots_lib
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting as matrix_plotting
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 as user_inputs2


async def get_pivots(maker, indicator, evaluator):
    await indicator_handling.activate_configurable_indicator(
        maker,
        indicator,
        def_val="price_data",
        data_source_name="data source for pivots highs",
    )
    await indicator_handling.activate_configurable_indicator(
        maker,
        indicator,
        def_val="price_data",
        data_source_name="data source for pivot lows",
        indicator_id=2,
    )
    pivot_lookback = (
        evaluator.pivot_lookback if hasattr(evaluator, "pivot_lookback") else None
    ) or await user_inputs2.user_input2(
        maker, indicator, "pivot lookback length", "int", 2, 1
    )

    pivot_low_active = await user_inputs2.user_input2(
        maker,
        indicator,
        "activate pivot lows",
        def_val=True,
        input_type="boolean",
        show_in_summary=False,
    )
    pivot_high_active = await user_inputs2.user_input2(
        maker,
        indicator,
        "activate pivot highs",
        def_val=True,
        input_type="boolean",
        show_in_summary=False,
    )
    await matrix_plotting.allow_enable_plot(maker, indicator, "plot Pivots")

    data = {
        "v": {
            "data": {},
        }
    }

    if pivot_low_active:
        (
            low_data_source_values,
            chart_location,
            low_data_source_title,
        ) = await indicator_handling.get_configurable_indicator(
            maker, indicator, indicator_id=2
        )
        pivot_low_data = multi_pivots_lib.pivot_lows(
            low_data_source_values, swing_history=pivot_lookback
        )
        await _get_pivots(
            maker,
            indicator,
            data,
            low_data_source_title,
            chart_location,
            low_data_source_values,
            pivot_low_data,
            pivot_lookback,
            key=PriceDataSources.LOW.value,
        )
    if pivot_high_active:
        (
            high_data_source_values,
            chart_location,
            high_data_source_title,
        ) = await indicator_handling.get_configurable_indicator(maker, indicator)
        pivot_low_data = multi_pivots_lib.pivot_highs(
            high_data_source_values, swing_history=pivot_lookback
        )
        await _get_pivots(
            maker,
            indicator,
            data,
            high_data_source_title,
            chart_location,
            high_data_source_values,
            pivot_low_data,
            pivot_lookback,
            key=PriceDataSources.HIGH.value,
        )
    data["v"]["chart_location"] = chart_location
    data["v"]["title"] = (
        f"{high_data_source_title} pivot highs / "
        f"{low_data_source_title} pivot lows (lb {pivot_lookback})"
    )
    return await matrix_plotting.store_indicator_data(
        maker, indicator, data, force_plot_disable=True
    )


async def _get_pivots(
    maker,
    indicator,
    data,
    data_source_title,
    chart_location,
    data_source_values,
    pivot_data,
    pivot_lookback,
    key=PriceDataSources.LOW.value,
):
    cache_key = key + "s"
    pivot_low_title = f"{data_source_title} pivot {key} (lb {pivot_lookback})"
    # format data and store
    cut_source_values = data_source_values[:-pivot_lookback]
    data["v"]["data"][key] = {
        "title": pivot_low_title,
        "pivots": pivot_data,
        "pivots_val": cut_source_values,
        "values": data_source_values,
        "chart-location": chart_location,
    }
    await matrix_plotting.plot_conditional(
        maker,
        indicator,
        cache_key,
        chart_location=chart_location,
        title=pivot_low_title,
        bool_list=pivot_data,
        values=cut_source_values,
    )
