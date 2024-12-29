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

import numpy

import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class BreakUp2Indicator(abstract_indicator_block.IndicatorBlock):
    NAME = "break_up2"
    TITLE = "Break Up 2"
    TITLE_SHORT = "Break Up 2"
    DESCRIPTION = "Break Up 2"

    fib_extension: float

    def init_block_settings(self) -> None:
        self.activate_single_input_data_node(
            enable_force_def_val=True,
            data_source_name="Break up 2 data source",
            def_val="break_up",
        )
        self.activate_single_input_data_node(
            enable_force_def_val=True,
            data_source_name="H4 data source",
            def_val="special_highs",
        )
        self.fib_extension = self.user_input("Fib extension value", "float", 1.168)
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
        (
            indictaror_1_data,
            _,
            indictaror_1_title,
        ) = await self.get_input_node_data()
        (
            indictaror_2_data,
            _,
            indictaror_2_title,
        ) = await self.get_input_node_data()
        indictaror_1_data, indictaror_2_data = cut_data_to_same_len(
            (indictaror_1_data, indictaror_2_data)
        )
        indictaror_1_data = numpy.array(indictaror_1_data)
        indictaror_2_data = numpy.array(indictaror_2_data)
        data = indictaror_1_data + self.fib_extension * (
            indictaror_1_data - indictaror_2_data
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} (from {indictaror_2_title} & {indictaror_1_title})",
            data=data,
        )
