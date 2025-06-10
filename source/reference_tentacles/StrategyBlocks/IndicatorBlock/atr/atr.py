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

import tulipy
import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class AtrIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "atr"
    TITLE = "Average True Range"
    TITLE_SHORT = "ATR"
    DESCRIPTION = "Average True Range"

    length: int
    enable_atr: bool
    enable_atr_low: bool
    atr_low_multiplier: float
    enable_atr_high: bool
    atr_high_multiplier: float

    def init_block_settings(self) -> None:
        self.length = self.user_input("ATR length", "int", 50, 0)
        self.enable_atr = self.user_input(
            "enable_atr", "boolean", True, title="Enable ATR"
        )
        if self.enable_atr:
            self.register_indicator_data_output(
                title=self.TITLE_SHORT,
                plot_switch_text=f"Plot {self.TITLE_SHORT}",
                plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
                default_plot_color=block_factory_enums.Colors.ORANGE,
                chart_location_title=f"{self.TITLE_SHORT} chart location",
                default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
            )
        self.enable_atr_low = self.user_input(
            "enable_atr_low", "boolean", False, title="Enable ATR low"
        )
        if self.enable_atr_low:
            self.atr_low_multiplier = self.user_input(
                "atr_low_multiplier", "float", 1, title="ATR low multiplier"
            )
            self.register_indicator_data_output(
                title=f"{self.TITLE_SHORT} low",
                plot_switch_text=f"Plot {self.TITLE_SHORT} low",
                plot_color_switch_title=f"{self.TITLE_SHORT} low plot color",
                default_plot_color=block_factory_enums.Colors.RED,
                chart_location_title=f"{self.TITLE_SHORT} low chart location",
                default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
            )
        self.enable_atr_high = self.user_input(
            "enable_atr_high", "boolean", False, title="Enable ATR high"
        )
        if self.enable_atr_high:
            self.atr_high_multiplier = self.user_input(
                "atr_high_multiplier", "float", 1, title="ATR high multiplier"
            )
            self.register_indicator_data_output(
                title=f"{self.TITLE_SHORT} high",
                plot_switch_text=f"Plot {self.TITLE_SHORT} high",
                plot_color_switch_title=f"{self.TITLE_SHORT} high plot color",
                default_plot_color=block_factory_enums.Colors.RED,
                chart_location_title=f"{self.TITLE_SHORT} high chart location",
                default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
            )
        self.user_select_data_source_time_frame()

    async def execute_block(
        self,
    ) -> None:
        closes = await self.get_candles(matrix_enums.PriceDataSources.CLOSE.value)
        atr_data = tulipy.atr(
            await self.get_candles(matrix_enums.PriceDataSources.HIGH.value),
            await self.get_candles(matrix_enums.PriceDataSources.LOW.value),
            closes,
            self.length,
        )
        if self.enable_atr:
            await self.store_indicator_data(
                title=f"{self.TITLE_SHORT} {self.length}",
                data=atr_data,
            )
        cutted_closes = None
        if self.enable_atr_low or self.enable_atr_high:
            cutted_closes = closes[-len(atr_data) :]
        if self.enable_atr_low:
            low_data = cutted_closes - atr_data
            await self.store_indicator_data(
                title=f"{self.TITLE_SHORT} Low {self.length} {self.atr_low_multiplier}",
                data=low_data,
            )
        if self.enable_atr_high:
            high_data = cutted_closes + atr_data
            await self.store_indicator_data(
                title=f"{self.TITLE_SHORT} High {self.length} {self.atr_high_multiplier}",
                data=high_data,
            )
