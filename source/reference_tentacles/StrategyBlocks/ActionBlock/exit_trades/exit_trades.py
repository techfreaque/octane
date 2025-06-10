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
from tentacles.Meta.Keywords.scripting_library.orders.order_types import market_order

CLOSE_LONG_TRADE = "Close Long Trade"
CLOSE_SHORT_TRADE = "Close Short Trade"

ENTRY_ORDER = "Entry orders"
STOP_LOSS_ORDER = "Stop loss orders"
TAKE_PROFIT_ORDER = "Take profit orders"


class ExitTradesAction(abstract_exit_order_block.ExitSignalsOrderBlock):
    NAME = "exit_trades"
    TITLE = "Exit Trades"
    TITLE_SHORT = TITLE
    DESCRIPTION = "This block can be used to exit trades based on signals"
    exit_side: str

    def init_block_settings(self) -> None:
        self.exit_side = self.user_input(
            "exit_side",
            commons_enums.UserInputTypes.OPTIONS.value,
            CLOSE_LONG_TRADE,
            title="Exit Side",
            options=[
                CLOSE_LONG_TRADE,
                CLOSE_SHORT_TRADE,
            ],
        )

    async def execute_block(
        self,
    ) -> None:
        if self.exit_side == CLOSE_LONG_TRADE:
            await exit_long_trade(self.block_factory.ctx)
        else:
            await exit_short_trade(self.block_factory.ctx)


async def exit_short_trade(ctx: context_management.Context):
    await market_order.market(ctx, side="buy", amount="100a%", reduce_only=True)


async def exit_long_trade(ctx: context_management.Context):
    await market_order.market(ctx, side="sell", amount="100a%", reduce_only=True)
