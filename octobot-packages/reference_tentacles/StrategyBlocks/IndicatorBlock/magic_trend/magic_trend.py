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
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class MagicTrendIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "magic_trend"
    TITLE = "Magic Trend"
    TITLE_SHORT = "Magic Trend"
    DESCRIPTION = "Magic Trend"

    cci_length: int
    atr_multiplier: float
    atr_length: int

    def init_block_settings(self) -> None:
        self.cci_length = self.user_input("CCI length", "int", 20, 1)
        self.atr_multiplier = self.user_input("ATR multiplier", "float", 1, 0.001)
        self.atr_length = self.user_input("ATR length", "int", 5, 1)
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
        highs = await self.get_candles(matrix_enums.PriceDataSources.HIGH.value)
        lows = await self.get_candles(matrix_enums.PriceDataSources.LOW.value)
        closes = await self.get_candles(matrix_enums.PriceDataSources.CLOSE.value)
        tr = tulipy.tr(
            highs,
            lows,
            closes,
        )
        atr = tulipy.sma(tr, self.atr_length)
        cci = tulipy.cci(highs, lows, closes, self.cci_length)
        highs, tr, atr, lows, closes, cci = cut_data_to_same_len(
            (highs, tr, atr, lows, closes, cci)
        )
        up_t = lows - atr * self.atr_multiplier
        down_t = highs + atr * self.atr_multiplier
        cci_above_o = cci >= 0
        magic_trend = []
        for index, this_cci_above_0 in enumerate(cci_above_o):
            this_magic_trend = magic_trend[-1] if len(magic_trend) else 0
            if this_cci_above_0:
                upt_above_mi = up_t[index] < this_magic_trend
                if upt_above_mi:
                    magic_trend.append(this_magic_trend)
                else:
                    magic_trend.append(up_t[index])
            else:
                upt_above_mi = down_t[index] > this_magic_trend
                if upt_above_mi:
                    magic_trend.append(this_magic_trend)
                else:
                    magic_trend.append(down_t[index])
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} {self.cci_length} {self.atr_multiplier} {self.atr_length}",
            data=magic_trend[3:],  # remove first few as there are zeros
        )
