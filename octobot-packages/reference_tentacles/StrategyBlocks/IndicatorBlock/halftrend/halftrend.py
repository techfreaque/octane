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


class HalftrendIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "halftrend"
    TITLE = "Halftrend"
    TITLE_SHORT = "Halftrend"
    DESCRIPTION = "Halftrend"

    amplitude: int
    channel_deviation: float

    def init_block_settings(self) -> None:
        self.amplitude = self.user_input("amplitude", "int", 2)
        self.channel_deviation = self.user_input("channel deviation", "float", 2)
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=self.TITLE_SHORT,
            plot_switch_text=f"Plot {self.TITLE_SHORT}",
            plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )
        self.register_indicator_data_output(
            title="ATR High",
            plot_switch_text="Plot ATR High",
            plot_color_switch_title="ATR High plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title="ATR High chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )
        self.register_indicator_data_output(
            title="ATR Low",
            plot_switch_text="Plot ATR Low",
            plot_color_switch_title="ATR Low plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title="ATR Low chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        highs = await self.get_candles(matrix_enums.PriceDataSources.HIGH.value)
        lows = await self.get_candles(matrix_enums.PriceDataSources.LOW.value)
        closes = await self.get_candles(matrix_enums.PriceDataSources.CLOSE.value)
        atr = tulipy.atr(highs, lows, closes, 100) / 2
        atr_with_deviation = atr * self.channel_deviation
        high_prices = tulipy.max(highs, self.amplitude)
        low_prices = tulipy.min(highs, self.amplitude)
        high_ma = tulipy.sma(highs, self.amplitude)
        low_ma = tulipy.sma(lows, self.amplitude)

        (
            highs,
            lows,
            closes,
            atr,
            atr_with_deviation,
            high_prices,
            high_prices,
            high_ma,
            low_ma,
        ) = cut_data_to_same_len(
            (
                highs,
                lows,
                closes,
                atr,
                atr_with_deviation,
                low_prices,
                high_prices,
                high_ma,
                low_ma,
            )
        )
        half_trend = []
        next_trend = 0
        trend = 0
        next_trends = [0]
        trends = [0]
        max_low_price = lows[0]
        min_high_price = highs[0]
        up = 0.0
        down = 0.0
        ups = []
        downs = []
        atr_highs = []
        atr_lows = []
        arrow_up = []
        arrow_down = []
        for index in range(1, len(highs)):
            if next_trend == 1:
                max_low_price = max(low_prices[index], max_low_price)
                if high_ma[index] < max_low_price and closes[index - 1] < lows[index]:
                    trend = 1
                    next_trend = 0
                    min_high_price = high_prices[index]
            else:
                min_high_price = min(high_prices[index], min_high_price)
                if low_ma[index] > min_high_price and closes[index - 1] > highs[index]:
                    trend = 0
                    next_trend = 1
                    max_low_price = low_prices[index]
            next_trends.append(next_trend)
            trends.append(trend)
            if trend == 0:
                if trends[index - 1] != 0:
                    up = downs[-1]
                    arrow_up = up - atr[index]
                else:
                    try:
                        up = max(max_low_price, ups[-1])
                    except IndexError:
                        up = max_low_price
                atr_lows.append(up + atr_with_deviation[index])
                atr_highs.append(up - atr_with_deviation[index])
            else:
                if trends[index - 1] != 1:
                    down = ups[-1]
                    arrow_down = down + atr[index]
                else:
                    down = max(min_high_price, downs[-1])
                atr_lows.append(down + atr_with_deviation[index])
                atr_highs.append(down - atr_with_deviation[index])
            ups.append(up)
            downs.append(down)
            half_trend.append(up if trend == 0 else down)
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} {self.amplitude} {self.channel_deviation}",
            data=half_trend,
        )
        await self.store_indicator_data(
            title=f"ATR High {self.amplitude} {self.channel_deviation}",
            data=atr_highs,
        )
        await self.store_indicator_data(
            title=f"ATR Low {self.amplitude} {self.channel_deviation}",
            data=atr_lows,
        )
