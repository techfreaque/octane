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
from py_expression_eval import Parser
import octobot_commons.enums as commons_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)

import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


INDICATOR_ID_TO_VAR_NAME = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
    8: "i",
    9: "j",
}


class MathIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "math"
    TITLE = "Math Indicator"
    TITLE_SHORT = "Math"
    DESCRIPTION = (
        "This indicator can be used to apply math functions on one or more indicators. "
        "You can find all available operators in the documentation here: "
        "https://pypi.org/project/py-expression-eval"
    )

    amount_of_indicators: int
    formula: str
    parser: Parser = Parser()

    def init_block_settings(self) -> None:
        self.amount_of_indicators = self.user_input(
            "Amount of indicator inputs", "int", 1, min_val=1, max_val=7
        )
        for indicator_id in range(0, self.amount_of_indicators):
            self.activate_single_input_data_node(
                data_source_name=f"Indicator {INDICATOR_ID_TO_VAR_NAME[indicator_id]}",
                def_val="price_data",
            )
        self.formula = self.user_input(
            "Formula",
            "text",
            "2 * a",
        )
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Data",
            plot_switch_text=f"Plot {self.TITLE_SHORT} data",
            plot_color_switch_title=f"{self.TITLE_SHORT} data plot color",
            chart_location_title=f"{self.TITLE_SHORT} data chart location",
            default_plot_color=block_factory_enums.Colors.BLUE,
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        variables = {}
        title = self.formula
        indicators_data = []
        for indicator_id in range(0, self.amount_of_indicators):
            (
                data_source_values,
                _,
                data_source_title,
            ) = await self.get_input_node_data()
            title = title.replace(
                INDICATOR_ID_TO_VAR_NAME[indicator_id], data_source_title
            )
            indicators_data.append(numpy.array(data_source_values))
        cutted_indicators_data = cut_data_to_same_len(indicators_data)
        for indicator_id in range(0, self.amount_of_indicators):
            variables[INDICATOR_ID_TO_VAR_NAME[indicator_id]] = cutted_indicators_data[
                indicator_id
            ]
        results_array = self.parser.parse(self.formula).evaluate(variables)
        await self.store_indicator_data(
            title=f"Math result data ({title})",
            data=list(results_array),
        )
