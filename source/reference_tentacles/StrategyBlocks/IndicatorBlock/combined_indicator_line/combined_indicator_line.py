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

import enum
from typing import Literal
import numpy as numpy
from octobot_commons.enums import UserInputTypes
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class ValueSide(enum.Enum):
    USE_LOWEST_LEVEL = "Use lowest data values"
    USE_HIGHEST_LEVEL = "Use highest data values"
    USE_INDICATOR_C_IF_LOWER = (
        "Use Indicator C if Indicator A is lower than Indicator B, else use Indicator A"
    )
    USE_INDICATOR_C_IF_HIGHER = "Use Indicator C if Indicator A is higher than Indicator B, else use Indicator A"


class CombinedIndicatorLineIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "combined_indicator_line"
    TITLE = "Combined Indicator Line"
    TITLE_SHORT = "Combined Indicator Line"
    DESCRIPTION = "Take the highest / lowest values of two indicators and combine them into a new indicator data source"

    value_side_to_keep: ValueSide

    def init_block_settings(self) -> None:
        self.value_side_to_keep = ValueSide(
            self.user_input(
                "Value side to keep",
                UserInputTypes.OPTIONS,
                def_val=ValueSide.USE_LOWEST_LEVEL.value,
                options=[
                    ValueSide.USE_LOWEST_LEVEL.value,
                    ValueSide.USE_HIGHEST_LEVEL.value,
                    ValueSide.USE_INDICATOR_C_IF_LOWER.value,
                    ValueSide.USE_INDICATOR_C_IF_HIGHER.value,
                ],
            )
        )
        self.activate_single_input_data_node(
            enable_force_def_val=True,
            data_source_name="Indicator B",
            def_val="price_data",
        )
        self.activate_single_input_data_node(
            enable_force_def_val=True,
            data_source_name="Indicator A",
            def_val="price_data",
        )
        if self.value_side_to_keep in [
            ValueSide.USE_INDICATOR_C_IF_LOWER,
            ValueSide.USE_INDICATOR_C_IF_HIGHER,
        ]:
            self.activate_single_input_data_node(
                enable_force_def_val=True,
                data_source_name="Indicator C",
                def_val="price_data",
            )

        self.register_indicator_data_output(
            title="Combined indicator line",
            plot_switch_text="Plot Combined indicator line",
            plot_color_switch_title="Combined indicator line plot color",
            chart_location_title="Combined indicator line chart location",
            default_plot_color=block_factory_enums.Colors.ORCHID,
        )
        self.user_select_data_source_time_frame()

    async def execute_block(self) -> None:
        combined_indicator_line: numpy.ndarray
        title: str
        (
            indicator_b_data,
            _,
            indicator_b_title,
        ) = await self.get_input_node_data()
        (
            indicator_a_data,
            chart_location,
            indicator_a_title,
        ) = await self.get_input_node_data()
        if self.value_side_to_keep in [
            ValueSide.USE_INDICATOR_C_IF_LOWER,
            ValueSide.USE_INDICATOR_C_IF_HIGHER,
        ]:
            (
                indicator_c_data,
                _,
                indicator_c_title,
            ) = await self.get_input_node_data()
            indicator_a_data, indicator_b_data, indicator_c_data = cut_data_to_same_len(
                (
                    numpy.asarray(indicator_a_data),
                    numpy.asarray(indicator_b_data),
                    numpy.asarray(indicator_c_data),
                )
            )
            if self.value_side_to_keep is ValueSide.USE_INDICATOR_C_IF_LOWER:
                combined_indicator_line = numpy.where(
                    indicator_a_data < indicator_b_data,
                    indicator_c_data,
                    indicator_a_data,
                )
            else:
                combined_indicator_line = numpy.where(
                    indicator_a_data > indicator_b_data,
                    indicator_c_data,
                    indicator_a_data,
                )
            title = f"Combined line (Use {indicator_c_title} if {indicator_a_title} {'<' if self.value_side_to_keep == ValueSide.USE_INDICATOR_C_IF_LOWER else '>'} {indicator_b_title}, else use {indicator_a_title})"
        else:
            indicator_a_data, indicator_b_data = cut_data_to_same_len(
                (indicator_a_data, indicator_b_data)
            )
            if self.value_side_to_keep == ValueSide.USE_HIGHEST_LEVEL:
                combined_indicator_line = numpy.maximum(
                    indicator_a_data, indicator_b_data
                )
            else:
                combined_indicator_line = numpy.minimum(
                    indicator_a_data, indicator_b_data
                )
            title = f"Combined line ({'Highest of' if self.value_side_to_keep == ValueSide.USE_HIGHEST_LEVEL else 'Lowest of'}) {indicator_a_title} / {indicator_b_title}"
        await self.store_indicator_data(
            enable_rounding_plots=False,
            filter_nan_for_plots=True,
            title=title,
            data=combined_indicator_line,
        )
