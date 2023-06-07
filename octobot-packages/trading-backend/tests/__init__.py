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


@pytest.fixture
def binance_exchange():
    return ExchangeWrapper(ccxt.async_support.binance())


@pytest.fixture
def okx_exchange():
    return ExchangeWrapper(ccxt.async_support.okx())


@pytest.fixture
def huobi_exchange():
    return ExchangeWrapper(ccxt.async_support.huobi())


@pytest.fixture
def huobipro_exchange():
    return ExchangeWrapper(ccxt.async_support.huobipro())


@pytest.fixture
def ftx_exchange():
    return ExchangeWrapper(ccxt.async_support.ftx())


@pytest.fixture
def ascendex_exchange():
    return ExchangeWrapper(ccxt.async_support.ascendex())


@pytest.fixture
def bybit_exchange():
    return ExchangeWrapper(ccxt.async_support.bybit())


@pytest.fixture
def gateio_exchange():
    return ExchangeWrapper(ccxt.async_support.gateio())


@pytest.fixture
def bybit_exchange():
    return ExchangeWrapper(ccxt.async_support.bybit())


@pytest.fixture
def bitget_exchange():
    return ExchangeWrapper(ccxt.async_support.bitget())


@pytest.fixture
def phemex_exchange():
    return ExchangeWrapper(ccxt.async_support.phemex())


@pytest.fixture
def default_exchange():
    """
    :return: An exchange for which there is no exchange implementation in trading_backend.exchanges
    """
    return ExchangeWrapper(ccxt.async_support.okex())


class ExchangeConnector:
    def __init__(self, ccxt_exchange):
        self.client = ccxt_exchange

    def add_headers(self, headers_dict):
        for header_key, header_value in headers_dict.items():
            self.client.headers[header_key] = header_value


class ExchangeManager:
    def __init__(self, is_margin=False, is_future=False):
        self.is_future = is_future
        self.is_margin = is_margin


class ExchangeWrapper:
    def __init__(self, ccxt_exchange, is_margin=False, is_future=False):
        self.connector = ExchangeConnector(ccxt_exchange)
        self.exchange_manager = ExchangeManager(is_margin=is_margin, is_future=is_future)

    def _get_params(self, params):
        return params
