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


class PsarIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "psar"
    TITLE = "Parabolic SAR"
    TITLE_SHORT = "PSAR"
    DESCRIPTION = "Parabolic SAR"
    acceleration_factor_step: float
    acceleration_factor_max: float
    candle_source_high: str
    candle_source_low: str

    def init_block_settings(self) -> None:
        self.acceleration_factor_step = self.user_input(
            "PSAR acceleration factor step", "float", 0.02, 0
        )
        self.acceleration_factor_max = self.user_input(
            "PSAR acceleration factor maximum", "float", 0.2, 0
        )
        self.candle_source_high = self.user_select_candle_source_name(
            "Select Candle High Source", matrix_enums.PriceDataSources.HIGH.value
        )
        self.candle_source_low = self.user_select_candle_source_name(
            "Select Candle Low Source", matrix_enums.PriceDataSources.LOW.value
        )
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=self.TITLE_SHORT,
            plot_switch_text=f"Plot {self.TITLE_SHORT}",
            plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        data = tulipy.psar(
            await self.get_candles(self.candle_source_high),
            await self.get_candles(self.candle_source_low),
            self.acceleration_factor_step,
            self.acceleration_factor_max,
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} {self.acceleration_factor_step} {self.acceleration_factor_max}",
            data=data,
        )