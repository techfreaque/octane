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
import octobot_commons.enums as commons_enums
from octobot_trading.enums import TradeOrderSide
from octobot_trading.modes.script_keywords import context_management
from tentacles.Meta.Keywords.block_factory import abstract_exit_order_block
import tentacles.Meta.Keywords.scripting_library.orders.cancelling as cancelling
from tentacles.Meta.Keywords.scripting_library.orders.open_orders import get_open_orders

CANCEL_LONG_ORDERS = "Cancel long orders"
CANCEL_SHORT_ORDERS = "Cancel short orders"


ENTRY_ORDER = "Entry orders"
STOP_LOSS_ORDER = "Stop loss orders"
TAKE_PROFIT_ORDER = "Take profit orders"


class CancelOrdersAction(abstract_exit_order_block.ExitSignalsOrderBlock):
    NAME = "cancel_orders"
    TITLE = "Cancel Orders"
    TITLE_SHORT = TITLE
    DESCRIPTION = "This block can be used to cancel orders based on signals"
    exit_side: str
    order_type: str

    def init_block_settings(self) -> None:
        self.exit_side = self.user_input(
            "exit_side",
            commons_enums.UserInputTypes.OPTIONS.value,
            CANCEL_LONG_ORDERS,
            title="Exit Side",
            options=[
                CANCEL_LONG_ORDERS,
                CANCEL_SHORT_ORDERS,
            ],
        )
        self.order_type = self.user_input(
            "order_type",
            commons_enums.UserInputTypes.MULTIPLE_OPTIONS.value,
            title="Exit Side",
            options=[ENTRY_ORDER, STOP_LOSS_ORDER, TAKE_PROFIT_ORDER],
            def_val=[ENTRY_ORDER, STOP_LOSS_ORDER, TAKE_PROFIT_ORDER],
        )

    async def execute_block(
        self,
    ) -> None:
        if self.exit_side == CANCEL_LONG_ORDERS:
            await self.cancel_long_orders()
        else:
            await self.cancel_short_orders()

    async def cancel_short_orders(self):
        if TAKE_PROFIT_ORDER in self.order_type:
            await cancelling.cancel_orders(
                self.block_factory.ctx,
                side=TradeOrderSide.BUY,
                tag=f"{matrix_enums.TAKE_PROFIT}{matrix_enums.TAG_SEPERATOR}",
            )
        if STOP_LOSS_ORDER in self.order_type:
            await cancelling.cancel_orders(
                self.block_factory.ctx,
                side=TradeOrderSide.BUY,
                tag=f"{matrix_enums.STOP_LOSS}{matrix_enums.TAG_SEPERATOR}",
            )
        if ENTRY_ORDER in self.order_type:
            await cancelling.cancel_orders(
                self.block_factory.ctx,
                side=TradeOrderSide.SELL,
                tag=f"{matrix_enums.ENTRY}{matrix_enums.TAG_SEPERATOR}",
            )

    async def cancel_long_orders(self):
        if TAKE_PROFIT_ORDER in self.order_type:
            await cancelling.cancel_orders(
                self.block_factory.ctx,
                side=TradeOrderSide.SELL,
                tag=f"{matrix_enums.TAKE_PROFIT}{matrix_enums.TAG_SEPERATOR}",
            )
        if STOP_LOSS_ORDER in self.order_type:
            await cancelling.cancel_orders(
                self.block_factory.ctx,
                side=TradeOrderSide.SELL,
                tag=f"{matrix_enums.STOP_LOSS}{matrix_enums.TAG_SEPERATOR}",
            )
        if ENTRY_ORDER in self.order_type:
            await cancelling.cancel_orders(
                self.block_factory.ctx,
                side=TradeOrderSide.BUY,
                tag=f"{matrix_enums.ENTRY}{matrix_enums.TAG_SEPERATOR}",
            )