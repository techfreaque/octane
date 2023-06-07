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
import mock
import ccxt

import trading_backend.exchanges as exchanges
import trading_backend.errors
from tests import default_exchange


def test_get_name(default_exchange):
    assert exchanges.Exchange(default_exchange).get_name() == exchanges.Exchange.get_name()


def test_get_orders_parameters(default_exchange):
    assert exchanges.Exchange(default_exchange).get_orders_parameters({"a": 1}) == {"a": 1}


@pytest.mark.asyncio
async def test_is_valid_account(default_exchange):
    exchange = exchanges.Exchange(default_exchange)
    with mock.patch.object(exchange._exchange.connector.client, "fetch_balance",
                           mock.AsyncMock(return_value=None)) as fetch_balance_mock:
        assert await exchange.is_valid_account() == (True, None)
        fetch_balance_mock.assert_called_once()
    with mock.patch.object(exchange._exchange.connector.client, "fetch_balance",
                           mock.AsyncMock(side_effect=ccxt.AuthenticationError)) as fetch_balance_mock:
        with pytest.raises(trading_backend.errors.ExchangeAuthError):
            assert await exchange.is_valid_account() == (True, None)
        fetch_balance_mock.assert_called_once()
    with mock.patch.object(exchange._exchange.connector.client, "fetch_balance",
                           mock.AsyncMock(side_effect=ccxt.InvalidNonce)) as fetch_balance_mock:
        with pytest.raises(trading_backend.errors.TimeSyncError):
            assert await exchange.is_valid_account() == (True, None)
        fetch_balance_mock.assert_called_once()


@pytest.mark.asyncio
async def test_initialize(default_exchange):
    exchange = exchanges.Exchange(default_exchange)
    init_result = await exchange.initialize()
    assert exchange.get_name().capitalize() in init_result
    assert "Broker" not in init_result


@pytest.mark.asyncio
async def test_ensure_broker_status(default_exchange):
    init_result = await exchanges.Exchange(default_exchange)._ensure_broker_status()
    assert "Broker" in init_result
    assert "enabled" in init_result
