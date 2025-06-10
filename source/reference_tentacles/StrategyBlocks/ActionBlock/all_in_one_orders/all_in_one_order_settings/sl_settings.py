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

import decimal
import octobot_commons.enums as commons_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.settings.sl_settings import (
    ManagedOrderSettingsSLTypes,
)


class ManagedOrderSettingsSLTrailTypes:
    DONT_TRAIL = "dont_trail"
    BREAK_EVEN = "break_even"
    TRAILING = "trailing"
    TRAILING_INDICATOR = "trailing_indicator"

    DONT_TRAIL_DESCRIPTION = "dont move the stop loss"
    BREAK_EVEN_DESCRIPTION = "move stop loss to break even"
    TRAILING_DESCRIPTION = "trailing stop loss based on sl settings"
    TRAILING_INDICATOR_DESCRIPTION = "trailing stop loss based on indicator"

    KEY_TO_DESCRIPTIONS = {
        DONT_TRAIL: DONT_TRAIL_DESCRIPTION,
        BREAK_EVEN: BREAK_EVEN_DESCRIPTION,
        TRAILING: TRAILING_DESCRIPTION,
        TRAILING_INDICATOR: TRAILING_INDICATOR_DESCRIPTION,
    }
    DESCRIPTIONS = [
        DONT_TRAIL_DESCRIPTION,
        BREAK_EVEN_DESCRIPTION,
        TRAILING_DESCRIPTION,
        TRAILING_INDICATOR_DESCRIPTION,
    ]


