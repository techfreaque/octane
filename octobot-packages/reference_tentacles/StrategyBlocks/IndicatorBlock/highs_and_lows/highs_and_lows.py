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

from octobot_commons.enums import UserInputEditorOptionsTypes
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block
import tentacles.Meta.Keywords.indicator_keywords.pivots_lib.multi_pivots_lib as multi_pivots_lib


class HighsAndLowsIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "highs_and_lows"
    TITLE = "Highs and lows"
    TITLE_SHORT = "Highs and lows"
    DESCRIPTION = (
        "Highs and lows can be used to detect pivot highs and lows from a data source"
    )
    candle_source: str
    pivot_lookback: int
    pivot_low_active: bool
    pivot_high_active: bool

    def init_block_settings(self) -> None:
        # TODO get pivot_lookback from calling evaluator
        # self.pivot_lookback = (
        #     evaluator.pivot_lookback if hasattr(evaluator, "pivot_lookback") else None
        # ) or self.user_input("pivot lookback length", "int", 2, 1)

        self.pivot_lookback = self.user_input("pivot lookback length", "int", 2, 1)

        pivot_lows_settings_name = "pivot_low_settings"
        self.user_input(
            pivot_lows_settings_name,
            def_val=None,
            title="Pivot Lows",
            input_type="object",
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
            input_type="boolean",
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
                chart_location_title="Pivot lows chart location",
                default_plot_color=block_factory_enums.Colors.PURPLE,
                parent_input_name=pivot_lows_settings_name,
            )

        pivot_high_settings_name = "pivot_high_settings"
        self.user_input(
            pivot_high_settings_name,
            def_val=None,
            title="Pivot Highs",
            input_type="object",
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
            input_type="boolean",
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
                chart_location_title="Pivot highs chart location",
                default_plot_color=block_factory_enums.Colors.GREEN,
                parent_input_name=pivot_high_settings_name,
            )

    async def execute_block(
        self,
    ) -> None:
        if self.pivot_low_active:
            (
                low_data_source_values,
                chart_location,
                low_data_source_title,
            ) = await self.get_input_node_data()
            pivot_low_data = multi_pivots_lib.pivot_lows(
                low_data_source_values, swing_history=self.pivot_lookback
            )
            await self.store_indicator_data(
                title=f"{low_data_source_title} pivot low (lb {self.pivot_lookback})",
                data=low_data_source_values[: -self.pivot_lookback],
                data_display_conditions=pivot_low_data,
                additional_payload_data={
                    "low_data_source_values": low_data_source_values,
                    "pivot_lookback": self.pivot_lookback,
                },
                chart_location=chart_location,
            )
        if self.pivot_high_active:
            (
                high_data_source_values,
                chart_location,
                high_data_source_title,
            ) = await self.get_input_node_data()
            pivot_high_data = multi_pivots_lib.pivot_highs(
                high_data_source_values, swing_history=self.pivot_lookback
            )
            await self.store_indicator_data(
                title=f"{high_data_source_title} pivot high (lb {self.pivot_lookback})",
                data=high_data_source_values[: -self.pivot_lookback],
                additional_payload_data={
                    "high_data_source_values": high_data_source_values,
                    "pivot_lookback": self.pivot_lookback,
                },
                data_display_conditions=pivot_high_data,
            )
