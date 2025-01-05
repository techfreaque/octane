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

from octobot_commons.enums import UserInputEditorOptionsTypes, UserInputTypes
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block
import tentacles.Meta.Keywords.indicator_keywords.pivots_lib.multi_pivots_lib as multi_pivots_lib


class UnbrokenHighsAndLowsIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "unbroken_highs_and_lows"
    TITLE = "Unbroken Highs and lows"
    TITLE_SHORT = "Unbroken Highs and lows"
    DESCRIPTION = "Unbroken Highs and lows can be used to detect unbroken pivot highs and lows from a data source"
    candle_source: str
    pivots_len: int
    confirmation: int
    min_pivot_age: int
    max_pivot_lookback: int
    pivot_low_active: bool
    pivot_high_active: bool

    def init_block_settings(self) -> None:
        # TODO get pivot_lookback from calling evaluator
        # self.pivot_lookback = (
        #     evaluator.pivot_lookback if hasattr(evaluator, "pivot_lookback") else None
        # ) or self.user_input("pivot lookback length", "int", 2, 1)

        self.pivots_len = self.user_input(
            "pivots_len",
            title="Pivots length",
            input_type=UserInputTypes.INT,
            def_val=100,
            min_val=1,
        )
        self.confirmation = self.user_input(
            "confirmation",
            title="Breaking confirmation time",
            input_type=UserInputTypes.INT,
            def_val=0,
            min_val=1,
        )
        self.min_pivot_age = self.user_input(
            "min_pivot_age",
            title="Min pivot age",
            input_type=UserInputTypes.INT,
            def_val=0,
            min_val=1,
        )
        self.max_pivot_lookback = self.user_input(
            "max_pivot_lookback",
            title="Max pivot lookback",
            input_type=UserInputTypes.INT,
            def_val=3000,
            min_val=1,
        )

        pivot_lows_settings_name = "pivot_low_settings"
        self.user_input(
            pivot_lows_settings_name,
            def_val=None,
            title="Pivot Lows",
            input_type=UserInputTypes.OBJECT,
            editor_options={
                UserInputEditorOptionsTypes.COLLAPSED.value: True,
                UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
                UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
            show_in_optimizer=False,
            show_in_summary=False,
        )

        self.pivot_low_active = self.user_input(
            "Activate pivot lows",
            def_val=True,
            input_type=UserInputTypes.BOOLEAN,
            show_in_summary=False,
            parent_input_name_new=pivot_lows_settings_name,
        )
        if self.pivot_low_active:
            self.activate_single_input_data_node(
                data_source_name="Pivot lows data source",
                def_val="price_data",
                parent_input_name=pivot_lows_settings_name,
            )
            self.register_indicator_data_output(
                title="Pivot lows",
                plot_switch_text="Plot pivot lows",
                plot_color_switch_title="Pivot lows plot color",
                default_plot_color=block_factory_enums.Colors.PURPLE,
                parent_input_name=pivot_lows_settings_name,
            )

        pivot_high_settings_name = "pivot_high_settings"
        self.user_input(
            pivot_high_settings_name,
            def_val=None,
            title="Pivot Highs",
            input_type=UserInputTypes.OBJECT,
            editor_options={
                UserInputEditorOptionsTypes.COLLAPSED.value: True,
                UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
                UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
            show_in_optimizer=False,
            show_in_summary=False,
        )

        self.pivot_high_active = self.user_input(
            "Activate pivot highs",
            def_val=True,
            input_type=UserInputTypes.BOOLEAN,
            show_in_summary=False,
            parent_input_name_new=pivot_high_settings_name,
        )
        if self.pivot_high_active:
            self.activate_single_input_data_node(
                data_source_name="Pivots highs data source",
                def_val="price_data",
                parent_input_name=pivot_high_settings_name,
            )
            self.register_indicator_data_output(
                title="Pivot highs",
                plot_switch_text="Plot pivot highs",
                plot_color_switch_title="Pivot highs plot color",
                default_plot_color=block_factory_enums.Colors.GREEN,
                parent_input_name=pivot_high_settings_name,
            )

    async def execute_block(
        self,
    ) -> None:
        if self.pivot_low_active:
            (
                lows_data,
                lows_conditions,
                lows_additional_payload_data,
                chart_location,
                pivots_title_lows,
            ) = await self.get_input_node_data(get_additional_node_data=True)
            pivot_lookback = lows_additional_payload_data.get("pivot_lookback")
            if not pivot_lookback:
                raise Exception(
                    "Pivot lookback not found , make sure highs and lows indicator is connected"
                )
            (
                history_pivot_lows_data,
                history_pivot_price_list,
            ) = multi_pivots_lib.unbroken_pivot_lows(
                lows_conditions,
                lows_additional_payload_data["low_data_source_values"],
                pivots_len=self.pivots_len,
                confirmation=self.confirmation,
                min_pivot_age=self.min_pivot_age,
                max_pivot_lookback=self.max_pivot_lookback,
                pivot_lookback=pivot_lookback,
            )
            await self.store_indicator_data(
                title=f"Unbroken  {pivots_title_lows}",
                data=history_pivot_price_list,
                additional_payload_data={
                    "low_data_source_values": lows_additional_payload_data[
                        "low_data_source_values"
                    ]
                },
                chart_location=chart_location,
                mode="markers",
            )
        if self.pivot_high_active:
            (
                highs_data,
                highs_conditions,
                highs_additional_payload_data,
                _,
                pivots_title_highs,
            ) = await self.get_input_node_data(get_additional_node_data=True)
            pivot_lookback = highs_additional_payload_data.get("pivot_lookback")
            if not pivot_lookback:
                raise Exception(
                    "Pivot lookback not found , make sure highs and lows indicator is connected"
                )
            (
                history_pivot_highs_data,
                history_pivot_price_list,
            ) = multi_pivots_lib.unbroken_pivot_highs(
                highs_conditions,
                highs_additional_payload_data["high_data_source_values"],
                pivots_len=self.pivots_len,
                confirmation=self.confirmation,
                min_pivot_age=self.min_pivot_age,
                max_pivot_lookback=self.max_pivot_lookback,
                pivot_lookback=pivot_lookback,
            )
            await self.store_indicator_data(
                title=f"Unbroken {pivots_title_highs}",
                data=history_pivot_price_list,
                additional_payload_data={
                    "high_data_source_values": highs_additional_payload_data[
                        "high_data_source_values"
                    ]
                },
                chart_location=chart_location,
                mode="markers",
            )
