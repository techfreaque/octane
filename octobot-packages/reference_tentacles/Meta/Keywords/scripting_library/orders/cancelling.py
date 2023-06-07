#  Drakkar-Software OctoBot-Trading
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import octobot_trading.enums as enums
import octobot_trading.modes.script_keywords.basic_keywords as basic_keywords


async def cancel_orders(
    ctx,
    side: str = None,
    tag: str = None,
    symbol: str = None,
    symbols: list[str] = None,
    cancel_loaded_orders=True,
    since: int or float = -1,
    until: int or float = -1,
    contains_tag=True,
) -> bool:
    symbols = symbols or [symbol] if symbol or symbols else [ctx.symbol]
    orders = None
    orders_canceled = False
    side = None if not side else enums.TradeOrderSide(side)

    for symbol in symbols:
        orders_canceled, orders = await ctx.trader.cancel_open_orders(
            symbol,
            cancel_loaded_orders=cancel_loaded_orders,
            side=side,
            since=since,
            until=until,
            tag=tag,
        )
        if basic_keywords.is_emitting_trading_signals(ctx):
            for order in orders:
                ctx.get_signal_builder().add_cancelled_order(
                    order, ctx.trader.exchange_manager
                )
    return orders_canceled
