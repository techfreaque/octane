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
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class FibLineIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "fib_line"
    TITLE = "Fib Line"
    TITLE_SHORT = "Fib Line"
    DESCRIPTION = "Fib Line"

    fib_line_level: float
    fib_line_ema_length: float
    enable_0_line: bool
    enable_1_line: bool
    enable_both_line: bool
    enable_ema_line: bool
    enable_short_line: bool
    enable_long_line: bool

    def init_block_settings(self) -> None:
        self.activate_single_input_data_node(
            enable_force_def_val=True,
            data_source_name="Pivot Lows",
            def_val="highs_and_lows",
        )
        self.activate_single_input_data_node(
            enable_force_def_val=True,
            data_source_name="Pivots Highs",
            def_val="highs_and_lows",
        )
        self.fib_line_level = self.user_input("Fib line level", "float", 0.618)

        self.enable_both_line = self.user_input(
            "Enable combined fib line",
            "boolean",
            True,
        )
        self.enable_0_line = self.user_input(
            "Enable fib 0 line",
            "boolean",
            False,
        )
        self.enable_1_line = self.user_input(
            "Enable fib 1 line",
            "boolean",
            False,
        )
        self.enable_ema_line = self.user_input(
            "Enable ema fib line",
            "boolean",
            False,
        )
        # self.enable_short_line = self.user_input(
        #     "Enable short fib line",
        #     "boolean",
        #     False,
        # )
        # self.enable_long_line = self.user_input(
        #     "Enable long fib line",
        #     "boolean",
        #     False,
        # )
        self.register_outputs()

    def register_outputs(self):
        if self.enable_both_line:
            self.register_indicator_data_output(
                title="Combined fib line",
                plot_switch_text="Plot Combined fib line",
                plot_color_switch_title="Combined fib line plot color",
                default_plot_color=block_factory_enums.Colors.ORANGE,
            )
        if self.enable_0_line:
            self.register_indicator_data_output(
                title="Fib 0 Line",
                plot_switch_text="Plot Fib 0 Line",
                plot_color_switch_title="Fib 0 Line plot color",
                default_plot_color=block_factory_enums.Colors.ORANGE,
            )
        if self.enable_1_line:
            self.register_indicator_data_output(
                title="Fib 1 Line",
                plot_switch_text="Plot Fib 1 Line",
                plot_color_switch_title="Fib 1 Line plot color",
                default_plot_color=block_factory_enums.Colors.ORANGE,
            )
        if self.enable_ema_line:
            self.fib_line_ema_length = self.user_input(
                "Fib line ema length", "float", 50, min_val=1
            )
            self.register_indicator_data_output(
                title="Ema Fib Line",
                plot_switch_text="Plot Ema Fib Line",
                plot_color_switch_title="Ema Fib Line plot color",
                default_plot_color=block_factory_enums.Colors.ORANGE,
            )
        # if self.enable_short_line:
        #     self.register_indicator_data_output(
        #         title="Short Fib Line",
        #         plot_switch_text="Plot Short Fib Line",
        #         plot_color_switch_title="Short Fib Line plot color",
        #         default_plot_color=block_factory_enums.Colors.ORANGE,
        #     )
        # if self.enable_long_line:
        #     self.register_indicator_data_output(
        #         title="Long Fib Line",
        #         plot_switch_text="Plot Long Fib Line",
        #         plot_color_switch_title="Long Fib Line plot color",
        #         default_plot_color=block_factory_enums.Colors.ORANGE,
        #     )
        self.user_select_data_source_time_frame()

    async def execute_block(self) -> None:
        (
            lows_data,
            lows_conditions,
            lows_additional_payload_data,
            chart_location,
            pivots_title_lows,
        ) = await self.get_input_node_data(get_additional_node_data=True)
        (
            highs_data,
            highs_conditions,
            highs_additional_payload_data,
            _,
            pivots_title_highs,
        ) = await self.get_input_node_data(get_additional_node_data=True)

        (
            fib_line_values,
            fib_long_line_values,
            fib_short_line_values,
            fib_0line_values,
            fib_1line_values,
            fib_ema,
        ) = self.calculate_fib_lines(
            highs_data,
            lows_data,
            highs_additional_payload_data,
            lows_additional_payload_data,
        )

        await self.store_fib_lines(
            fib_line_values,
            fib_ema,
            fib_0line_values,
            fib_1line_values,
            fib_long_line_values,
            fib_short_line_values,
            pivots_title_highs,
            pivots_title_lows,
            chart_location,
        )

    def calculate_fib_lines(
        self,
        highs_data,
        lows_data,
        highs_additional_payload_data,
        lows_additional_payload_data,
    ):
        fib_line_values = []
        fib_long_line_values = []
        fib_short_line_values = []
        fib_0line_values = []
        fib_1line_values = []
        fib_ema = []

        if highs_data is not None and lows_data is not None:
            pivot_highs, pivot_lows, highs, lows = cut_data_to_same_len(
                (
                    highs_data,
                    lows_data,
                    highs_additional_payload_data["high_data_source_values"],
                    lows_additional_payload_data["low_data_source_values"],
                )
            )
            for index, pivot_high in enumerate(pivot_highs):
                lowest_low, highest_high = self.get_high_low(
                    pivot_lows=pivot_lows,
                    pivot_highs=pivot_highs,
                    lows=lows,
                    highs=highs,
                    index=index,
                )
                fib_side = detect_fib_side(highest_high, highs, lowest_low, lows, index)
                (
                    current_fib_line,
                    current_long_fib_line,
                    current_short_fib_line,
                ) = self.get_fib_lines(fib_side, highest_high, lowest_low)

                fib_long_line_values.append(current_long_fib_line)
                fib_short_line_values.append(current_short_fib_line)
                fib_line_values.append(current_fib_line)
                fib_0line_values.append(lowest_low)
                fib_1line_values.append(highest_high)

            if self.enable_ema_line and len(fib_line_values):
                fib_line_values = numpy.asarray(fib_line_values)
                fib_ema = tulipy.ema(fib_line_values, self.fib_line_ema_length)

        return (
            fib_line_values,
            fib_long_line_values,
            fib_short_line_values,
            fib_0line_values,
            fib_1line_values,
            fib_ema,
        )

    def get_high_low(self, pivot_lows, pivot_highs, lows, highs, index):
        try:
            lowest_low = min(pivot_lows[index])
        except ValueError:
            start_index = self.get_last_low_index(pivot_lows, index)
            lowest_low = min(lows[start_index : index + 1])

        try:
            highest_high = max(pivot_highs[index])
        except ValueError:
            start_index = self.get_last_low_index(pivot_highs, index)
            highest_high = max(highs[start_index : index + 1])

        return lowest_low, highest_high

    def get_last_low_index(self, pivots, index):
        for i in range(index - 1, -1, -1):
            if pivots[i]:
                return i
        return 0

    def get_fib_lines(self, fib_side, highest_high, lowest_low):
        current_fib_line = (highest_high - lowest_low) * (
            1 - self.fib_line_level
        ) + lowest_low
        if fib_side == trading_enums.PositionSide.LONG:
            current_long_fib_line = current_fib_line
            current_short_fib_line = numpy.nan
        else:
            current_long_fib_line = numpy.nan
            current_short_fib_line = current_fib_line
        return current_fib_line, current_long_fib_line, current_short_fib_line

    async def store_fib_lines(
        self,
        fib_line_values,
        fib_ema,
        fib_0line_values,
        fib_1line_values,
        fib_long_line_values,
        fib_short_line_values,
        pivots_title_highs,
        pivots_title_lows,
        chart_location,
    ):
        if self.enable_both_line:
            await self.store_indicator_data(
                enable_rounding_plots=False,
                filter_nan_for_plots=True,
                title=f"Fib line ({self.fib_line_level}) {pivots_title_highs} / {pivots_title_lows}",
                data=fib_line_values,
                chart_location=chart_location,
            )
        if self.enable_ema_line:
            await self.store_indicator_data(
                enable_rounding_plots=False,
                filter_nan_for_plots=True,
                title=f"Fib ema line ({self.fib_line_level}) {pivots_title_highs} / {pivots_title_lows}",
                data=fib_ema,
                chart_location=chart_location,
            )
        if self.enable_0_line:
            await self.store_indicator_data(
                enable_rounding_plots=False,
                filter_nan_for_plots=True,
                title=f"Fib 0 line {pivots_title_highs} / {pivots_title_lows}",
                data=fib_0line_values,
                chart_location=chart_location,
            )
        if self.enable_1_line:
            await self.store_indicator_data(
                enable_rounding_plots=False,
                filter_nan_for_plots=True,
                title=f"Fib 1 line {pivots_title_highs} / {pivots_title_lows}",
                data=fib_1line_values,
                chart_location=chart_location,
            )
        # if self.enable_short_line:
        #     await self.store_indicator_data(
        #         enable_rounding_plots=False,
        #         filter_nan_for_plots=True,
        #         title=f"Fib short line ({self.fib_line_level}) {pivots_title_highs} / {pivots_title_lows}",
        #         data=fib_short_line_values,
        #         chart_location=chart_location,
        #         mode="markers",
        #         line_shape=None,
        #     )
        # if self.enable_long_line:
        #     await self.store_indicator_data(
        #         enable_rounding_plots=False,
        #         filter_nan_for_plots=True,
        #         title=f"Fib long line ({self.fib_line_level}) {pivots_title_highs} / {pivots_title_lows}",
        #         data=fib_long_line_values,
        #         chart_location=chart_location,
        #         mode="markers",
        #         line_shape=None,
        #     )


def detect_fib_side(
    highest_high, highs, lowest_low, lows, index
) -> trading_enums.PositionSide:
    for sub_index in range(0, index):
        if highest_high == highs[index - sub_index]:
            return trading_enums.PositionSide.LONG
        if lowest_low == lows[index - sub_index]:
            return trading_enums.PositionSide.SHORT
