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


import numpy as np
import tulipy
import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class GrowthRateIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "growth_rate"
    TITLE = "Growth Rate"
    TITLE_SHORT = "Growth Rate"
    DESCRIPTION = "Growth Rate"

    length: int

    def init_block_settings(self) -> None:
        self.activate_single_input_data_node(
            data_source_name="Growth Rate Source",
            def_val="price_data",
        )
        self.length = self.user_input(
            "Growth rate Moving Average length",
            "int",
            5,
            min_val=1,
        )

        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=self.TITLE_SHORT,
            plot_switch_text=f"Plot {self.TITLE_SHORT}",
            plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
            chart_location_title=f"{self.TITLE_SHORT} chart location",
            default_plot_color=block_factory_enums.Colors.GREEN,
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
        )
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Moving Average",
            plot_switch_text=f"Plot {self.TITLE_SHORT} Moving Average",
            plot_color_switch_title=f"{self.TITLE_SHORT} Moving Average plot color",
            chart_location_title=f"{self.TITLE_SHORT} Moving Average chart location",
            default_plot_color=block_factory_enums.Colors.BLUE,
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        (
            data_source_values,
            _,
            data_source_title,
        ) = await self.get_input_node_data()
        growth_rates = np.exp(np.diff(np.log(data_source_values))) - 1
        growth_rates = growth_rates * 10000
        growth_rates_ma = tulipy.ema(growth_rates, self.length)
        await self.store_indicator_data(
            title=f"{data_source_title} growth rate {self.length}",
            data=list(growth_rates),
        )
        await self.store_indicator_data(
            title=f"{data_source_title} growth rate MA {self.length}",
            data=list(growth_rates_ma),
        )
