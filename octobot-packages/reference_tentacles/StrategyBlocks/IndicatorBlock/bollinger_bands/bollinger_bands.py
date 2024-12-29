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

import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class BollingerBandsIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "bollinger_bands"
    TITLE = "Bollinger Bands"
    TITLE_SHORT = "Bollinger Bands"
    DESCRIPTION = "Bollinger Bands"

    length: int
    stddev: int
    candle_source: str
    enable_upper: bool
    enable_lower: bool
    enable_middle: bool

    def init_block_settings(self) -> None:
        self.length = self.user_input("Bollinger Bands length", "int", 12)
        self.stddev = self.user_input("Bollinger Bands Standard Deviation", "int", 2)
        self.candle_source = self.user_select_candle_source_name(
            "Select Candle Source", enable_volume=True
        )
        self.user_select_data_source_time_frame()
        self.enable_upper = self.user_input(
            "Enable upper Bollinger Band", "boolean", True
        )
        if self.enable_upper:
            self.register_indicator_data_output(
                title="Upper BB",
                plot_switch_text="Plot Upper Bollinger Band",
                plot_color_switch_title="Upper Bollinger Band plot color",
                default_plot_color=block_factory_enums.Colors.ORANGE,
                chart_location_title="Upper Bollinger Band chart location",
                default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
            )
        self.enable_middle = self.user_input(
            "Enable middle Bollinger Band", "boolean", True
        )
        if self.enable_middle:
            self.register_indicator_data_output(
                title="Middle BB",
                plot_switch_text="Plot Middle Bollinger Band",
                plot_color_switch_title="Middle Bollinger Band plot color",
                default_plot_color=block_factory_enums.Colors.ORANGE,
                chart_location_title="Middle Bollinger Band chart location",
                default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
            )
        self.enable_lower = self.user_input(
            "Enable lower Bollinger Band", "boolean", True
        )
        if self.enable_lower:
            self.register_indicator_data_output(
                title="Lower BB",
                plot_switch_text="Plot Lower Bollinger Band",
                plot_color_switch_title="Lower Bollinger Band plot color",
                default_plot_color=block_factory_enums.Colors.ORANGE,
                chart_location_title="Lower Bollinger Band chart location",
                default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
            )

    async def execute_block(
        self,
    ) -> None:
        bbands_lower, bbands_middle, bbands_upper = tulipy.bbands(
            await self.get_candles(self.candle_source), self.length, self.stddev
        )
        if self.enable_upper:
            await self.store_indicator_data(
                title=f"Upper {self.TITLE_SHORT} {self.length} {self.stddev}",
                data=bbands_upper,
            )
        if self.enable_middle:
            await self.store_indicator_data(
                title=f"Middle {self.TITLE_SHORT} {self.length} {self.stddev}",
                data=bbands_middle,
            )
        if self.enable_lower:
            await self.store_indicator_data(
                title=f"Lower {self.TITLE_SHORT} {self.length} {self.stddev}",
                data=bbands_lower,
            )
