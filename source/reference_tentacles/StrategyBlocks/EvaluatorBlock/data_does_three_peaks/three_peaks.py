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

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_evaluator_block as abstract_evaluator_block

LONG_SIGNAL: str = "Long"
SHORT_SIGNAL: str = "Short"


class DataDoesThreePeaksEvaluator(abstract_evaluator_block.EvaluatorBlock):
    NAME = "data_does_three_peaks"
    TITLE = "Data peaks three times"
    TITLE_SHORT = "Data peaks three times"
    DESCRIPTION = (
        "Data does three peaks allows you to detect "
        "when a data source is peaking the third time or more. "
        "Connect the lows and highs indicator to get started."
    )
    break_confirmation_time: int
    confirmation_time: int
    max_pivot_1_age: int
    min_pivot_2_age: int
    min_bars_distance_pivot_1_and_2: int
    max_p_distance_pivot_1_and_2: float
    activate_long_three_peaks: bool
    activate_short_three_peaks: bool
    plot_peak_1_and_2: bool

    signal_side: str

    def init_block_settings(self) -> None:
        self.break_confirmation_time = self.user_input(
            "Bars it takes to confirm a pivot break", "int", 1, 0
        )
        self.confirmation_time = self.user_input(
            "Bars it takes to confirm a pivot 2 cross up", "int", 1, 0
        )
        self.max_pivot_1_age = self.user_input(
            "Maximum pivot 1 age in bars", "int", 80, 0
        )
        self.min_pivot_2_age = self.user_input(
            "Minimum pivot 2 age in bars", "int", 5, 0
        )
        # max_pivot_2_age = self.user_input("maximum pivot 2 age in bars", "int", 40, 0)
        self.min_bars_distance_pivot_1_and_2 = self.user_input(
            "Min distance between pivot 1 and 2 in bars", "int", 5, 0
        )
        self.max_p_distance_pivot_1_and_2 = self.user_input(
            "Max % distance between pivot 1 and lowest " "price after",
            "float",
            2,
            0,
        )
        # max_nearby_signals = self.user_input("maximum nearby signals", "int", 1, 0)
        # max_nearby_signals_lb = self.user_input("maximum nearby signals look back period", "int", 8, 0)
        self.signal_side = self.user_input(
            "Signal side",
            def_val=LONG_SIGNAL,
            input_type="options",
            options=[LONG_SIGNAL, SHORT_SIGNAL],
        )
        self.activate_single_input_data_node(
            def_val="highs_and_lows",
            data_source_name=f"Pivot {'Lows' if self.signal_side == LONG_SIGNAL else 'Highs'}",
            enable_force_def_val=True,
        )
        self.register_evaluator_data_output(
            title=f"Three Peeks {self.signal_side} Signals",
            plot_switch_text=f"Plot three peaks {self.signal_side.lower()} signals",
            plot_color_switch_title=f"{self.signal_side} signals plot color",
            default_plot_color=block_factory_enums.Colors.CYAN,
        )
        self.plot_peak_1_and_2 = self.user_input(
            "Plot peak 1 and 2",
            def_val=True,
            input_type="boolean",
        )

    async def execute_block(
        self,
    ) -> None:
        (
            cutted_data_source_values,
            data_source_conditions,
            data_source_values,
            chart_location,
            indicator_title,
        ) = await self.get_input_node_data(get_additional_node_data=True)
        (
            _cutted_data_source_values,
            cutted_data_source_conditions,
            _data_source_values,
        ) = cut_data_to_same_len(
            (cutted_data_source_values, data_source_conditions, data_source_values)
        )
        data_length = len(cutted_data_source_conditions)
        pivot_2_price_history = []
        pivot_1_price_history = []
        three_p_price_history = []
        is_three_p_history = []
        for candle_id in range(200, data_length):
            pivot_2_prices = []
            pivot_1_prices = []
            three_p_prices = []
            find_pivot_2(
                signal_side=self.signal_side,
                candle_id=candle_id,
                max_p_distance_pivot_1_and_2=self.max_p_distance_pivot_1_and_2,
                cutted_data_source_values=_cutted_data_source_values,
                confirmation_time=self.confirmation_time,
                break_confirmation_time=self.break_confirmation_time,
                min_pivot_2_age=self.min_pivot_2_age,
                max_pivot_1_age=self.max_pivot_1_age,
                min_bars_distance_pivot_1_and_2=self.min_bars_distance_pivot_1_and_2,
                data_source_conditions=cutted_data_source_conditions,
                data_source_values=_data_source_values,
                pivot_2_prices=pivot_2_prices,
                pivot_1_prices=pivot_1_prices,
                three_p_prices=three_p_prices,
            )
            long_three_peaks = False
            if three_p_prices:
                long_three_peaks = True
            pivot_2_price_history.append(pivot_2_prices)
            pivot_1_price_history.append(pivot_1_prices)
            three_p_price_history.append(three_p_prices)
            is_three_p_history.append(long_three_peaks)
        if self.plot_peak_1_and_2:
            await self.plot_and_store_indicator_data(
                title=f"Peak 1 {self.signal_side} ({indicator_title})",
                data=pivot_1_price_history,
                mode="markers",
                color=block_factory_enums.Colors.BLUE.value,
                chart_location=chart_location,
                size=1,
            )
            await self.plot_and_store_indicator_data(
                title=f"Peak 2 {self.signal_side} ({indicator_title})",
                data=pivot_2_price_history,
                mode="markers",
                color=block_factory_enums.Colors.RED.value,
                chart_location=chart_location,
                size=1,
            )
        await self.store_evaluator_signals(
            title=f"Three peaks {self.signal_side} ({indicator_title})",
            signals=is_three_p_history,
            signal_values=three_p_price_history,
            chart_location=chart_location,
        )


