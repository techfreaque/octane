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
import re
import functools

import octobot_commons


# pylint: disable=R0902
class Symbol:
    FULL_SYMBOL_GROUPS_REGEX = r"([^//]*)\/([^:]*):?([^-]*)-?([^-]*)-?([^-]*)-?([^-]*)"
    #                             base   /  quote : settlement-identifier-strike price-type
    # Inspired from CCXT https://docs.ccxt.com/en/latest/manual.html#option:
    # //
    # // base asset or currency
    # // ↓
    # // ↓  quote asset or currency
    # // ↓  ↓
    # // ↓  ↓    settlement asset or currency
    # // ↓  ↓    ↓
    # // ↓  ↓    ↓       identifier (settlement date)
    # // ↓  ↓    ↓       ↓
    # // ↓  ↓    ↓       ↓   strike price
    # // ↓  ↓    ↓       ↓   ↓
    # // ↓  ↓    ↓       ↓   ↓   type, put (P) or call (C)
    # // ↓  ↓    ↓       ↓   ↓   ↓
    # 'BTC/USDT:BTC-211225-60000-P'  // BTC/USDT put option contract strike price 60000 USDT settled in BTC (inverse)
    # on 2021-12-25
    # 'ETH/USDT:USDT-211225-40000-C' // BTC/USDT call option contract strike price 40000 USDT settled in USDT (linear,
    # vanilla) on 2021-12-25
    # 'ETH/USDT:ETH-210625-5000-P'   // ETH/USDT put option contract strike price 5000 USDT settled in ETH (inverse)
    # on 2021-06-25
    # 'ETH/USDT:USDT-210625-5000-C'  // ETH/USDT call option contract strike price 5000 USDT settled in USDT (linear,
    # vanilla) on 2021-06-25

    def __init__(
        self,
        symbol_str,
        market_separator=octobot_commons.MARKET_SEPARATOR,
        settlement_separator=octobot_commons.SETTLEMENT_ASSET_SEPARATOR,
    ):
        self.symbol_str = symbol_str
        self.base = None
        self.quote = None
        self.settlement_asset = None
        self.identifier = None
        self.strike_price = None
        self.option_type = None
        self.market_separator = market_separator
        self.settlement_separator = settlement_separator
        self.parse_symbol(self.symbol_str)

    def parse_symbol(self, symbol_str):
        """
        Parse the specified symbol
        :param symbol_str: the symbol to parse
        """
        if self.settlement_separator in symbol_str:
            (
                self.base,
                self.quote,
                self.settlement_asset,
                self.identifier,
                self.strike_price,
                self.option_type,
            ) = _parse_symbol_full(self.FULL_SYMBOL_GROUPS_REGEX, symbol_str)
        else:
            # simple (probably spot) pair, use str.split as it is much faster
            self.base, self.quote = _parse_spot_symbol(
                self.market_separator, symbol_str
            )
            self.settlement_asset = (
                self.identifier
            ) = self.strike_price = self.option_type = ""

    def base_and_quote(self):
        """
        return a tuple made of this symbol's base and quote assets
        """
        return self.base, self.quote

    def merged_str_symbol(
        self,
        market_separator=octobot_commons.MARKET_SEPARATOR,
        settlement_separator=octobot_commons.SETTLEMENT_ASSET_SEPARATOR,
    ):
        """
        return the base/quote representation of this symbol. includes settlement asset if set
        """
        if self.settlement_asset:
            return f"{self.base}{market_separator}{self.quote}{settlement_separator}{self.settlement_asset}"
        return f"{self.base}{market_separator}{self.quote}"

    def merged_str_base_and_quote_only_symbol(
        self,
        market_separator=octobot_commons.MARKET_SEPARATOR,
    ):
        """
        return the base/quote representation of this symbol. includes settlement asset if set
        """
        return f"{self.base}{market_separator}{self.quote}"

    def is_perpetual_future(self):
        """
        return True when this symbol is related to a perpetual future contract
        """
        return self.settlement_asset and not (
            self.identifier or self.strike_price or self.option_type
        )

    def is_spot(self):
        """
        return True when this symbol is related to a spot asset
        """
        return self.base and self.quote and not self.settlement_asset

    def is_future(self):
        """
        return True when this symbol is related to a non-perpetual future contract
        """
        return bool(
            self.settlement_asset and not (self.strike_price or self.option_type)
        )

    def is_option(self):
        """
        return True when this symbol is related to an option contract
        """
        return bool(
            self.settlement_asset
            and self.identifier
            and self.strike_price
            and self.option_type
        )

    def is_linear(self):
        """
        return True when this symbol is related to a linear contract based on the settlement_asset
        """
        return self.quote == self.settlement_asset if self.settlement_asset else True

    def is_inverse(self):
        """
        return True when this symbol is related to an inverse contract based on the settlement_asset
        """
        return self.base == self.settlement_asset if self.settlement_asset else False

    def is_same_base_and_quote(self, other):
        """*
        :return: True if the given symbol has the same base and quote as self
        """
        return self.base == other.base and self.quote == other.quote

    def __eq__(self, other):
        return self is other or (
            isinstance(other, Symbol)
            and self.symbol_str == other.symbol_str
            and self.base == other.base
            and self.quote == other.quote
            and self.settlement_asset == other.settlement_asset
            and self.identifier == other.identifier
            and self.strike_price == other.strike_price
            and self.option_type == other.option_type
        )

    def __str__(self):
        return self.symbol_str


@functools.lru_cache(maxsize=None)
def _parse_symbol_full(full_symbol_regex, symbol_str):
    return re.search(full_symbol_regex, symbol_str).groups()


@functools.lru_cache(maxsize=None)
def _parse_spot_symbol(separator, symbol_str):
    return symbol_str.split(separator)
