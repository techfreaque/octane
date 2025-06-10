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

from __future__ import annotations
import decimal

import octobot_commons.enums as commons_enums


from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.settings.entry_settings import (
    ManagedOrderEntryGrid,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.settings.entry_types import ManagedOrderSettingsEntryTypes
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.scaled_orders as scaled_orders
import tentacles.StrategyBlocks.ActionBlock.all_in_one_orders.all_in_one_order_settings.sl_settings as sl_settings
import tentacles.StrategyBlocks.ActionBlock.all_in_one_orders.all_in_one_order_settings.tp_settings as tp_settings
import tentacles.StrategyBlocks.ActionBlock.all_in_one_orders as all_in_one_orders


class ManagedOrderSettingsEntry:
    take_profit: tp_settings.ManagedOrderSettingsTP = tp_settings.ManagedOrderSettingsTP
    stop_loss: sl_settings.ManagedOrderSettingsSL = sl_settings.ManagedOrderSettingsSL

    entry_type: str = None
    limit_offset: float = None
    slippage_limit: float = None
    market_in_if_limit_fails: bool = None

    entry_scaled_min: float = None
    entry_scaled_max: float = None
    entry_scaled_order_count: int = None
    scaled_entry_price_distribution_type: str = None
    scaled_entry_price_growth_factor: float = None
    scaled_entry_value_distribution_type: str = None
    scaled_entry_value_growth_factor: float = None
    entry_scaled_min: float = None
    entry_scaled_max: float = None

    limit_max_age_in_bars: int = None
    enable_expired_limit_cancel: bool = None

    entry_multi_grid_mode: bool = None
    amount_of_entry_grids: int = None
    entry_grids: dict[str, ManagedOrderEntryGrid] = None

    def __init__(self):
        pass

    def initialize_entry_settings(
        self,
        order_block: all_in_one_orders.AllInOneOrders,
        parent_user_input_name: str,
        managed_order_group_id: str,
    ):
        _entry_setting_name = "entry_settings"
        entry_setting_name = f"{_entry_setting_name}_{managed_order_group_id}"
        order_block.user_input(
            _entry_setting_name,
            "object",
            title="Entry settings",
            def_val=None,
            parent_input_name=parent_user_input_name,
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
                commons_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
        )

        # entry type
        self.entry_type = order_block.user_input(
            "entry_type",
            "options",
            ManagedOrderSettingsEntryTypes.SINGLE_MARKET_IN_DESCRIPTION,
            title="entry type",
            options=ManagedOrderSettingsEntryTypes.DESCRIPTIONS,
            parent_input_name=entry_setting_name,
        )
        # entry: limit in
        if (
            self.entry_type
            == ManagedOrderSettingsEntryTypes.SINGLE_LIMIT_IN_DESCRIPTION
        ):
            self.limit_offset = decimal.Decimal(
                str(
                    order_block.user_input(
                        "limit_entry_offset_in_%",
                        "float",
                        0.2,
                        title="limit entry offset in %",
                        min_val=0,
                        parent_input_name=entry_setting_name,
                    )
                )
            )
            self._limit_order_expiration_user_input(order_block, entry_setting_name)

        # entry: try limit in
        elif (
            self.entry_type
            == ManagedOrderSettingsEntryTypes.SINGLE_TRY_LIMIT_IN_DESCRIPTION
        ):
            self.slippage_limit = decimal.Decimal(
                str(
                    order_block.user_input(
                        "slippage_limit",
                        "float",
                        40,
                        title="Slippage Limit: can be % or price",
                        parent_input_name=entry_setting_name,
                    )
                )
            )
            self.market_in_if_limit_fails = order_block.user_input(
                "try_to_limit_in",
                "boolean",
                True,
                title="try to limit in",
                parent_input_name=entry_setting_name,
            )
            self._limit_order_expiration_user_input(order_block, entry_setting_name)
            # self.entry_scaled_order_count = await basic_keywords.user_input(
            #     ctx,
            #     "amount of entry orders",
            #     "int",
            #     10,
            #     min_val=2,
            #  #   path=self.entry_path,
            #     parent_input_name=group_user_input_name_prefix,
            # )

        elif (
            self.entry_type
            == ManagedOrderSettingsEntryTypes.SCALED_STATIC_DESCRIPTION
            or self.entry_type
            == ManagedOrderSettingsEntryTypes.SCALED_DYNAMIC_DESCRIPTION
            or self.entry_type
            == ManagedOrderSettingsEntryTypes.SCALED_INDICATOR_DESCRIPTION
        ):
            self._scaled_orders_user_input(
                order_block, entry_setting_name, managed_order_group_id
            )

    def _scaled_orders_user_input(
        self,
        order_block: all_in_one_orders.AllInOneOrders,
        entry_setting_name: str,
        managed_order_group_id: str,
    ):
        grid_type_name = ManagedOrderSettingsEntryTypes.DESCRIPTIONS_TO_KEY[
            self.entry_type
        ]

        self.entry_multi_grid_mode = order_block.user_input(
            f"entry_{grid_type_name}_multi_grid_mode",
            "boolean",
            False,
            title="Use multiple grids",
            parent_input_name=entry_setting_name,
        )
        if self.entry_multi_grid_mode:
            self.amount_of_entry_grids = order_block.user_input(
                f"amount_of_{grid_type_name}_entry_grids",
                "int",
                2,
                title="How many grids?",
                min_val=1,
                parent_input_name=entry_setting_name,
            )
        else:
            self.amount_of_entry_grids = 1
        self._limit_order_expiration_user_input(order_block, entry_setting_name)
        self.entry_grids = {}
        for grid_id in range(1, self.amount_of_entry_grids + 1):
            _grid_name = f"{grid_type_name}_entry_grid_{grid_id}"
            grid_name = f"{_grid_name}_{managed_order_group_id}"
            grid_suffix = f"g{grid_id}"
            title = f"Grid {grid_id}"
            order_block.user_input(
                _grid_name,
                "object",
                None,
                title=title,
                parent_input_name=entry_setting_name,
                editor_options={
                    commons_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True
                },
            )
            parent_input_name = grid_name
            if self.amount_of_entry_grids != 1:
                value_percent = decimal.Decimal(
                    str(
                        order_block.user_input(
                            f"{grid_suffix}_position_size_percent",
                            "float",
                            50,
                            min_val=0,
                            max_val=100,
                            title="Percent of total position value to use for this grid",
                            parent_input_name=parent_input_name,
                        )
                    )
                )
            else:
                value_percent = 100

            order_count = order_block.user_input(
                f"{grid_suffix}_amount_of_orders",
                "int",
                10,
                title="amount of orders",
                min_val=2,
                parent_input_name=parent_input_name,
            )

            (
                price_distribution_type,
                price_growth_factor,
            ) = self._price_distribution_settings(
                order_block, grid_suffix, parent_input_name
            )
            (
                value_distribution_type,
                value_growth_factor,
            ) = self._value_distribution_settings(
                order_block, grid_suffix, parent_input_name
            )

            from_level, to_level = self._scale_from_to_settings(
                order_block, grid_id, grid_suffix, parent_input_name
            )
            self.entry_grids[grid_id] = ManagedOrderEntryGrid(
                grid_id=grid_id,
                price_distribution_type=price_distribution_type,
                price_growth_factor=price_growth_factor,
                order_count=order_count,
                value_distribution_type=value_distribution_type,
                value_growth_factor=value_growth_factor,
                from_level=from_level,
                to_level=to_level,
                value_percent=value_percent,
            )

    def _scale_from_to_settings(
        self,
        order_block: all_in_one_orders.AllInOneOrders,
        grid_id: str,
        grid_suffix: str,
        parent_input_name: str,
    ) -> tuple[str | None, str | None]:
        # from_to_settings = f"{grid_suffix}_scale_from_to_config"
        # order_block.user_input(
        #     from_to_settings,
        #     "object",
        #     None,
        #     title="Scale from / to",
        #     parent_input_name=parent_input_name,
        #     editor_options={
        #         commons_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True
        #     },
        # )
        from_level: str | None = None
        to_level: str | None = None
        if (
            self.entry_type
            == ManagedOrderSettingsEntryTypes.SCALED_DYNAMIC_DESCRIPTION
        ):
            from_level = decimal.Decimal(
                str(
                    order_block.user_input(
                        f"{grid_suffix}_scale_limit_orders_from",
                        "float",
                        1,
                        title="scale limit orders from: (measured in %) ",
                        min_val=-100,
                        max_val=100,
                        parent_input_name=parent_input_name,
                    )
                )
            )
            to_level = decimal.Decimal(
                str(
                    order_block.user_input(
                        f"{grid_suffix}_scale_limit_orders_to",
                        "float",
                        2,
                        title="scale limit orders to: (measured in %)",
                        min_val=-100,
                        max_val=100,
                        parent_input_name=parent_input_name,
                    )
                )
            )
        elif (
            self.entry_type
            == ManagedOrderSettingsEntryTypes.SCALED_STATIC_DESCRIPTION
        ):
            from_level = decimal.Decimal(
                str(
                    order_block.user_input(
                        f"{grid_suffix}_from_price",
                        "float",
                        0.1,
                        title="Scale limit orders from price",
                        min_val=0,
                        parent_input_name=parent_input_name,
                    )
                )
            )
            to_level = decimal.Decimal(
                str(
                    order_block.user_input(
                        f"{grid_suffix}_to_price",
                        "float",
                        0.2,
                        title="Scale limit orders to price",
                        min_val=0,
                        parent_input_name=parent_input_name,
                    )
                )
            )
        elif (
            self.entry_type
            == ManagedOrderSettingsEntryTypes.SCALED_INDICATOR_DESCRIPTION
        ):
            order_block.activate_single_input_data_node(
                data_source_name=f"Grid {grid_id} Scale From",
                def_val="price_data",
                parent_input_name=parent_input_name,
            )
            order_block.activate_single_input_data_node(
                data_source_name=f"Grid {grid_id} Scale To",
                def_val="price_data",
                parent_input_name=parent_input_name,
            )
        return from_level, to_level

    def _value_distribution_settings(
        self,
        order_block: all_in_one_orders.AllInOneOrders,
        grid_suffix: str,
        parent_input_name: str,
    ):
        # value_distribution_settings = f"{grid_suffix}_value_distribution_config"
        # order_block.user_input(
        #     value_distribution_settings,
        #     "object",
        #     None,
        #     title="Value distribution",
        #     parent_input_name=parent_input_name,
        #     editor_options={
        #         commons_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True
        #     },
        # )

        value_distribution_type = order_block.user_input(
            f"{grid_suffix}_value_distribution_type",
            "options",
            scaled_orders.ScaledOrderValueDistributionTypes.LINEAR_GROWTH,
            title="Value distribution type",
            options=scaled_orders.ScaledOrderValueDistributionTypes.all_types,
            parent_input_name=parent_input_name,
        )
        value_growth_factor = None
        if value_distribution_type in (
            scaled_orders.ScaledOrderValueDistributionTypes.LINEAR_GROWTH,
            scaled_orders.ScaledOrderValueDistributionTypes.EXPONENTIAL,
        ):
            value_growth_factor = decimal.Decimal(
                str(
                    order_block.user_input(
                        f"{grid_suffix}_value_growth_rate",
                        "float",
                        2,
                        title="Value scaling growth rate",
                        min_val=0.0000001,
                        max_val=100,
                        parent_input_name=parent_input_name,
                    )
                )
            )
        return value_distribution_type, value_growth_factor

    def _price_distribution_settings(
        self,
        order_block: all_in_one_orders.AllInOneOrders,
        grid_suffix: str,
        parent_input_name: str,
    ):
        # price_distribution_settings = f"{grid_suffix}_price_distribution_config"
        # order_block.user_input(
        #     price_distribution_settings,
        #     "object",
        #     None,
        #     title="Price distribution",
        #     parent_input_name=parent_input_name,
        #     editor_options={
        #         commons_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True
        #     },
        # )

        price_distribution_type = order_block.user_input(
            f"{grid_suffix}_price_distribution_type",
            "options",
            scaled_orders.ScaledOrderPriceDistributionTypes.LINEAR_GROWTH,
            title="Grid price distribution type",
            options=scaled_orders.ScaledOrderPriceDistributionTypes.all_types,
            parent_input_name=parent_input_name,
        )
        price_growth_factor = None
        if price_distribution_type in (
            scaled_orders.ScaledOrderPriceDistributionTypes.LINEAR_GROWTH,
            scaled_orders.ScaledOrderPriceDistributionTypes.EXPONENTIAL,
        ):
            price_growth_factor = decimal.Decimal(
                str(
                    order_block.user_input(
                        f"{grid_suffix}_price_growth_rate",
                        "float",
                        2,
                        title="Price scaling growth rate",
                        min_val=0.0000001,
                        max_val=100,
                        parent_input_name=parent_input_name,
                    )
                )
            )
        return price_distribution_type, price_growth_factor

    def _limit_order_expiration_user_input(
        self, order_block: all_in_one_orders.AllInOneOrders, entry_setting_name: str
    ):
        self.enable_expired_limit_cancel = bool(
            order_block.user_input(
                "enable_expired_limit_cancel",
                "boolean",
                True,
                title="Enable order cancellation after X bars",
                parent_input_name=entry_setting_name,
            )
        )
        if self.enable_expired_limit_cancel:
            self.limit_max_age_in_bars = int(
                order_block.user_input(
                    "limit_max_age_in_bars",
                    "int",
                    3,
                    title="Maximum bars to fill until the order(s) get canceled",
                    min_val=0,
                    parent_input_name=entry_setting_name,
                )
            )
