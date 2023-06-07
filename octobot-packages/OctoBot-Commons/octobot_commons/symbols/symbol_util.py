# pylint: disable=R0913
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
import functools

import octobot_commons
import octobot_commons.symbols.symbol


@functools.lru_cache(maxsize=None)
def parse_symbol(symbol):
    """
    Parse the specified symbol into a Symbol object
    :param symbol: the symbol to parse
    :return: Symbol object
    """
    return octobot_commons.symbols.symbol.Symbol(symbol)


@functools.lru_cache(maxsize=None)
def merge_symbol(symbol):
    """
    Return merged currency and market without /
    :param symbol: the specified symbol
    :return: merged currency and market without /
    """
    return symbol.replace(octobot_commons.MARKET_SEPARATOR, "").replace(
        octobot_commons.SETTLEMENT_ASSET_SEPARATOR, "_"
    )


@functools.lru_cache(maxsize=None)
def merge_currencies(
    currency,
    market,
    settlement_asset=None,
    market_separator=octobot_commons.MARKET_SEPARATOR,
    settlement_separator=octobot_commons.SETTLEMENT_ASSET_SEPARATOR,
):
    """
    Merge currency and market
    :param currency: the base currency
    :param market: the quote currency
    :param settlement_asset: the settlement asset currency (unused for spot trading)
    :param market_separator: the separator between currency and market
    :param settlement_separator: the separator between the pair and reference market
    :return: currency and market merged
    """
    symbol = octobot_commons.symbols.symbol.Symbol(
        f"{currency}{market_separator}{market}", market_separator=market_separator
    )
    if settlement_asset is not None:
        symbol.settlement_asset = settlement_asset
    return symbol.merged_str_symbol(
        market_separator=market_separator,
        settlement_separator=settlement_separator,
    )


@functools.lru_cache(maxsize=None)
def convert_symbol(
    symbol,
    symbol_separator,
    new_symbol_separator=octobot_commons.MARKET_SEPARATOR,
    should_uppercase=False,
    should_lowercase=False,
    base_and_quote_only=False,
):
    """
    Convert symbol according to parameter
    :param symbol: the symbol to convert
    :param symbol_separator: the symbol separator
    :param new_symbol_separator: the new symbol separator
    :param should_uppercase: if it should be concerted to uppercase
    :param should_lowercase: if it should be concerted to lowercase
    :param base_and_quote_only: if it should only contain base and quote from the given symbol
    :return:
    """
    if base_and_quote_only:
        symbol = symbol.split(octobot_commons.SETTLEMENT_ASSET_SEPARATOR)[0]
    if should_uppercase:
        return symbol.replace(symbol_separator, new_symbol_separator).upper()
    if should_lowercase:
        return symbol.replace(symbol_separator, new_symbol_separator).lower()
    return symbol.replace(symbol_separator, new_symbol_separator)