class ManagedOrderSettingsSL:
    indicator_times = None
    indicator_values = None

    def __init__(self) -> None:
        super().__init__()

        self.sl_type: str = None
        self.use_bundled_sl_orders: bool = None
        self.sl_low_high_lookback: int = None
        self.sl_low_high_buffer: float = None
        self.sl_min_p: float = None
        self.sl_max_p: float = None
        self.sl_in_p_value: float = None
        self.sl_price: float = None
        self.sl_min_p: float = None
        self.sl_max_p: float = None
        self.atr_period: int = None
        self.sl_min_p: float = None
        self.sl_trail_type: str = None
        self.sl_trail_start_only_in_profit: bool = None
        self.sl_trail_start: float = None
        self.sl_trail_start_only_if_above_entry: bool = None
        self.sl_trailing_min_p: float = None
        self.sl_trailing_max_p: float = None

        self.sl_indicator_id: int = None
        self.trailing_indicator_id: int = None

    def initialize_sl_settings(
        self,
        order_block,
        parent_user_input_name: str,
        managed_order_group_id: str,
        managed_order_group_id_number: str,
        enable_trailing_stop_settings: bool = False,
        enable_stop_loss_settings: bool = False,
    ):
        self.use_bundled_sl_orders = True  # await basic_keywords.user_input(
        #     maker.ctx,
        #     "Bundle stop order with entry order",
        #     "boolean",
        #     False,
        #
        #     parent_input_name=sl_setting_name,
        #     other_schema_values={
        #         "description": "When this option is enabled the SL will only get "
        #         "placed once the entry got filled (OctoBot must be running). "
        #         "Only on bybit futures it will already place the SL with the entry "
        #         "and OctoBot doesnt need to run for the SL"
        #     },
        #     show_in_optimizer=False,
        #     show_in_summary=False,
        # )
        if not enable_stop_loss_settings:
            self.sl_type = ManagedOrderSettingsSLTypes.NO_SL_DESCRIPTION
            return

        _sl_setting_name = "sl_settings"
        sl_setting_name = f"{_sl_setting_name}_{managed_order_group_id}"
        _sl_trailing_setting_name = "sl_trailing_settings"
        sl_trailing_setting_name = (
            f"{_sl_trailing_setting_name}_{managed_order_group_id}"
        )
        order_block.user_input(
            _sl_setting_name,
            "object",
            title="Stop loss settings",
            def_val=None,
            parent_input_name=parent_user_input_name,
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
                commons_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
        )

        if self.use_bundled_sl_orders:
            available_types = ManagedOrderSettingsSLTypes.DESCRIPTIONS
            default_type = (
                ManagedOrderSettingsSLTypes.BASED_ON_PERCENT_ENTRY_DESCRIPTION
            )
        else:
            available_types = [
                ManagedOrderSettingsSLTypes.NO_SL_DESCRIPTION,
                ManagedOrderSettingsSLTypes.AT_LOW_HIGH_DESCRIPTION,
                ManagedOrderSettingsSLTypes.BASED_ON_STATIC_PRICE_DESCRIPTION,
                ManagedOrderSettingsSLTypes.BASED_ON_ATR_DESCRIPTION,
                ManagedOrderSettingsSLTypes.BASED_ON_INDICATOR_DESCRIPTION,
            ]
            default_type = ManagedOrderSettingsSLTypes.NO_SL_DESCRIPTION

        self.sl_type = order_block.user_input(
            "sl_type",
            "options",
            def_val=default_type,
            options=available_types,
            title="SL type",
            parent_input_name=sl_setting_name,
        )

        if self.sl_type == ManagedOrderSettingsSLTypes.NO_SL_DESCRIPTION:
            self.sl_trail_type = ManagedOrderSettingsSLTrailTypes.DONT_TRAIL_DESCRIPTION
        else:
            # SL based on low/high
            if self.sl_type == ManagedOrderSettingsSLTypes.AT_LOW_HIGH_DESCRIPTION:
                self.sl_low_high_lookback = order_block.user_input(
                    "sl_at_low_high_lookback_period",
                    "int",
                    3,
                    title="SL at low/high lookback period",
                    parent_input_name=sl_setting_name,
                )
                self.sl_low_high_buffer = decimal.Decimal(
                    str(
                        order_block.user_input(
                            "sl_at_low_high_buffer_in_%",
                            "float",
                            0.2,
                            title="SL at low/high buffer in %",
                            parent_input_name=sl_setting_name,
                        )
                    )
                )
                self.sl_min_p = decimal.Decimal(
                    str(
                        order_block.user_input(
                            "min_sl_in_%",
                            "float",
                            0.1,
                            min_val=0,
                            title="min SL in %",
                            parent_input_name=sl_setting_name,
                        )
                    )
                )
                self.sl_max_p = decimal.Decimal(
                    str(
                        order_block.user_input(
                            "max_sl_in_%",
                            "float",
                            1,
                            min_val=0,
                            title="max SL in %",
                            parent_input_name=sl_setting_name,
                        )
                    )
                )

            # sl based on percent
            elif self.sl_type in (
                ManagedOrderSettingsSLTypes.BASED_ON_PERCENT_ENTRY_DESCRIPTION,
                ManagedOrderSettingsSLTypes.BASED_ON_PERCENT_PRICE_DESCRIPTION,
            ):
                self.sl_in_p_value = decimal.Decimal(
                    str(
                        order_block.user_input(
                            "sl_in_%",
                            "float",
                            0.5,
                            min_val=0,
                            title="SL in %",
                            parent_input_name=sl_setting_name,
                        )
                    )
                )

            # sl based on static price
            elif (
                self.sl_type
                == ManagedOrderSettingsSLTypes.BASED_ON_STATIC_PRICE_DESCRIPTION
            ):
                self.sl_price = decimal.Decimal(
                    str(
                        order_block.user_input(
                            "sl_based_on_static_price",
                            "float",
                            0,
                            min_val=0,
                            title="SL based on static price",
                            parent_input_name=sl_setting_name,
                        )
                    )
                )

            # sl based on indicator
            elif (
                self.sl_type
                == ManagedOrderSettingsSLTypes.BASED_ON_INDICATOR_DESCRIPTION
            ):
                order_block.activate_single_input_data_node(
                    data_source_name=f"Group {managed_order_group_id_number} SL",
                    def_val="price_data",
                )
                self.sl_min_p = decimal.Decimal(
                    str(
                        order_block.user_input(
                            "min_sl_in_%",
                            "float",
                            0.1,
                            min_val=0,
                            title="min SL in %",
                            parent_input_name=sl_setting_name,
                        )
                    )
                )
                self.sl_max_p = decimal.Decimal(
                    str(
                        order_block.user_input(
                            "max_sl_in_%",
                            "float",
                            1,
                            min_val=0,
                            title="max SL in %",
                            parent_input_name=sl_setting_name,
                        )
                    )
                )

            # SL based on atr
            elif self.sl_type == ManagedOrderSettingsSLTypes.BASED_ON_ATR_DESCRIPTION:
                self.atr_period = order_block.user_input(
                    "atr_period",
                    "int",
                    4,
                    title="ATR Period",
                    parent_input_name=sl_setting_name,
                )
                self.sl_min_p = decimal.Decimal(
                    str(
                        order_block.user_input(
                            "min_sl_in_%",
                            "float",
                            0.1,
                            min_val=0,
                            title="min SL in %",
                            parent_input_name=sl_setting_name,
                        )
                    )
                )
                self.sl_max_p = decimal.Decimal(
                    str(
                        order_block.user_input(
                            "max_sl_in_%",
                            "float",
                            1,
                            min_val=0,
                            title="max SL in %",
                            parent_input_name=sl_setting_name,
                        )
                    )
                )

            if enable_trailing_stop_settings:
                # trailing SL
                order_block.user_input(
                    _sl_trailing_setting_name,
                    "object",
                    title="Trailing stop loss settings",
                    def_val=None,
                    parent_input_name=parent_user_input_name,
                    editor_options={
                        commons_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
                        commons_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
                        commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
                    },
                )
                self.sl_trail_type = order_block.user_input(
                    "sl_trailing_type",
                    "options",
                    ManagedOrderSettingsSLTrailTypes.DONT_TRAIL_DESCRIPTION,
                    options=ManagedOrderSettingsSLTrailTypes.DESCRIPTIONS,
                    title="SL trailing type",
                    parent_input_name=sl_trailing_setting_name,
                )
                if (
                    self.sl_trail_type
                    == ManagedOrderSettingsSLTrailTypes.BREAK_EVEN_DESCRIPTION
                ):
                    self.sl_trail_start_only_in_profit = True
                    self.sl_trail_start = decimal.Decimal(
                        str(
                            order_block.user_input(
                                "move_stop_loss_to_break_even_when_price_moves_x%_into_profit",
                                "float",
                                0.5,
                                min_val=0,
                                title="move stop loss to break even when price moves x% into profit",
                                parent_input_name=sl_trailing_setting_name,
                            )
                        )
                    )
                    self.sl_trail_start_only_if_above_entry = False
                elif (
                    self.sl_trail_type
                    == ManagedOrderSettingsSLTrailTypes.TRAILING_DESCRIPTION
                ):
                    self.sl_trail_start_only_in_profit = order_block.user_input(
                        "start_stop_loss_trailing_only_when_price_moves_into_profit",
                        "boolean",
                        True,
                        title="start stop loss trailing only when price moves into profit",
                        parent_input_name=sl_trailing_setting_name,
                    )
                    if self.sl_trail_start_only_in_profit:
                        self.sl_trail_start = decimal.Decimal(
                            str(
                                order_block.user_input(
                                    "start_trailing_the_SL_when_price_moves_x%_into_profit",
                                    "float",
                                    0.5,
                                    min_val=0,
                                    title="start trailing the SL when price moves x% into profit",
                                    parent_input_name=sl_trailing_setting_name,
                                )
                            )
                        )
                    self.sl_trail_start_only_if_above_entry = order_block.user_input(
                        "start_trailing_only_if_SL_would_be_above_the_entry",
                        "boolean",
                        True,
                        title="Start trailing only if SL would be above the entry",
                        parent_input_name=sl_trailing_setting_name,
                    )

                elif (
                    self.sl_trail_type
                    == ManagedOrderSettingsSLTrailTypes.TRAILING_INDICATOR_DESCRIPTION
                ):
                    self.trailing_indicator_id = managed_order_group_id + 200

                    standalone_data_sources.activate_standalone_data_source(
                        "Trailing stop loss indicator",
                        parent_input_name=sl_trailing_setting_name,
                        indicator_id=self.trailing_indicator_id,
                        maker=maker,
                    )
                    self.sl_trail_start_only_in_profit = order_block.user_input(
                        "start_stop_loss_trailing_only_when_price_moves_into_profit",
                        "boolean",
                        True,
                        title="start stop loss trailing only when price moves into profit",
                        parent_input_name=sl_trailing_setting_name,
                    )
                    if self.sl_trail_start_only_in_profit:
                        self.sl_trail_start = decimal.Decimal(
                            str(
                                order_block.user_input(
                                    "start_trailing_the_SL_when_price_moves_x%_into_profit",
                                    "float",
                                    0.5,
                                    min_val=0,
                                    title="start trailing the SL when price moves x% into profit",
                                    parent_input_name=sl_trailing_setting_name,
                                )
                            )
                        )
                    self.sl_trailing_min_p = decimal.Decimal(
                        str(
                            order_block.user_input(
                                "min_trailing_SL_in_%",
                                "float",
                                0.1,
                                min_val=0,
                                title="min trailing SL in %",
                                parent_input_name=sl_trailing_setting_name,
                            )
                        )
                    )
                    self.sl_trailing_max_p = decimal.Decimal(
                        str(
                            order_block.user_input(
                                "max_trailing_SL_in_%",
                                "float",
                                1,
                                min_val=0,
                                title="max trailing SL in %",
                                parent_input_name=sl_trailing_setting_name,
                            )
                        )
                    )
                    self.sl_trail_start_only_if_above_entry = order_block.user_input(
                        "start_trailing_only_if_sl_would_be_above_the_entry",
                        "boolean",
                        True,
                        title="Start trailing only if SL would be above the entry",
                        parent_input_name=sl_trailing_setting_name,
                    )
            else:
                self.sl_trail_type = (
                    ManagedOrderSettingsSLTrailTypes.DONT_TRAIL_DESCRIPTION
                )
