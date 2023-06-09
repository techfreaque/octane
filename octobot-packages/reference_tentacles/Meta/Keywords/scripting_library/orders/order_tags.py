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


def get_tagged_orders(
    ctx, tag, symbol=None, since: int or float = -1, until: int or float = -1, contains_tag=True
):
    return ctx.exchange_manager.exchange_personal_data.orders_manager.get_open_orders(
        symbol=symbol, tag=tag, since=since, until=until, contains_tag=contains_tag,
    )
