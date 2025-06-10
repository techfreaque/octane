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

import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_evaluator_block as abstract_evaluator_block


class DataIsTheSameAsDataEvaluator(abstract_evaluator_block.EvaluatorBlock):
    NAME = "data_is_the_same_as_data"
    TITLE = "Data is the same as Data"
    TITLE_SHORT = TITLE
    DESCRIPTION = (
        "Data is the same as Data can be used to get signals when "
        "on data source is the same as the other data source"
    )
    signal_lag: int
    sideways_is_rising: bool
    only_one_signal: bool

    def init_block_settings(self) -> None:
        raise NotImplementedError("is_the_same is not supported on the current version")
        selected_indicator = self.activate_single_input_data_node(
            enable_static_value=False
        )
        self.register_evaluator_data_output(
            title="Rising Signals",
            plot_switch_text=f"Plot when {selected_indicator} is rising",
            plot_color_switch_title="Signals plot color",
            default_plot_color=block_factory_enums.Colors.GREEN,
        )

    async def execute_block(
        self,
    ) -> None:
        pass
        # (
        #     data_source_values,
        #     chart_location,
        #     indicator_title,
        # ) = await self.get_input_node_data()
        # await self.store_evaluator_signals(
        #     title=f"{indicator_title} is rising",
        #     signals=signals,
        #     signal_values=data_source_values,
        #     chart_location=chart_location,
        # )

        # above_values_title = await activate_configurable_indicator(
        #     maker, evaluator, def_val="price_data", data_source_name="data source above"
        # )
        # below_values_title = await activate_configurable_indicator(
        #     maker,
        #     evaluator,
        #     data_source_name="data source below",
        #     def_val="EMA",
        #     indicator_id=2,
        # )
        # confirmation_time = await user_input2(
        #     maker, evaluator, "min candles above", "int", 0, 0
        # )
        # look_back = await user_input2(
        #     maker, evaluator, "was above x candles back", "int", 1, 1
        # )
        # above_percent = await user_input2(maker, evaluator, "was x percent above", "int", 0)
        # await allow_enable_plot(
        #     maker,
        #     evaluator,
        #     f"Plot when {above_values_title} was above {below_values_title}",
        # )
        # (
        #     data_above_values,
        #     evaluator.chart_location,
        #     above_values_detailed_title,
        # ) = await get_configurable_indicator(maker, evaluator)
        # evaluator.values, _, below_values_detailed_title = await get_configurable_indicator(
        #     maker, evaluator, indicator_id=2
        # )
        # evaluator.signals = []
        # for index in range(look_back, len(is_above_data)):
        #     evaluator.signals.append(1 if is_above_data[index - look_back] == 1 else 0)

        # evaluator.title = (
        #     f"{above_values_detailed_title} was above {below_values_detailed_title}"
        # )

        # return await store_evaluator_data(maker, evaluator, allow_signal_extension=True)
