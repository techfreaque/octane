#  Drakkar-Software OctoBot-Commons
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

import octobot_commons.symbols


@pytest.fixture
def spot_symbol():
    return octobot_commons.symbols.Symbol("BTC/USDT")


@pytest.fixture
def perpetual_future_symbol():
    return octobot_commons.symbols.Symbol("BTC/USDT:BTC")


@pytest.fixture
def future_symbol():
    return octobot_commons.symbols.Symbol("ETH/USDT:USDT-210625")


@pytest.fixture
def option_symbol():
    return octobot_commons.symbols.Symbol("ETH/USDT:USDT-211225-40000-C")


def test_parse_spot_symbol(spot_symbol):
    assert spot_symbol.base == "BTC"
    assert spot_symbol.quote == "USDT"
    assert spot_symbol.settlement_asset == spot_symbol.identifier == spot_symbol.strike_price \
           == spot_symbol.option_type == ""


def test_parse_perpetual_future_symbol(perpetual_future_symbol):
    assert perpetual_future_symbol.base == "BTC"
    assert perpetual_future_symbol.quote == "USDT"
    assert perpetual_future_symbol.settlement_asset == "BTC"
    assert perpetual_future_symbol.strike_price == perpetual_future_symbol.option_type == ""


def test_parse_future_symbol(future_symbol):
    assert future_symbol.base == "ETH"
    assert future_symbol.quote == "USDT"
    assert future_symbol.settlement_asset == "USDT"
    assert future_symbol.identifier == "210625"
    assert future_symbol.strike_price == future_symbol.option_type == ""


def test_parse_option_symbol(option_symbol):
    assert option_symbol.base == "ETH"
    assert option_symbol.quote == "USDT"
    assert option_symbol.settlement_asset == "USDT"
    assert option_symbol.identifier == "211225"
    assert option_symbol.strike_price == "40000"
    assert option_symbol.option_type == "C"


def test_base_and_quote(spot_symbol, option_symbol):
    assert spot_symbol.base_and_quote() == ("BTC", "USDT")
    assert option_symbol.base_and_quote() == ("ETH", "USDT")


def test_is_linear(spot_symbol, perpetual_future_symbol,  option_symbol):
    assert spot_symbol.is_linear() is True
    assert perpetual_future_symbol.is_linear() is False
    assert option_symbol.is_linear() is True


def test_is_inverse(spot_symbol, perpetual_future_symbol, option_symbol):
    assert spot_symbol.is_inverse() is False
    assert perpetual_future_symbol.is_inverse() is True
    assert option_symbol.is_inverse() is False


def test__eq__(spot_symbol, option_symbol):
    assert spot_symbol == octobot_commons.symbols.Symbol("BTC/USDT")
    assert spot_symbol != octobot_commons.symbols.Symbol("BTC/USD")
    assert spot_symbol != option_symbol
    assert option_symbol == octobot_commons.symbols.Symbol("ETH/USDT:USDT-211225-40000-C")
    assert option_symbol != octobot_commons.symbols.Symbol("ETH/USDT:USDT-211225-40000-P")
