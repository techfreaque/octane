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


def get_supported_price_indicators():
    return [
        "ATR Low",
        "ATR High",
        "EMA",
        "fib_line",
        "fib_line 0",
        "fib_line 1",
        "fib_line long",
        "fib_line short",
        "fib_line ema",
        "HMA",
        "DEMA",
        "ichimoku conversion line",
        "ichimoku base line",
        "ichimoku leading span b",
        "ichimoku leading span a",
        "keltner channel base",
        "SSL_channel Up",
        "SSL_channel Down",
        "keltner channel low",
        "keltner channel high",
        "PSAR",
        "TEMA",
        "SMA",
        "ALMA",
        "supertrend",
        "VWAP",
        "VWMA",
        "Bollinger Band High",
        "Bollinger Band Middle",
        "Bollinger Band Low",
        "halftrend",
        "heikin_ashi",
        "candle_average",
        "special_highs",
        "special_lows",
        "break_up",
        "break_up2",
        "break_down2",
        "break_down",
        "ZLEMA",
        "WMA",
        "williams_R",
        "ultimate_oscillator",
        "unbroken_pivots",
        "magic_trend",
    ]


def get_supported_multi_data_indicators():
    return ["unbroken_pivots", "pivots"]


def get_supported_oscillators():
    return [
        "ADX",
        "exchange_delta",
        "accumulation_distribution_oscillator",
        "awesome_oscillator",
        "CCI",
        "EV_MACD",
        "EV_MACD signal",
        "MACD",
        "MACD signal",
        "MACD histogram",
        "MFI",
        "OBV",
        "RSI",
        "stochastic oscillator d",
        "stochastic oscillator k",
        "stochastic_RSI k",
        "stochastic_RSI d",
        "VW_MACD",
        "VW_MACD signal",
        "growth rate",
        "growth rate MA",
        "vector_absolute_value",
        "accumulation_distribution_line",
        "vector_addition",
        "average_directional_movement_rating",
        "absolute_price_oscillator",
        "Aroon UP",
        "Aroon Down",
        "Aroon_oscillator",
        "balance_of_power",
        "chande_momentum_oscillator",
        "candle_range",
    ]


def get_supported_indicator_config(indicator_meta):
    indicator_meta.indicator_class_name = indicator_meta.indicator_name
    if "MACD" in indicator_meta.indicator_name:
        if indicator_meta.indicator_name == "EV_MACD signal":
            indicator_meta.value_key = "s"
            indicator_meta.indicator_class_name = "EV_MACD"
        elif indicator_meta.indicator_name == "VW_MACD signal":
            indicator_meta.value_key = "s"
            indicator_meta.indicator_class_name = "VW_MACD"
        elif indicator_meta.indicator_name == "MACD signal":
            indicator_meta.value_key = "s"
            indicator_meta.indicator_class_name = "MACD"
        elif indicator_meta.indicator_name == "MACD histogram":
            indicator_meta.value_key = "h"
            indicator_meta.indicator_class_name = "MACD"
    elif "stochastic_RSI" in indicator_meta.indicator_name:
        if indicator_meta.indicator_name == "stochastic_RSI d":
            indicator_meta.value_key = "d"
        indicator_meta.indicator_class_name = "stochastic_RSI"
    elif "Bollinger Band" in indicator_meta.indicator_name:
        if indicator_meta.indicator_name == "Bollinger Band Middle":
            indicator_meta.value_key = "m"
        elif indicator_meta.indicator_name == "Bollinger Band Low":
            indicator_meta.value_key = "l"
        indicator_meta.indicator_class_name = "bollinger_bands"
    elif "Aroon " in indicator_meta.indicator_name:
        if indicator_meta.indicator_name == "Aroon UP":
            indicator_meta.value_key = "u"
        indicator_meta.indicator_class_name = "Aroon"
    elif "ichimoku" in indicator_meta.indicator_name:
        if indicator_meta.indicator_name == "ichimoku base line":
            indicator_meta.value_key = "b"
        elif indicator_meta.indicator_name == "ichimoku leading span b":
            indicator_meta.value_key = "lsb"
        elif indicator_meta.indicator_name == "ichimoku leading span a":
            indicator_meta.value_key = "lsa"
        indicator_meta.indicator_class_name = "ichimoku"
    elif "stochastic oscillator" in indicator_meta.indicator_name:
        if indicator_meta.indicator_name == "stochastic oscillator d":
            indicator_meta.value_key = "d"
        indicator_meta.indicator_class_name = "stochastic_oscillator"
    elif "keltner channel" in indicator_meta.indicator_name:
        if indicator_meta.indicator_name == "keltner channel low":
            indicator_meta.value_key = "l"
        elif indicator_meta.indicator_name == "keltner channel high":
            indicator_meta.value_key = "h"
        indicator_meta.indicator_class_name = "keltner_channel"
    elif "growth rate" in indicator_meta.indicator_name:
        if indicator_meta.indicator_name == "growth rate MA":
            indicator_meta.value_key = "ma"
        indicator_meta.indicator_class_name = "growth_rate"
    elif "SSL_channel" in indicator_meta.indicator_name:
        if indicator_meta.indicator_name == "SSL_channel Up":
            indicator_meta.value_key = "up"
        indicator_meta.indicator_class_name = "SSL_channel"
    elif "ATR" in indicator_meta.indicator_name:
        if indicator_meta.indicator_name == "ATR High":
            indicator_meta.value_key = "h"
        indicator_meta.indicator_class_name = "ATR"
    elif "fib_line" in indicator_meta.indicator_name:
        if indicator_meta.indicator_name == "fib_line ema":
            indicator_meta.value_key = "e"
            indicator_meta.indicator_class_name = "fib_line"
        elif indicator_meta.indicator_name == "fib_line 0":
            indicator_meta.value_key = "0"
            indicator_meta.indicator_class_name = "fib_line"
        elif indicator_meta.indicator_name == "fib_line 1":
            indicator_meta.value_key = "1"
            indicator_meta.indicator_class_name = "fib_line"
        elif indicator_meta.indicator_name == "fib_line long":
            indicator_meta.value_key = "l"
            indicator_meta.indicator_class_name = "fib_line"
        elif indicator_meta.indicator_name == "fib_line short":
            indicator_meta.value_key = "s"
            indicator_meta.indicator_class_name = "fib_line"
    return indicator_meta


def get_supported_indicators_(
    enable_oscillators=True,
    enable_price_indicators=True,
    enable_static_value=True,
    enable_price_data=True,
    enable_multi_data_indicators=False,
):
    available_sources = []
    indicator_sources = []
    if enable_price_data:
        available_sources.append("price_data")
    if enable_static_value:
        available_sources.append("static_value")
    if enable_oscillators:
        indicator_sources += get_supported_oscillators()
    if enable_multi_data_indicators:
        indicator_sources += get_supported_multi_data_indicators()
    if enable_price_indicators:
        indicator_sources += get_supported_price_indicators()
    return sorted(available_sources + indicator_sources, key=str.casefold)
