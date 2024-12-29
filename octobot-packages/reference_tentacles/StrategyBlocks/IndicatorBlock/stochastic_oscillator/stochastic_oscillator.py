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
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class StochasticOscillator(abstract_indicator_block.IndicatorBlock):
    NAME = "stochastic_oscillator"
    TITLE = "Stochastic Oscillator"
    TITLE_SHORT = "Stochastic Oscillator"
    DESCRIPTION = "Stochastic Oscillator"

    k_period: int
    slowing_period: int
    d_period: int

    def init_block_settings(self) -> None:
        self.k_period = self.user_input("stochastic %k length", "int", 14)
        self.slowing_period = self.user_input("stochastic %k smoothing", "int", 1)
        self.d_period = self.user_input("stochastic %d smoothing", "int", 3)
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} K",
            plot_switch_text=f"Plot {self.TITLE_SHORT} K",
            plot_color_switch_title=f"{self.TITLE_SHORT} K plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} K chart location",
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
        )
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} D",
            plot_switch_text=f"Plot {self.TITLE_SHORT} D",
            plot_color_switch_title=f"{self.TITLE_SHORT} D plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} D chart location",
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        stoch_k, stoch_d = tulipy.stoch(
            await self.get_candles(matrix_enums.PriceDataSources.HIGH.value),
            await self.get_candles(matrix_enums.PriceDataSources.LOW.value),
            await self.get_candles(matrix_enums.PriceDataSources.CLOSE.value),
            self.k_period,
            self.slowing_period,
            self.d_period,
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT}  K",
            data=stoch_k,
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT}  D",
            data=stoch_d,
        )
