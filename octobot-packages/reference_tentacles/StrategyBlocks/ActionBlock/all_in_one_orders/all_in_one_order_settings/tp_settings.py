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
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.settings.entry_types import ManagedOrderSettingsEntryTypes
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.settings.sl_settings import ManagedOrderSettingsSLTypes
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.settings.tp_settings import ManagedOrderSettingsTPTypes



class ManagedOrderSettingsTP:
    indicator_times = None
    indicator_values = None

    def __init__(self) -> None:
        self.tp_type: str = None
        self.tp_rr: decimal.Decimal = None
        self.tp_in_p: decimal.Decimal = None
        self.tp_in_d: decimal.Decimal = None
        self.rr_tp_min: decimal.Decimal = None
        self.rr_tp_max: decimal.Decimal = None
        self.rr_tp_order_count: int = None
        self.p_tp_order_count: int = None
        self.p_tp_min: decimal.Decimal = None
        self.p_tp_max: decimal.Decimal = None
        self.tp_min_p: decimal.Decimal = None
        self.tp_max_p: decimal.Decimal = None
        self.position_mode: str = None
        self.use_bundled_tp_orders: bool = None
        self.indicator: None
        self.tp_indicator_id: int = None

    def initialize_tp_settings(
        self,
        order_block,
        entry_type,
        sl_type,
        parent_user_input_name,
        managed_order_group_id: str,
        managed_order_group_id_number: str,
        enable_take_profit_settings: bool = True,
    ):
        if not enable_take_profit_settings:
            self.tp_type = ManagedOrderSettingsSLTypes.NO_SL_DESCRIPTION
            return
        _tp_setting_name = "tp_settings"
        tp_setting_name = f"{_tp_setting_name}_{managed_order_group_id}"
        order_block.user_input(
            _tp_setting_name,
            "object",
            title="Take profit settings",
            def_val=None,
            parent_input_name=parent_user_input_name,
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
                commons_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
        )

        self.use_bundled_tp_orders = True  # await basic_keywords.user_input(
        #     maker.ctx,
        #     "Bundle take profit order with entry order",
        #     "boolean",
        #     False,
        #
        #     parent_input_name=tp_setting_name,
        #     other_schema_values={
        #         "description": "When this option is enabled the TP will only get "
        #         "placed once the entry got filled (OctoBot must be running). "
        #         "Only on bybit futures it will already place the TP with the entry "
        #         "and OctoBot doesnt need to run for the SL"
        #     },
        #     show_in_optimizer=False,
        #     show_in_summary=False,
        # )
        if sl_type == ManagedOrderSettingsSLTypes.NO_SL_DESCRIPTION:
            # self.use_bundled_tp_orders = False
            tp_type_def_val = ManagedOrderSettingsTPTypes.SINGLE_PERCENT_DESCRIPTION
            if self.use_bundled_tp_orders:
                if entry_type in (
                    ManagedOrderSettingsEntryTypes.SINGLE_LIMIT_IN_DESCRIPTION,
                    ManagedOrderSettingsEntryTypes.SINGLE_MARKET_IN_DESCRIPTION,
                ):
                    tp_type_optinions = [
                        ManagedOrderSettingsTPTypes.NO_TP_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_PERCENT_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_STATIC_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_INDICATOR_DESCRIPTION,
                    ]
                else:
                    tp_type_optinions = [
                        ManagedOrderSettingsTPTypes.NO_TP_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_STATIC_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_PERCENT_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_INDICATOR_DESCRIPTION,
                    ]
            else:
                tp_type_optinions = [
                    ManagedOrderSettingsTPTypes.NO_TP_DESCRIPTION,
                    # ManagedOrderSettingsTPTypes.SINGLE_PERCENT_DESCRIPTION,
                    ManagedOrderSettingsTPTypes.SINGLE_STATIC_DESCRIPTION,
                    ManagedOrderSettingsTPTypes.SINGLE_INDICATOR_DESCRIPTION,
                    # ManagedOrderSettingsTPTypes.SCALED_PERCENT_DESCRIPTION,
                    # ManagedOrderSettingsTPTypes.SCALED_STATIC_DESCRIPTION,
                ]
        else:
            tp_type_def_val = ManagedOrderSettingsTPTypes.SINGLE_RISK_REWARD_DESCRIPTION
            if self.use_bundled_tp_orders:
                if entry_type in (
                    ManagedOrderSettingsEntryTypes.SINGLE_LIMIT_IN_DESCRIPTION,
                    ManagedOrderSettingsEntryTypes.SINGLE_MARKET_IN_DESCRIPTION,
                ):
                    tp_type_optinions = [
                        ManagedOrderSettingsTPTypes.NO_TP_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_RISK_REWARD_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_PERCENT_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_STATIC_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_INDICATOR_DESCRIPTION,
                    ]
                else:
                    tp_type_optinions = [
                        ManagedOrderSettingsTPTypes.NO_TP_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_RISK_REWARD_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_PERCENT_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_STATIC_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_INDICATOR_DESCRIPTION,
                    ]
            else:
                if entry_type in (
                    ManagedOrderSettingsEntryTypes.SINGLE_LIMIT_IN_DESCRIPTION,
                    ManagedOrderSettingsEntryTypes.SINGLE_MARKET_IN_DESCRIPTION,
                ):
                    tp_type_optinions = [
                        ManagedOrderSettingsTPTypes.NO_TP_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_RISK_REWARD_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_PERCENT_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_STATIC_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_INDICATOR_DESCRIPTION,
                    ]
                else:
                    tp_type_optinions = [
                        ManagedOrderSettingsTPTypes.NO_TP_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_STATIC_DESCRIPTION,
                        ManagedOrderSettingsTPTypes.SINGLE_INDICATOR_DESCRIPTION,
                    ]
        # TP
        self.tp_type = order_block.user_input(
            "take_profit_type",
            "options",
            tp_type_def_val,
            options=tp_type_optinions,
            title="Take profit type",
            parent_input_name=tp_setting_name,
        )
        # TP based on risk reward
        if self.tp_type == ManagedOrderSettingsTPTypes.SINGLE_RISK_REWARD_DESCRIPTION:
            self.tp_rr = decimal.Decimal(
                str(
                    order_block.user_input(
                        "tp_risk_reward_target",
                        "float",
                        2,
                        min_val=0,
                        title="TP Risk Reward target",
                        parent_input_name=tp_setting_name,
                    )
                )
            )
        # TP based on indicator
        elif self.tp_type == ManagedOrderSettingsTPTypes.SINGLE_INDICATOR_DESCRIPTION:
            order_block.activate_single_input_data_node(
                data_source_name=f"Group {managed_order_group_id_number} TP",
                def_val="price_data",
            )
            self.tp_min_p = decimal.Decimal(
                str(
                    order_block.user_input(
                        "min_tp_in_%",
                        "float",
                        0.5,
                        min_val=0,
                        title="min take profit in %",
                        parent_input_name=tp_setting_name,
                    )
                )
            )
            self.tp_max_p = decimal.Decimal(
                str(
                    order_block.user_input(
                        "max_tp_in_%",
                        "float",
                        10,
                        min_val=0,
                        title="max take profit in %",
                        parent_input_name=tp_setting_name,
                    )
                )
            )

        # TP based on percent
        elif self.tp_type == ManagedOrderSettingsTPTypes.SINGLE_PERCENT_DESCRIPTION:
            self.tp_in_p = decimal.Decimal(
                str(
                    order_block.user_input(
                        "take_profit_in_percent",
                        "float",
                        2,
                        title="Take profit in %",
                        min_val=0,
                        parent_input_name=tp_setting_name,
                    )
                )
            )

        # single TP based on static price
        elif self.tp_type == ManagedOrderSettingsTPTypes.SINGLE_STATIC_DESCRIPTION:
            self.tp_in_d = decimal.Decimal(
                str(
                    order_block.user_input(
                        "take_profit_static_price",
                        "float",
                        None,
                        title="Take profit static price",
                        min_val=0,
                        parent_input_name=tp_setting_name,
                    )
                )
            )

        # scaled TP based on risk reward
        elif (
            self.tp_type == ManagedOrderSettingsTPTypes.SCALED_RISK_REWARD_DESCRIPTION
            and not self.use_bundled_tp_orders
        ):
            self.rr_tp_min = decimal.Decimal(
                str(
                    order_block.user_input(
                        "take_profit_min_risk_reward_target",
                        "float",
                        2,
                        min_val=0,
                        title="take profit min risk reward target",
                        parent_input_name=tp_setting_name,
                    )
                )
            )
            self.rr_tp_max = decimal.Decimal(
                str(
                    order_block.user_input(
                        "take_profit_max_risk_reward_target",
                        "float",
                        10,
                        min_val=0,
                        title="take profit max risk reward target",
                        parent_input_name=tp_setting_name,
                    )
                )
            )
            self.rr_tp_order_count = order_block.user_input(
                "take_profit_order_count",
                "int",
                10,
                min_val=2,
                title="take profit order count",
                parent_input_name=tp_setting_name,
            )

        # scaled TP based on percent
        elif (
            self.tp_type == ManagedOrderSettingsTPTypes.SCALED_PERCENT_DESCRIPTION
            and not self.use_bundled_tp_orders
        ):
            self.p_tp_min = decimal.Decimal(
                str(
                    order_block.user_input(
                        "scale_take_profit_from_%",
                        "float",
                        1,
                        min_val=0,
                        title="scale take profit from: (measured in %) ",
                        parent_input_name=tp_setting_name,
                    )
                )
            )
            self.p_tp_max = decimal.Decimal(
                str(
                    order_block.user_input(
                        "scale_take_profit_to_%",
                        "float",
                        50,
                        min_val=0,
                        title="scale take profit to: (measured in %",
                        parent_input_name=tp_setting_name,
                    )
                )
            )
            self.p_tp_order_count = order_block.user_input(
                "take_profit_order_count",
                "int",
                10,
                min_val=2,
                title="take profit order count",
                parent_input_name=tp_setting_name,
            )

        # grid sell based on percent
        elif (
            self.tp_type == ManagedOrderSettingsTPTypes.SCALED_STATIC_DESCRIPTION
            and not not self.use_bundled_tp_orders
        ):
            self.position_mode = order_block.user_input(
                "position_mode",
                "options",
                "long only",
                options=["long only", "short only", "both"],
                title="Position Mode",
                parent_input_name=tp_setting_name,
                other_schema_values={
                    "description": "When both: it will reach the maximum short "
                    "size at the top of the range, and the max long position at the"
                    " bottom. - "
                    "When short only: it will reach the maximum short size at the"
                    " top of the range, and will be in no position at the top"
                    " bottom. - "
                    "When long only: the max size is reached at the bottom and yo"
                },
            )
            self.p_tp_min = decimal.Decimal(
                str(
                    order_block.user_input(
                        "scale_sell_orders_from_price",
                        "float",
                        1,
                        min_val=0,
                        title="scale sell orders from price",
                        parent_input_name=tp_setting_name,
                    )
                )
            )
            self.p_tp_max = decimal.Decimal(
                str(
                    order_block.user_input(
                        "scale_sell_orders_to_price",
                        "float",
                        50,
                        min_val=0,
                        title="scale sell orders to price",
                        parent_input_name=tp_setting_name,
                    )
                )
            )
            self.p_tp_order_count = order_block.user_input(
                "take_profit_order_count",
                "int",
                10,
                min_val=2,
                title="take profit order count",
                parent_input_name=tp_setting_name,
            )
