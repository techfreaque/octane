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

import octobot_commons.enums as enums
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class StaticValueIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "static_value"
    TITLE = "Static Value"
    TITLE_SHORT = "Static Value"
    DESCRIPTION = "Static Value can be used for semi automated trading based on levels"

    static_value: float

    def init_block_settings(self) -> None:
        self.static_value = self.user_input("select a static value", "float", 40)
        self.register_indicator_data_output(
            title=self.TITLE_SHORT,
            plot_switch_text=f"Plot {self.TITLE_SHORT}",
            plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
            default_plot_color=block_factory_enums.Colors.RED,
            chart_location_title=f"{self.TITLE_SHORT} chart location",
            default_chart_location=enums.PlotCharts.MAIN_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        values = [float(self.static_value)] * len(
            await self.get_candles(matrix_enums.PriceDataSources.CLOSE.value)
        )
        await self.store_indicator_data(
            title=f"Static value: {self.static_value}",
            data=values,
        )
