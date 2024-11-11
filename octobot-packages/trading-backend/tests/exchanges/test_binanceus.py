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
import tests.util.account_tests as account_tests
from tests import binanceus_exchange


def test_get_name(binanceus_exchange):
    assert exchanges.BinanceUS(binanceus_exchange).get_name() == ccxt.async_support.binanceus().id.lower()


@pytest.mark.asyncio
async def test_get_orders_parameters(binanceus_exchange):
    exchange = exchanges.BinanceUS(binanceus_exchange)
    assert exchange.get_orders_parameters({}) == {}


@pytest.mark.asyncio
async def test_inner_is_valid_account(binanceus_exchange):
    exchange = exchanges.BinanceUS(binanceus_exchange)
    assert await exchange._inner_is_valid_account() == (False, await exchange._ensure_broker_status())


@pytest.mark.asyncio
async def test_invalid_api_key(binanceus_exchange):
    # _inner_is_valid_account is not implemented on binanceus
    pass


@pytest.mark.asyncio
async def test_invalid_api_key_get_api_key_rights(binanceus_exchange):
    exchange = exchanges.BinanceUS(binanceus_exchange)
    await account_tests.check_invalid_account_keys_rights(exchange)
