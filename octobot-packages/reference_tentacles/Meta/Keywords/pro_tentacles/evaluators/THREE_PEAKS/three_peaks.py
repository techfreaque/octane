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
    is_above,
)


async def get_three_peaks(maker, evaluator):
    await activate_configurable_indicator(
        maker,
        evaluator,
        def_val="pivots",
        data_source_name="three peaks data source",
        enable_force_def_val=True,
    )

    confirmation_time = await user_input2(
        maker, evaluator, "Bars it takes to confirm a pivot break", "int", 1, 0
    )
    max_pivot_1_age = await user_input2(
        maker, evaluator, "maximum pivot 1 age in bars", "int", 80, 0
    )

    min_pivot_2_age = await user_input2(
        maker, evaluator, "minimum pivot 2 age in bars", "int", 5, 0
    )
    # max_pivot_2_age = await user_input(ctx, "maximum pivot 2 age in bars", "int", 40, 0)

    min_bars_distance_pivot_1_and_2 = await user_input2(
        maker, evaluator, "min distance between pivot 1 and 2 in bars", "int", 5, 0
    )
    max_p_distance_pivot_1_and_2 = await user_input2(
        maker,
        evaluator,
        "max % distance between pivot 1 and lowest " "price after",
        "float",
        2,
        0,
    )

    # max_nearby_signals = await user_input(ctx, "maximum nearby signals", "int", 1, 0)
    # max_nearby_signals_lb = await user_input(ctx, "maximum nearby signals look back period", "int", 8, 0)

    activate_long_three_peaks = await user_input2(
        maker,
        evaluator,
        "Activate long Three Peaks",
        def_val=True,
        input_type="boolean",
    )
    activate_short_three_peaks = await user_input2(
        maker,
        evaluator,
        "Activate short Three Peaks",
        def_val=True,
        input_type="boolean",
    )

    await allow_enable_plot(maker, evaluator, f"Plot three peaks")

    (
        evaluator.values,
        evaluator.chart_location,
        indicator_title,
    ) = await get_configurable_indicator(maker, evaluator)

    evaluator.signals = []
    if activate_long_three_peaks:
        p_length = len(pivot_low_data)
        pivot_2_price_history = []
        pivot_1_price_history = []
        three_p_price_history = []
        is_three_p_history = []

        for jj in range(max_pivot_1_age, p_length):
            pivot_2_prices = []
            pivot_1_prices = []
            three_p_prices = []
            long_three_peaks = False

            # check if pivot 2 found
            for i in range(
                max(min_pivot_2_age, confirmation_time) + 1, max_pivot_1_age
            ):
                if pivot_low_data[jj - i]:
                    pivot_2_price = pivot_low_price_data[jj - i]
                    # max dip down
                    if (pivot_2_price * (1 - max_p_distance_pivot_1_and_2 / 100)) < min(
                        pivot_low_price_data[jj - i : jj + 1]
                    ):
                        # was unbroken
                        try:
                            if pivot_2_price <= min(
                                pivot_low_price_data[
                                    jj - i : jj - confirmation_time + 1
                                ]
                            ):
                                pivot_2_prices.append(pivot_2_price)

                                # check if pivot 1 found
                                for j in range(
                                    i + min_bars_distance_pivot_1_and_2, max_pivot_1_age
                                ):
                                    pivot_is_unbroken = (
                                        pivot_2_price < pivot_low_price_data[jj - j]
                                    )
                                    if pivot_low_data[jj - j] and pivot_is_unbroken:
                                        if pivot_2_price < pivot_low_price_data[jj - j]:
                                            pivot_1_price = pivot_low_price_data[jj - j]

                                            # max distance
                                            try:
                                                if (
                                                    pivot_1_price
                                                    * (
                                                        1
                                                        - max_p_distance_pivot_1_and_2
                                                        * 2
                                                        / 100
                                                    )
                                                ) < min(
                                                    pivot_low_price_data[
                                                        jj - j : jj + 1
                                                    ]
                                                ):
                                                    pivot_1_prices.append(pivot_1_price)

                                                    # check if pivot 2 got sfp'ed
                                                    long_three_peaks = (
                                                        closes[jj]
                                                        > pivot_2_price
                                                        > min(lows[jj - 1 : jj + 1])
                                                    )
                                                    if long_three_peaks:
                                                        long_three_peaks_price = (
                                                            pivot_2_price
                                                        )
                                                        three_p_prices.append(
                                                            long_three_peaks_price
                                                        )
                                            except:
                                                test = 0
                        except:
                            test = 0
            if three_p_prices:
                long_three_peaks = True
            pivot_2_price_history.append(pivot_2_prices)
            pivot_1_price_history.append(pivot_1_prices)
            three_p_price_history.append(three_p_prices)
            is_three_p_history.append(long_three_peaks)
        _cache = {}
        if plot_peak_1_and_2:
            _cache = {
                pivot_low_1_key: pivot_1_price_history,
                pivot_low_2_key: pivot_2_price_history,
            }
        if plot_three_peaks:
            if _cache:
                _cache = {
                    pivot_low_1_key: pivot_1_price_history,
                    pivot_low_2_key: pivot_2_price_history,
                    long_three_peaks_key: three_p_price_history,
                }
            else:
                _cache = {long_three_peaks_key: three_p_price_history}

    evaluator.title = f"three peaks ({indicator_title})"

    return await store_evaluator_data(maker, evaluator)
