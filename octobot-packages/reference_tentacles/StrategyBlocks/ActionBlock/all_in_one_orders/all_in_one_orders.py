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

import numpy
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords import matrix_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    ENTRY,
    TAG_SEPERATOR,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.expired_orders_cancelling import (
    cancel_expired_orders_for_this_candle,
)
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.activate_managed_order as activate_managed_order

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.settings.entry_types import ManagedOrderSettingsEntryTypes
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)
import tentacles.Meta.Keywords.block_factory as _block_factory
import typing
import tentacles.Meta.Keywords.block_factory.abstract_entry_order_block as abstract_entry_order_block

from tentacles.StrategyBlocks.ActionBlock.all_in_one_orders.all_in_one_order_settings.all_settings import (
    ManagedOrdersSettings,
)
from tentacles.StrategyBlocks.ActionBlock.all_in_one_orders.all_in_one_order_settings.order_settings_group import (
    ManagedOrderSettingsOrderGroup,
)
from tentacles.StrategyBlocks.ActionBlock.all_in_one_orders.all_in_one_order_settings.sl_settings import (
    ManagedOrderSettingsSLTypes,
)
from tentacles.StrategyBlocks.ActionBlock.all_in_one_orders.all_in_one_order_settings.tp_settings import (
    ManagedOrderSettingsTPTypes,
)


class AllInOneOrders(abstract_entry_order_block.EntryOrderBlock):
    NAME = "all_in_one_orders"
    TITLE = "All In One Orders"
    TITLE_SHORT = TITLE
    DESCRIPTION = (
        "A versatile block combining market/limit order entries, stop losses, take profits based on percentages, and dynamic risk management. "
        "Simplify trading strategies with single-block functionality for comprehensive position management and risk control."
    )

    managed_order_settings = None

    def init_block_settings(self) -> None:
        parent_input_name: str = self.node_parent_input
        order_tag_prefix: str = self.node_parent_input
        name_prefix: str = self.node_parent_input
        enable_position_size_settings: bool = True
        enable_stop_loss_settings: bool = True
        enable_trailing_stop_settings: bool = False
        enable_take_profit_settings: bool = True
        enable_ping_pong: bool = self.block_factory.current_nodes["mode_node"][
            "config_mode_node"
        ].get("enable_ping_pong")
        try:
            self.managed_order_settings: ManagedOrdersSettings = ManagedOrdersSettings()
            self.managed_order_settings.initialize(
                order_block=self,
                parent_user_input_name=parent_input_name,
                order_tag_prefix=order_tag_prefix,
                unique_name_prefix=name_prefix,
                enable_position_size_settings=enable_position_size_settings,
                enable_trailing_stop_settings=enable_trailing_stop_settings,
                enable_stop_loss_settings=enable_stop_loss_settings,
                enable_take_profit_settings=enable_take_profit_settings,
                enable_ping_pong=enable_ping_pong,
            )
        except Exception as error:
            raise RuntimeError(
                "Managed Order: There is an issue in your Managed Order "
                "configuration. Check the settings: " + str(error)
            ) from error

    async def init_block_data(
        self,
    ) -> None:
        await self.load_indicators()

    async def load_indicators(self):
        times = None
        for order_group in self.managed_order_settings.order_groups.values():
            if (
                order_group.stop_loss.sl_type
                == ManagedOrderSettingsSLTypes.BASED_ON_INDICATOR_DESCRIPTION
            ):
                (
                    data_source_values,
                    _,
                    _,
                ) = await self.get_input_node_data()
                times = times or await self.get_candles(
                    matrix_enums.PriceDataSources.TIME.value
                )
                cutted_times, cutted_data_source_values = cut_data_to_same_len(
                    (times, data_source_values)
                )
                cutted_int_times = numpy.array(cutted_times).astype(int)
                order_group.stop_loss.indicator_times = cutted_int_times
                order_group.stop_loss.indicator_values = cutted_data_source_values
            if (
                order_group.take_profit.tp_type
                == ManagedOrderSettingsTPTypes.SINGLE_INDICATOR_DESCRIPTION
            ):
                (
                    data_source_values,
                    _,
                    _,
                ) = await self.get_input_node_data()
                times = times or await self.get_candles(
                    matrix_enums.PriceDataSources.TIME.value
                )
                cutted_times, cutted_data_source_values = cut_data_to_same_len(
                    (times, data_source_values)
                )
                cutted_int_times = numpy.array(cutted_times).astype(int)
                order_group.take_profit.indicator_times = cutted_int_times
                order_group.take_profit.indicator_values = cutted_data_source_values
            if (
                order_group.entry.entry_type
                == ManagedOrderSettingsEntryTypes.SCALED_INDICATOR_DESCRIPTION
            ):
                for grid in order_group.entry.entry_grids.values():
                    (
                        data_source_values,
                        _,
                        _,
                    ) = await self.get_input_node_data()
                    times = times or await self.get_candles(
                        matrix_enums.PriceDataSources.TIME.value
                    )
                    cutted_times, cutted_data_source_values = cut_data_to_same_len(
                        (times, data_source_values)
                    )
                    cutted_int_times = numpy.array(cutted_times).astype(int)
                    grid.from_indicator_times = cutted_int_times
                    grid.from_indicator_values = cutted_data_source_values
                    (
                        data_source_values,
                        _,
                        _,
                    ) = await self.get_input_node_data()
                    cutted_times, cutted_data_source_values = cut_data_to_same_len(
                        (times, data_source_values)
                    )
                    cutted_int_times = numpy.array(cutted_times).astype(int)
                    grid.to_indicator_times = cutted_int_times
                    grid.to_indicator_values = cutted_data_source_values

    def get_indicator_value(self, order_group_sl_or_tp):
        try:
            data_index = numpy.where(
                order_group_sl_or_tp.indicator_times
                == float(self.block_factory.ctx.trigger_value[0])
            )[0][0]
            return decimal.Decimal(
                str(order_group_sl_or_tp.indicator_values[data_index])
            )
        except Exception:
            raise RuntimeError(
                "Failed to get indicator value for all in one order block"
            )

    async def execute_block(
        self,
    ) -> None:
        await activate_managed_order.managed_order(
            self.block_factory,
            order_block=self,
            trading_side=self.managed_order_settings.trading_side,
            orders_settings=self.managed_order_settings,
        )

    async def execute_cron_jobs(
        self,
        block_factory,
        triggering_block: typing.Optional[_block_factory.AbstractBlock] = None,
    ):
        for order_group in self.managed_order_settings.order_groups.values():
            order_group: ManagedOrderSettingsOrderGroup
            if order_group.entry.enable_expired_limit_cancel:
                await cancel_expired_orders_for_this_candle(
                    block_factory.ctx,
                    limit_max_age_in_bars=order_group.entry.limit_max_age_in_bars,
                    symbol=block_factory.ctx.symbol,
                    time_frame=block_factory.ctx.time_frame,
                    tag=ENTRY + TAG_SEPERATOR + order_group.order_tag_prefix,
                )
