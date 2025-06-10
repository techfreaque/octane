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


import tentacles.Meta.Keywords.indicator_keywords.moving.moving_up_down as moving_up_down
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_evaluator_block as abstract_evaluator_block


class DataIsFallingEvaluator(abstract_evaluator_block.EvaluatorBlock):
    NAME = "data_is_falling"
    TITLE = "Data is falling"
    TITLE_SHORT = TITLE
    DESCRIPTION = (
        "Data is falling, takes a single data source "
        "and gives you signals when it is falling."
    )
    signal_lag: int
    sideways_is_falling: bool
    only_one_signal: bool

    def init_block_settings(self) -> None:
        selected_indicator = self.activate_single_input_data_node(
            enable_static_value=False
        )
        self.signal_lag = self.user_input(
            "Amount of consecutive falling candles before flashing a signal",
            "int",
            def_val=2,
            min_val=1,
            grid_columns=12,
        )
        self.sideways_is_falling = self.user_input(
            "Sideways counts as falling", "boolean", True, grid_columns=12
        )
        self.only_one_signal = self.user_input(
            "Flash signals only on the first candle", "boolean", False, grid_columns=12
        )
        self.register_evaluator_data_output(
            title="Falling Signals",
            plot_switch_text=f"Plot when data source is falling",
            plot_color_switch_title="Signals plot color",
            default_plot_color=block_factory_enums.Colors.RED,
            allow_move_signal_to_the_right=True,
        )

    async def execute_block(
        self,
    ) -> None:
        (
            data_source_values,
            chart_location,
            indicator_title,
        ) = await self.get_input_node_data()
        signals = moving_up_down.moving_down(
            data_source_values,
            self.signal_lag,
            sideways_is_falling=self.sideways_is_falling,
            only_first_signal=self.only_one_signal,
        )
        await self.store_evaluator_signals(
            title=f"{indicator_title} is falling",
            signals=signals,
            signal_values=data_source_values,
            chart_location=chart_location,
        )
