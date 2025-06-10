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

import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class SpecialLowsIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "special_lows"
    TITLE = "Special Lows"
    TITLE_SHORT = "Special Lows"
    DESCRIPTION = "Special Lows"

    multiplicator: float

    def init_block_settings(self) -> None:
        self.multiplicator = self.user_input("Special lows multiplicator", "float", 2)
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
        candle_high = await self.get_candles(matrix_enums.PriceDataSources.HIGH.value)
        candle_low = await self.get_candles(matrix_enums.PriceDataSources.LOW.value)
        candle_close = await self.get_candles(matrix_enums.PriceDataSources.CLOSE.value)
        data = candle_close - (candle_high - candle_low) * 1.1 / self.multiplicator
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} {self.multiplicator}",
            data=data,
        )
