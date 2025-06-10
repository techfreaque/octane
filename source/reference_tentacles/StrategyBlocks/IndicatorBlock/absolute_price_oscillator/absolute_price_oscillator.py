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

import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class AbsolutePriceOscillator(abstract_indicator_block.IndicatorBlock):
    NAME = "absolute_price_oscillator"
    TITLE = "Absolute Price Oscillator"
    TITLE_SHORT = "Absolute Price Oscillator"
    DESCRIPTION = "Absolute Price Oscillator"

    fast_length: int
    slow_length: int
    candle_source: str

    def init_block_settings(self) -> None:
        self.fast_length = self.user_input(
            "Absolute Price Oscillator fast length", "int", 12
        )
        self.slow_length = self.user_input(
            "Absolute Price Oscillator slow length", "int", 26
        )
        self.candle_source = self.user_select_candle_source_name("Select Candle Source")
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=self.TITLE_SHORT,
            plot_switch_text=f"Plot {self.TITLE_SHORT}",
            plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} chart location",
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        try:
            data = tulipy.apo(
                await self.get_candles(self.candle_source),
                self.fast_length,
                self.slow_length,
            )
        except tulipy.lib.InvalidOptionError:
            raise RuntimeError(
                f"Absolute Price Oscillator (slow: {self.slow_length} fast: {self.fast_length}): "
                f"fast length cant be longer than slow length"
            )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} {self.fast_length} {self.slow_length} {self.candle_source}",
            data=data,
        )
