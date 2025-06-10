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

import tentacles.Meta.Keywords.indicator_keywords.above_below.is_above_below as is_above_below
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_evaluator_block as abstract_evaluator_block


class DataWasBelowDataEvaluator(abstract_evaluator_block.EvaluatorBlock):
    NAME = "data_was_below_data"
    TITLE = "Data was below data"
    TITLE_SHORT = "Data was below data"
    DESCRIPTION = (
        "Data was below data allows you to get signals when one data source "
        "was below the other data source in the near past"
    )

    confirmation_time: int
    look_back: int
    below_percent: float

    def init_block_settings(self) -> None:
        self.activate_single_input_data_node(
            def_val="price_data", data_source_name="Data source above"
        )
        self.activate_single_input_data_node(
            data_source_name="Data source below",
            def_val="ema",
        )
        self.confirmation_time = self.user_input("min candles below", "int", 0, 0)
        self.look_back = self.user_input("was below x candles back", "int", 1, 1)
        self.below_percent = self.user_input("was x percent below", "float", 0)
        self.register_evaluator_data_output(
            title="Signals",
            plot_switch_text="Plot signals",
            plot_color_switch_title="Signals plot color",
            default_plot_color=block_factory_enums.Colors.GREEN,
        )

    async def execute_block(
        self,
    ) -> None:
        (
            data_below_values,
            chart_location,
            above_values_detailed_title,
        ) = await self.get_input_node_data()
        (
            data_above_values,
            _,
            below_values_detailed_title,
        ) = await self.get_input_node_data()
        is_below_data = is_above_below.is_below(
            below_data=data_above_values,
            above_data=data_below_values,
            confirmation_time=self.confirmation_time,
            below_percent=self.below_percent,
            max_history=not self.block_factory.live_recording_mode,
        )
        signals = []
        for index in range(self.look_back, len(is_below_data)):
            signals.append(1 if is_below_data[index - self.look_back] == 1 else 0)
        await self.store_evaluator_signals(
            title=f"{above_values_detailed_title} was below {below_values_detailed_title}",
            signals=signals,
            signal_values=data_above_values,
            chart_location=chart_location,
        )