def find_pivot_2(
    signal_side: str,
    candle_id: int,
    max_p_distance_pivot_1_and_2: float,
    cutted_data_source_values,
    break_confirmation_time: int,
    confirmation_time: int,
    min_pivot_2_age: int,
    max_pivot_1_age: int,
    min_bars_distance_pivot_1_and_2: int,
    data_source_conditions,
    data_source_values,
    pivot_2_prices: list,
    pivot_1_prices: list,
    three_p_prices: list,
):
    for pivot_2_candles_back_id in range(
        min_pivot_2_age + 1,
        max_pivot_1_age,
    ):
        # find pivot 2 first (the right one on the chart)
        pivot_2_candle_id: int = candle_id - pivot_2_candles_back_id
        if pivot_2_candle_id > 0:
            if data_source_conditions[pivot_2_candle_id]:
                pivot_2_price: float = cutted_data_source_values[pivot_2_candle_id]
                if not_dipped_down_more_than_max_percent(
                    signal_side=signal_side,
                    pivot_2_candle_id=pivot_2_candle_id,
                    candle_id=candle_id,
                    pivot_2_price=pivot_2_price,
                    max_p_distance_pivot_1_and_2=max_p_distance_pivot_1_and_2,
                    data_source_values=data_source_values,
                ):
                    if is_pivot_still_unbroken(
                        signal_side=signal_side,
                        pivot_2_price=pivot_2_price,
                        data_source_values=data_source_values,
                        pivot_2_candle_id=pivot_2_candle_id,
                        candle_id=candle_id,
                        break_confirmation_time=break_confirmation_time,
                    ):
                        find_pivot_one(
                            signal_side=signal_side,
                            pivot_2_candles_back_id=pivot_2_candles_back_id,
                            candle_id=candle_id,
                            confirmation_time=confirmation_time,
                            min_bars_distance_pivot_1_and_2=min_bars_distance_pivot_1_and_2,
                            max_pivot_1_age=max_pivot_1_age,
                            max_p_distance_pivot_1_and_2=max_p_distance_pivot_1_and_2,
                            data_source_conditions=data_source_conditions,
                            data_source_values=data_source_values,
                            cutted_data_source_values=cutted_data_source_values,
                            pivot_1_prices=pivot_1_prices,
                            pivot_2_price=pivot_2_price,
                            pivot_2_prices=pivot_2_prices,
                            three_p_prices=three_p_prices,
                        )


