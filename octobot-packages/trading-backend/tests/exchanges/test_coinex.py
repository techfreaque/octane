#  Drakkar-Software trading-backend
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
import pytest
import ccxt.async_support
import trading_backend.exchanges as exchanges
import tests.util.create_order_tests as create_order_tests
from tests import coinex_exchange


def test_get_name(coinex_exchange):
    assert exchanges.Coinex(coinex_exchange).get_name() == ccxt.async_support.coinex().id.lower()


@pytest.mark.asyncio
async def test_get_orders_parameters(coinex_exchange):
    exchange = exchanges.Coinex(coinex_exchange)
    await create_order_tests.create_order_mocked_test_args(
        exchange,
        exchange_private_post_order_method_name="v1PrivatePostOrderLimit",
        exchange_request_referral_key="client_id",
        should_contains=True)


@pytest.mark.asyncio
async def test_sign(coinex_exchange):
    exchange = exchanges.Coinex(coinex_exchange)
    await create_order_tests.sign_test(
        exchange,
        ['v1', 'private'],
        "client_id",
        should_contains=True,
        in_body=True,
        url_path="order/limit"
    )
