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
import tentacles.Meta.Keywords.indicator_keywords.crossing.crossing_up_down as crossing_up_down
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities
import tentacles.Meta.Keywords.block_factory.abstract_evaluator_block as abstract_evaluator_block
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums


class DataIsCrossingEvaluator(abstract_evaluator_block.EvaluatorBlock):
    NAME = "data_is_crossing_data"
    TITLE = "Data is Crossing Data"
    TITLE_SHORT = TITLE
    DESCRIPTION = (
        "Data is crossing can be used to get signals "
        "when two data source groups are crossing each other"
    )

    crossing_delay: int
    max_crossing: float
    max_crossing_lookback: int
    crossing_direction: str

    def init_block_settings(self) -> None:
        self.activate_single_input_data_node(
            data_source_name="crossing values",
            def_val="price_data",
            enable_static_value=False,
        )
        self.activate_multiple_input_data_nodes(
            data_source_name="values to cross",
            def_val=["EMA"],
            indicator_group_id=2,
        )
        crossing_options = ["crossing up", "crossing down"]
        self.crossing_direction = self.user_input(
            "crossing direction",
            "options",
            "crossing up",
            options=crossing_options,
            grid_columns=12,
        )
        self.crossing_delay = self.user_input("crossing signal delay", "int", 0)
        self.max_crossing_lookback = self.user_input(
            "history length for maximum dump/pump (0 = disabled)",
            "int",
            0,
            0,
            grid_columns=12,
        )
        self.max_crossing = 0
        if int(self.max_crossing_lookback) != 0:
            self.max_crossing = self.user_input(
                "maximum % dump/pump before cross up/down (0 = disabled)",
                "float",
                0,
                grid_columns=12,
            )
        self.max_crossing = (
            None
            if int(self.max_crossing_lookback) == 0 or int(self.max_crossing) == 0
            else str(self.max_crossing) + "%"
        )
        # max_crossing_count = 50
        # max_crossing_count_lookback = self.user_input(
        #     "history length for nearby signals (0 = disabled)",
        #     "int",
        #     0,
        #     0,
        #     grid_columns=12,
        # )
        # if int(max_crossing_count_lookback) != 0:
        #     max_crossing_count = self.user_input(
        #         "maximum nearby signals", "int", 1, min_val=1, grid_columns=12
        #     )
        #     max_crossing_count = (
        #         max_crossing_count if int(max_crossing_count) != 0 else 50
        #     )

        # max_crossing_count_lookback = (
        #     max_crossing_count_lookback if max_crossing_count_lookback != 0 else 1
        # )
        self.register_evaluator_data_output(
            title="Crossing Signals",
            plot_switch_text="Plot crossing signals",
            plot_color_switch_title="Signals plot color",
            default_plot_color=block_factory_enums.Colors.PURPLE,
        )

    async def execute_block(
        self,
    ) -> None:
        # execute get_input_node_data and get_multi_input_node_data
        # in the same order as in init_block_settings above
        (
            data_crossing_values,
            chart_location,
            crossing_values_title,
        ) = await self.get_input_node_data()
        values_to_cross_indicators_data = await self.get_multi_input_node_data()

        all_values_to_cross = []
        indicator_titles: list = []
        for indicator_data, _, indicator_title in values_to_cross_indicators_data:
            all_values_to_cross.append(indicator_data)
            indicator_titles.append(indicator_title)
        title = (
            f"{crossing_values_title} is {self.crossing_direction} {indicator_titles}"
        )
        all_values_to_cross = utilities.cut_data_to_same_len(
            all_values_to_cross, get_list=True
        )
        stacked_values_to_cross = numpy.dstack(all_values_to_cross)
        values = None
        signals = None
        if self.crossing_direction == "crossing up":
            values = stacked_values_to_cross.max(axis=2)[0]
            signals = await crossing_up_down.crossing_up_(
                maker=self,
                values_to_cross=values,
                crossing_values=data_crossing_values,
                delay=self.crossing_delay,
                max_cross_down=self.max_crossing,
                max_cross_down_lookback=self.max_crossing_lookback,
                max_history=not self.block_factory.live_recording_mode,
            )

        elif self.crossing_direction == "crossing down":
            values = stacked_values_to_cross.min(axis=2)[0]
            signals = await crossing_up_down.crossing_down_(
                maker=self,
                values_to_cross=values,
                crossing_values=data_crossing_values,
                delay=self.crossing_delay,
                max_cross_up=self.max_crossing,
                max_cross_up_lookback=self.max_crossing_lookback,
                max_history=not self.block_factory.live_recording_mode,
            )
        else:  # crossing up or down
            values = values_to_cross_indicators_data[0][0]
            signals = await crossing_up_down.crossing_(
                maker=self,
                values_to_cross=values,
                crossing_values=data_crossing_values,
                delay=self.crossing_delay,
                max_cross=self.max_crossing,
                max_cross_lookback=self.max_crossing_lookback,
                max_history=not self.block_factory.live_recording_mode,
            )
        await self.store_evaluator_signals(
            title=title,
            signals=signals,
            signal_values=values,
            chart_location=chart_location,
            allow_signal_extension=True,
        )
