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
from finta import TA as fta
import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class VwMacdIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "vw_macd"
    TITLE = "VW MACD"
    TITLE_SHORT = "VW MACD"
    DESCRIPTION = "VW MACD"

    fast_length: int
    slow_length: int
    signal_smoothing: int

    def init_block_settings(self) -> None:
        self.fast_length = self.user_input("VW MACD fast length", "int", 12)
        self.slow_length = self.user_input("VW MACD slow length", "int", 26)
        self.signal_smoothing = self.user_input("VW MACD signal smoothing", "int", 9)
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=self.TITLE_SHORT,
            plot_switch_text=f"Plot {self.TITLE_SHORT}",
            plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} chart location",
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
        )
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Signal",
            plot_switch_text=f"Plot {self.TITLE_SHORT} signal",
            plot_color_switch_title=f"{self.TITLE_SHORT} signal plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} signal chart location",
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        df = pd.DataFrame(
            {
                "open": await self.get_candles(
                    matrix_enums.PriceDataSources.OPEN.value
                ),
                "high": await self.get_candles(
                    matrix_enums.PriceDataSources.HIGH.value
                ),
                "low": await self.get_candles(matrix_enums.PriceDataSources.LOW.value),
                "close": await self.get_candles(
                    matrix_enums.PriceDataSources.CLOSE.value
                ),
                "volume": await self.get_candles(
                    matrix_enums.PriceDataSources.VOLUME.value
                ),
            }
        )
        macd_df = fta.VW_MACD(
            df,
            period_fast=self.fast_length,
            period_slow=self.slow_length,
            signal=self.signal_smoothing,
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} {self.signal_smoothing} {self.fast_length} {self.slow_length}",
            data=list(macd_df.iloc[self.slow_length * 2 :, 1]),
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} Signal {self.signal_smoothing} {self.fast_length} {self.slow_length}",
            data=list(macd_df.iloc[self.slow_length * 2 :, 0]),
        )
