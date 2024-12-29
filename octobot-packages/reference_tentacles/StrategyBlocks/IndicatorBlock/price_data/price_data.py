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

from octobot_commons import enums
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class PriceDataIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "price_data"
    TITLE = "Price Data Sources"
    TITLE_SHORT = "Price Data Sources"
    DESCRIPTION = (
        "Price Data Sources allow you to use different sources "
        "like high, low, heikin ashi and more"
    )
    candle_source: str

    def init_block_settings(self) -> None:
        self.candle_source = self.user_select_candle_source_name(
            "Select Candle Source", enable_volume=True
        )
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=f"Candle {self.candle_source}",
            plot_switch_text=f"Plot Candle {self.candle_source}",
            plot_color_switch_title=f"{self.candle_source} plot color",
            default_plot_color=block_factory_enums.Colors.PURPLE,
            chart_location_title=f"{self.candle_source} chart location",
            default_chart_location=enums.PlotCharts.SUB_CHART.value
            if self.candle_source == matrix_enums.PriceDataSources.VOLUME.value
            else enums.PlotCharts.MAIN_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        candle_data = await self.get_candles(self.candle_source)
        await self.store_indicator_data(
            title=f"Candle {self.candle_source}",
            data=candle_data,
        )
