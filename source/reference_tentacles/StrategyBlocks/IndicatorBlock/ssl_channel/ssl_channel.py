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
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)
import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class SSLChannelIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "ssl_channel"
    TITLE = "SSL Channel"
    TITLE_SHORT = "SSL Channel"
    DESCRIPTION = "SSL Channel"

    length: int

    def init_block_settings(self) -> None:
        self.length = self.user_input("SSL length", "int", 50, 0)
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Down",
            plot_switch_text=f"Plot {self.TITLE_SHORT} Down",
            plot_color_switch_title=f"{self.TITLE_SHORT} Down plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} Down chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Up",
            plot_switch_text=f"Plot {self.TITLE_SHORT} Up",
            plot_color_switch_title=f"{self.TITLE_SHORT} Up plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} Up chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        lows = await self.get_candles(PriceDataSources.LOW.value)
        highs = await self.get_candles(PriceDataSources.HIGH.value)
        closes = await self.get_candles(PriceDataSources.CLOSE.value)
        ssl_down, ssl_up = compute_ssl_channel(highs, lows, closes, self.length)
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} Down {self.length}",
            data=ssl_down,
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} Up {self.length}",
            data=ssl_up,
        )


def compute_ssl_channel(highs, lows, closes, length):
    sma_high = tulipy.ema(highs, length)
    sma_low = tulipy.ema(lows, length)
    ssl_down = []
    ssl_up = []
    hlv = []
    data_length = len(sma_high)
    closes = closes[-data_length:]
    for index in range(1, len(sma_high)):
        if closes[index] > sma_high[index]:
            hlv.append(1)
            ssl_down.append(sma_low[index])
            ssl_up.append(sma_high[index])
        elif closes[index] < sma_low[index]:
            hlv.append(-1)
            ssl_down.append(sma_high[index])
            ssl_up.append(sma_low[index])
        elif hlv:
            if hlv[-1] > 0:
                hlv.append(1)
                ssl_down.append(sma_low[index])
                ssl_up.append(sma_high[index])
            elif hlv[-1] < 0:
                hlv.append(-1)
                ssl_down.append(sma_high[index])
                ssl_up.append(sma_low[index])
            else:
                ssl_down.append(0)
                ssl_up.append(0)
    return ssl_down, ssl_up
