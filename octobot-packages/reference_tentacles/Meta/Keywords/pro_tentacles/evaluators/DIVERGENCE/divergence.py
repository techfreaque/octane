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
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.divergences.divergence import (
    divergence_,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_evaluator_data,
    allow_enable_plot,
)
from tentacles.Meta.Keywords.pro_tentacles.indicators.indicator_handling import (
    get_configurable_indicator,
    activate_configurable_indicator,
)


async def get_divergence(maker, evaluator):
    base_title = await activate_configurable_indicator(
        maker,
        evaluator,
        data_source_name="divergence base",
        def_val="pivots",
        enable_force_def_val=True,
    )
    other_title = await activate_configurable_indicator(
        maker,
        evaluator,
        data_source_name="divergence other",
        def_val="pivots",
        indicator_id=2,
        enable_force_def_val=True,
    )
    confirmation_time = await user_input2(
        maker, evaluator, "Bars it takes to confirm divergence", "int", 0, 0
    )
    time_for_ll = await user_input2(
        maker, evaluator, "bars until a lower low is invalid", "int", 1, 1
    )
    max_pivot_age = await user_input2(
        maker, evaluator, "maximum pivots age in Bars", "int", 800, 2
    )
    min_pivot_age = await user_input2(
        maker, evaluator, "minimum pivots age in Bars", "int", 0, 0
    )
    pivot_match_range = await user_input2(
        maker, evaluator, "range to match pivots", "int", 10, 1
    )
    pivot_other_loockback_offset = await user_input2(
        maker, evaluator, "pivot lookback offset other data", "int", -1, max_val=0
    )
    pivot_lookback = await user_input2(
        maker, evaluator, "pivot lookback length", "int", 20, 3
    )
    first_signal_only = await user_input2(
        maker, evaluator, "flash signal only on the first candle", "boolean", False
    )
    wait_for_a_reversal = await user_input2(
        maker, evaluator, "wait for a reversal above base pivot", "boolean", True
    )
    # ll_only = await user_input(maker.ctx, f"{evaluator.config_path} trigger when lower low found on base data",
    #                            "boolean", True)
    await allow_enable_plot(
        maker, evaluator, f"plot divergence between {base_title} and {other_title}"
    )
    evaluator.pivot_lookback = pivot_lookback
    base_data, evaluator.chart_location, base_title = await get_configurable_indicator(
        maker, evaluator
    )

    evaluator.pivot_lookback = pivot_lookback + pivot_other_loockback_offset

    (
        other_data,
        evaluator.second_chart_location,
        other_title,
    ) = await get_configurable_indicator(maker, evaluator, indicator_id=2)
    (
        div_data,
        div_other_values,
        div_base_values,
        cleaned_div_data,
        cleaned_div_other_values,
        cleaned_div_base_values,
    ) = divergence_(
        base_data=base_data[PriceDataSources.LOW.value]["pivots"],
        other_data=other_data[PriceDataSources.LOW.value]["pivots"],
        base_values=base_data[PriceDataSources.LOW.value]["pivots_val"],
        other_values=other_data[PriceDataSources.LOW.value]["pivots_val"],
        base_source_data=base_data[PriceDataSources.LOW.value]["values"],
        other_source_data=other_data[PriceDataSources.LOW.value]["values"],
        max_pivot_age=max_pivot_age,
        min_pivot_age=min_pivot_age,
        time_for_ll=time_for_ll,
        confirmation_time=confirmation_time,
        pivot_lookback_base=pivot_lookback,
        pivot_lookback_other=pivot_lookback + pivot_other_loockback_offset,
        pivot_match_range=pivot_match_range,
        wait_for_a_reversal=wait_for_a_reversal,
        ll_only=False,
    )
    if first_signal_only:
        evaluator.signals = cleaned_div_data
        evaluator.second_values = cleaned_div_other_values
        evaluator.values = cleaned_div_base_values
    else:
        evaluator.signals = div_data
        evaluator.second_values = div_other_values
        evaluator.values = div_base_values
    evaluator.title = f"divergence (ll on: {base_title} hl on; {other_title})(base)"
    evaluator.second_title = (
        f"divergence (ll on: {base_title} hl on; {other_title})(other)"
    )
    return await store_evaluator_data(maker, evaluator)
