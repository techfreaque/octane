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

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
from tentacles.Meta.Keywords.block_factory.input_output_nodes import (
    evaluator_signals_output_node,
)
import tentacles.Meta.Keywords.indicator_keywords.divergences.divergence as divergence
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_evaluator_block as abstract_evaluator_block


class DivergenceEvaluator(abstract_evaluator_block.EvaluatorBlock):
    NAME = "divergence"
    TITLE = "Divergence between Data"
    TITLE_SHORT = TITLE
    DESCRIPTION = (
        "Divergence can be use to compare lows/highs of two data sources "
        "and get signals when there is divergence between them."
    )
    confirmation_time: int
    time_for_ll: int
    max_pivot_age: int
    min_pivot_age: int
    pivot_match_range: int
    pivot_other_loockback_offset: int
    pivot_lookback: int
    first_signal_only: bool
    wait_for_a_reversal: bool

    def init_block_settings(self) -> None:
        self.activate_single_input_data_node(
            data_source_name="Base Pivots",
            def_val="highs_and_lows",
            enable_force_def_val=True,
        )
        self.activate_single_input_data_node(
            data_source_name="Other Pivots",
            def_val="highs_and_lows",
            enable_force_def_val=True,
        )
        self.confirmation_time = self.user_input(
            "Bars it takes to confirm divergence", "int", 0, 0
        )
        self.time_for_ll = self.user_input(
            "bars until a lower low is invalid", "int", 1, 1
        )
        self.max_pivot_age = self.user_input(
            "maximum pivots age in Bars", "int", 800, 2
        )
        self.min_pivot_age = self.user_input("minimum pivots age in Bars", "int", 0, 0)
        self.pivot_match_range = self.user_input("range to match pivots", "int", 10, 1)
        self.pivot_other_loockback_offset = self.user_input(
            "pivot lookback offset other data", "int", -1, max_val=0
        )
        self.pivot_lookback = self.user_input("pivot lookback length", "int", 20, 3)
        self.first_signal_only = self.user_input(
            "flash signal only on the first candle", "boolean", False
        )
        self.wait_for_a_reversal = self.user_input(
            "wait for a reversal above base pivot", "boolean", True
        )
        # ll_only = await user_input(maker.ctx, f"{evaluator.config_path} trigger when lower low found on base data",
        #                            "boolean", True)
        self.register_evaluator_data_output(
            title="Divergence Signals",
            plot_switch_text="Plot divergence signals",
            plot_color_switch_title="Signals plot color",
            default_plot_color=block_factory_enums.Colors.GREEN,
        )

    async def execute_block(
        self,
    ) -> None:
        (
            cutted_base_values,
            base_conditions,
            base_values,
            chart_location,
            base_title,
        ) = await self.get_input_node_data(get_additional_node_data=True)
        (
            cutted_other_values,
            other_conditions,
            other_values,
            second_chart_location,
            other_title,
        ) = await self.get_input_node_data(get_additional_node_data=True)
        (
            div_data,
            div_other_values,
            div_base_values,
            cleaned_div_data,
            cleaned_div_other_values,
            cleaned_div_base_values,
        ) = divergence.get_divergence(
            base_data=base_conditions,
            other_data=other_conditions,
            base_values=cutted_base_values,
            other_values=cutted_other_values,
            base_source_data=base_values,
            other_source_data=other_values,
            max_pivot_age=self.max_pivot_age,
            min_pivot_age=self.min_pivot_age,
            time_for_ll=self.time_for_ll,
            confirmation_time=self.confirmation_time,
            pivot_lookback_base=self.pivot_lookback,
            pivot_lookback_other=self.pivot_lookback
            + self.pivot_other_loockback_offset,
            pivot_match_range=self.pivot_match_range,
            wait_for_a_reversal=self.wait_for_a_reversal,
            ll_only=False,
        )
        if self.first_signal_only:
            signals = cleaned_div_data
            second_values = cleaned_div_other_values
            values = cleaned_div_base_values
        else:
            signals = div_data
            second_values = div_other_values
            values = div_base_values
        await self.store_evaluator_signals(
            title=f"divergence (ll on: {base_title} hl on; {other_title})(base)",
            signals=signals,
            signal_values=values,
            chart_location=chart_location,
        )
        output_node: evaluator_signals_output_node.EvaluatorSignalsOutputNode = next(
            iter(self.output_nodes.values())
        )
        if output_node.plot_enabled:
            await self.plot_and_store_signals(
                title=f"divergence (ll on: {base_title} hl on; {other_title})(other)",
                signals=signals,
                signal_values=second_values,
                chart_location=second_chart_location,
                plot_color=output_node.plot_color.value
                if output_node.plot_color
                else None,
                size=10,
            )
