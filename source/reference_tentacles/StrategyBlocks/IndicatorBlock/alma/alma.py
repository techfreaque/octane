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

import pandas as pd
import pandas_ta as pta
import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class AlmaIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "alma"
    TITLE = "Alma"
    TITLE_SHORT = "Alma"
    DESCRIPTION = "Alma"

    length: int
    candle_source: str
    offset: float
    sigma: int

    def init_block_settings(self) -> None:
        self.length = self.user_input(f"{self.TITLE} length", "int", 50, 0)
        self.offset = self.user_input("Offset", "float", 0.85)
        self.sigma = self.user_input("Sigma", "int", 6)
        self.candle_source = self.user_select_candle_source_name(
            f"Select {self.TITLE} Candle Source"
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
        candle_data = pd.Series(await self.get_candles(self.candle_source))
        alma_series = pta.alma(
            close=candle_data,
            length=self.length,
            distribution_offset=self.offset,
            sigma=self.sigma,
        )
        alma_series = alma_series.dropna()
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} l:{self.length} o:{self.offset} s:{self.sigma}",
            data=alma_series.to_list()[1:],
        )
