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

import pandas_ta as pta
import pandas as pd
import octobot_commons.enums as commons_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class KeltnerChannelIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "keltner_channel"
    TITLE = "Keltner Channel"
    TITLE_SHORT = "Keltner Channel"
    DESCRIPTION = "Keltner Channel"

    length: int
    multiplier: int

    def init_block_settings(self) -> None:
        self.multiplier = self.user_input("keltner channel multiplier", "int", 2)
        self.length = self.user_input("keltner channel period", "int", 20)
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Base",
            plot_switch_text=f"Plot {self.TITLE_SHORT} Base",
            plot_color_switch_title=f"{self.TITLE_SHORT} Base plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} Base chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Low",
            plot_switch_text=f"Plot {self.TITLE_SHORT} Low",
            plot_color_switch_title=f"{self.TITLE_SHORT} Low plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} Low chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Low",
            plot_switch_text=f"Plot {self.TITLE_SHORT} Low",
            plot_color_switch_title=f"{self.TITLE_SHORT} Low plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} Low chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        highs = pd.Series(await self.get_candles(PriceDataSources.HIGH.value))
        lows = pd.Series(await self.get_candles(PriceDataSources.LOW.value))
        closes = pd.Series(await self.get_candles(PriceDataSources.CLOSE.value))
        keltner_df = pta.kc(
            highs, lows, closes, length=self.length, multiplier=self.multiplier
        )
        keltner_df = keltner_df.dropna()
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} Base {self.multiplier} {self.length}",
            data=list(keltner_df.iloc[:, 1]),
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} Low {self.multiplier} {self.length}",
            data=list(keltner_df.iloc[:, 0]),
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} High {self.multiplier} {self.length}",
            data=list(keltner_df.iloc[:, 2]),
        )
