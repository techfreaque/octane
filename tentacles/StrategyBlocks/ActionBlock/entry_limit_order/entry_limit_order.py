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
import octobot_trading.enums as trading_enums

import tentacles.Meta.Keywords.block_factory.abstract_entry_order_block as abstract_entry_order_block
from tentacles.Meta.Keywords.scripting_library.orders import order_types


class EntryLimitOrder(abstract_entry_order_block.EntryOrderBlock):
    NAME = "limit_order"
    TITLE = "Entry Limit Order"
    TITLE_SHORT = TITLE
    DESCRIPTION = "Place a single limit order"

    crossing_delay: int
    max_crossing: float
    max_crossing_lookback: int
    limit_offset: decimal.Decimal
    enable_expired_limit_cancel: bool
    limit_max_age_in_bars: int
    trading_side: str

    def init_block_settings(self) -> None:
        self.trading_side = self.user_input(
            "trading_side",
            commons_enums.UserInputTypes.OPTIONS.value,
            trading_enums.TradeOrderSide.BUY.value,
            title="Trading Side",
            options=[
                trading_enums.TradeOrderSide.BUY.value,
                trading_enums.TradeOrderSide.SELL.value,
            ],
        )
        self.limit_offset = decimal.Decimal(
            str(
                self.user_input(
                    "limit_entry_offset_in_%",
                    "float",
                    0.2,
                    title="limit entry offset in %",
                    min_val=0,
                )
            )
        )
        # self.enable_expired_limit_cancel = self.user_input(
        #     "enable_expired_limit_cancel",
        #     "boolean",
        #     True,
        #     title="Enable order cancellation after X bars",
        # )
        # if self.enable_expired_limit_cancel:
        #     self.limit_max_age_in_bars = self.user_input(
        #         "limit_max_age_in_bars",
        #         "int",
        #         3,
        #         title="Maximum bars to fill until the order(s) get canceled",
        #         min_val=0,
        #     )

        self.register_take_profit_orders_input()
        self.register_stop_orders_input()
        self.register_order_filled_output()

    async def execute_block(
        self,
    ) -> None:
        created_orders = await order_types.market(
            self.block_factory.ctx,
            side=self.trading_side,
            amount=100,
            # tag=self.entry_order_tag,
            # stop_loss_offset=bundled_sl_offset,
            # stop_loss_tag=bundled_sl_tag,
            # stop_loss_group=bundled_sl_group,
            # take_profit_offset=bundled_tp_offset,
            # take_profit_tag=bundled_tp_tag,
            # take_profit_group=bundled_tp_group,
        )