def find_pivot_one(
    signal_side: str,
    pivot_2_candles_back_id: int,
    candle_id: int,
    min_bars_distance_pivot_1_and_2: int,
    max_pivot_1_age: int,
    confirmation_time: int,
    max_p_distance_pivot_1_and_2: float,
    data_source_conditions,
    data_source_values,
    cutted_data_source_values,
    pivot_2_prices: list,
    pivot_1_prices: list,
    pivot_2_price: float,
    three_p_prices: list,
):
    for pivot_1_candles_back_id in range(
        pivot_2_candles_back_id + min_bars_distance_pivot_1_and_2,
        max_pivot_1_age,
    ):
        pivot_1_candle_id = candle_id - pivot_1_candles_back_id
        if pivot_1_candle_id > 0:
            if data_source_conditions[
                pivot_1_candle_id
            ] and check_if_pivot_1_is_unbroken(
                signal_side, pivot_2_price, cutted_data_source_values, pivot_1_candle_id
            ):
                pivot_1_price = cutted_data_source_values[pivot_1_candle_id]
                if check_if_pivots_are_close_enough_in_percent(
                    signal_side=signal_side,
                    candle_id=candle_id,
                    pivot_1_candle_id=pivot_1_candle_id,
                    pivot_1_price=pivot_1_price,
                    max_p_distance_pivot_1_and_2=max_p_distance_pivot_1_and_2,
                    cutted_data_source_values=cutted_data_source_values,
                ):
                    pivot_1_prices.append(pivot_1_price)
                    pivot_2_prices.append(pivot_2_price)
                    if check_if_pivot_2_got_sfp(
                        signal_side=signal_side,
                        data_source_values=data_source_values,
                        pivot_2_price=pivot_2_price,
                        candle_id=candle_id,
                        confirmation_time=confirmation_time,
                    ):
                        three_p_prices.append(pivot_2_price)


def check_if_pivots_are_close_enough_in_percent(
    signal_side: str,
    candle_id: int,
    pivot_1_candle_id: int,
    pivot_1_price: float,
    max_p_distance_pivot_1_and_2: float,
    cutted_data_source_values,
) -> bool:
    if signal_side == LONG_SIGNAL:
        return (pivot_1_price * (1 - max_p_distance_pivot_1_and_2 * 2 / 100)) < min(
            cutted_data_source_values[pivot_1_candle_id : candle_id + 1]
        )
    return (pivot_1_price * (1 + max_p_distance_pivot_1_and_2 * 2 / 100)) > max(
        cutted_data_source_values[pivot_1_candle_id : candle_id + 1]
    )


def check_if_pivot_1_is_unbroken(
    signal_side: str,
    pivot_2_price: float,
    cutted_data_source_values,
    pivot_1_candle_id: int,
):
    if signal_side == LONG_SIGNAL:
        return pivot_2_price < cutted_data_source_values[pivot_1_candle_id]
    return pivot_2_price > cutted_data_source_values[pivot_1_candle_id]


def check_if_pivot_2_got_sfp(
    signal_side: str,
    data_source_values,
    pivot_2_price: float,
    candle_id: int,
    confirmation_time: int,
) -> bool:
    if signal_side == LONG_SIGNAL:
        if data_source_values[
            candle_id - 1 - confirmation_time
        ] < pivot_2_price and pivot_2_price < min(
            data_source_values[candle_id - confirmation_time : candle_id + 1]
        ):
            return True
    else:
        if data_source_values[
            candle_id - 1 - confirmation_time
        ] > pivot_2_price and pivot_2_price > max(
            data_source_values[candle_id - confirmation_time : candle_id + 1]
        ):
            return True
    return False


def not_dipped_down_more_than_max_percent(
    signal_side: str,
    pivot_2_candle_id: int,
    candle_id: int,
    max_p_distance_pivot_1_and_2: float,
    pivot_2_price: float,
    data_source_values,
) -> bool:
    if signal_side == LONG_SIGNAL:
        return (pivot_2_price * (1 - max_p_distance_pivot_1_and_2 / 100)) < min(
            data_source_values[pivot_2_candle_id : candle_id + 1]
        )
    return (pivot_2_price * (1 + max_p_distance_pivot_1_and_2 / 100)) > max(
        data_source_values[pivot_2_candle_id : candle_id + 1]
    )


def is_pivot_still_unbroken(
    signal_side: str,
    pivot_2_price: float,
    data_source_values,
    pivot_2_candle_id: int,
    candle_id: int,
    break_confirmation_time: int,
) -> bool:
    ending_index = candle_id - break_confirmation_time + 1
    if ending_index - 1 < pivot_2_candle_id:
        # pivot got just detected
        return True
    if signal_side == LONG_SIGNAL:
        return pivot_2_price <= min(data_source_values[pivot_2_candle_id:ending_index])
    return pivot_2_price >= max(data_source_values[pivot_2_candle_id:ending_index])
