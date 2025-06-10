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

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class SuperTrendIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "supertrend"
    TITLE = "Supertrend"
    TITLE_SHORT = "Supertrend"
    DESCRIPTION = "Supertrend"

    length: int
    multiplier: int

    def init_block_settings(self) -> None:
        self.multiplier = self.user_input("supertrend ATR multiplier", "int", 3)
        self.length = self.user_input("supertrend ATR period", "int", 10)
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
        highs = pd.Series(
            await self.get_candles(matrix_enums.PriceDataSources.HIGH.value)
        )
        lows = pd.Series(
            await self.get_candles(matrix_enums.PriceDataSources.LOW.value)
        )
        closes = pd.Series(
            await self.get_candles(matrix_enums.PriceDataSources.CLOSE.value)
        )
        strend_df = pta.supertrend(
            highs, lows, closes, length=self.length, multiplier=self.multiplier
        )
        try:
            strend_df = strend_df.drop(strend_df.columns[[2, 3]], axis=1)
        except AttributeError as error:
            raise RuntimeError("Supertrend doesnt have enough data") from error
        strend_df = strend_df.dropna()
        supert = strend_df.iloc[1:, 0]
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} m:{self.multiplier} l:{self.length}",
            data=list(supert),
        )
