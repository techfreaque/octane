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

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)
import tentacles.Meta.Keywords.scripting_library.orders.offsets.offset as offset
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
)


async def crossing_up_(
    maker=None,
    values_to_cross=None,
    crossing_values=None,
    delay=0,
    max_cross_down=None,
    max_cross_down_lookback=5,
    max_history=True,
):
    # true if price just risen over value and stayed there for delay time
    min_candles = max_cross_down_lookback + delay + 1
    crossing_data = []

    if values_to_cross is None:
        raise RuntimeError("crossing_up: you need to provide values_to_cross")
    else:
        if crossing_values is not None:
            length = min([len(values_to_cross), len(crossing_values)])
            values_to_cross = values_to_cross[-length:]
            crossing_values = crossing_values[-length:]
            for candle_id in range(min_candles, length):
                if not max_history:
                    candle_id = length - 1
                condition = False
                was_below = None
                try:
                    was_below = (
                        crossing_values[candle_id - delay - 1]
                        < values_to_cross[candle_id - delay - 1]
                    )
                except IndexError:
                    raise RuntimeError(
                        "crossing_up: not enough values_to_cross, length needs to be same as delay"
                    )

                didnt_cross_to_much = True
                if max_cross_down:
                    try:
                        didnt_cross_to_much = min(
                            values_to_cross[
                                candle_id - max_cross_down_lookback : candle_id - delay
                            ]
                        ) - float(
                            await offset.get_offset(maker.ctx, "-" + max_cross_down)
                        ) < min(
                            crossing_values[
                                candle_id - max_cross_down_lookback : candle_id - delay
                            ]
                        )
                    except ValueError:
                        raise RuntimeError(
                            "crossing_up: not enough values_to_cross, length needs to be same "
                            "as max_cross_down_lookback"
                        )

                if was_below and didnt_cross_to_much:
                    for i in range(0, delay + 1):
                        condition = (
                            crossing_values[candle_id - i]
                            > values_to_cross[candle_id - i]
                        )
                        if not condition:
                            crossing_data.append(0)
                            break
                    if condition:
                        crossing_data.append(1)
                else:
                    crossing_data.append(0)
                if not max_history:
                    break
            return crossing_data
        else:
            length = len(values_to_cross)
            closes = await get_candles_(maker, PriceDataSources.CLOSE.value)
            closes = closes[-length:]
            # highs = exchange_public_data.High(context, limit=data_limit)
            lows = await get_candles_(maker, PriceDataSources.LOW.value)
            lows = lows[-length:]

            for candle_id in range(min_candles, length):
                if not max_history:
                    candle_id = length - 1
                condition = False
                was_below = None
                is_currently_above = None
                try:
                    was_below = (
                        lows[candle_id - delay - 1]
                        < values_to_cross[candle_id - delay - 1]
                    )
                    is_currently_above = (
                        closes[candle_id - 1] > values_to_cross[candle_id - 1]
                    )
                except IndexError:
                    raise RuntimeError(
                        "crossing_up: not enough values_to_cross, length needs to be same as delay"
                    )

                didnt_cross_to_much = True
                if max_cross_down is not None:
                    try:
                        didnt_cross_to_much = min(
                            values_to_cross[
                                candle_id - max_cross_down_lookback : candle_id
                            ]
                        ) - float(
                            await offset.get_offset(maker.ctx, "-" + max_cross_down)
                        ) < min(
                            lows[candle_id - max_cross_down_lookback : candle_id]
                        )
                    except ValueError:
                        raise RuntimeError(
                            "crossing_up: not enough values_to_cross, length needs to be same "
                            "as max_cross_down_lookback"
                        )

                if was_below and is_currently_above and didnt_cross_to_much:
                    # check if closed above within delay time
                    for i in range(1, delay + 2):
                        condition = (
                            closes[candle_id - i] > values_to_cross[candle_id - i]
                        )
                        if not condition:
                            crossing_data.append(0)
                            break
                    if condition:
                        crossing_data.append(1)
                else:
                    crossing_data.append(0)
                if not max_history:
                    break
            return crossing_data


async def crossing_down_(
    maker=None,
    values_to_cross=None,
    crossing_values=None,
    delay=0,
    max_cross_up=None,
    max_cross_up_lookback=5,
    max_history=True,
):
    # true if price just fell under value and stayed there for delay time
    min_candles = max_cross_up_lookback + delay + 1
    crossing_data = []

    if values_to_cross is None:
        raise RuntimeError("crossing_up: you need to provide values_to_cross")
    else:
        if crossing_values is not None:
            length = min([len(values_to_cross), len(crossing_values)])
            values_to_cross = values_to_cross[-length:]
            crossing_values = crossing_values[-length:]
            for candle_id in range(min_candles, length):
                if not max_history:
                    candle_id = length - 1
                condition = False
                was_above = None
                try:
                    was_above = (
                        crossing_values[candle_id - delay - 1]
                        > values_to_cross[candle_id - delay - 1]
                    )
                except IndexError:
                    raise RuntimeError(
                        "crossing_up: not enough values_to_cross, length needs to be same as delay"
                    )

                didnt_cross_to_much = True
                if max_cross_up:
                    try:
                        didnt_cross_to_much = max(
                            values_to_cross[
                                candle_id - max_cross_up_lookback : candle_id - delay
                            ]
                        ) + float(
                            await offset.get_offset(maker.ctx, "-" + max_cross_up)
                        ) > max(
                            crossing_values[
                                candle_id - max_cross_up_lookback : candle_id - delay
                            ]
                        )
                    except ValueError:
                        raise RuntimeError(
                            "crossing_up: not enough values_to_cross, length needs to be same "
                            "as max_cross_down_lookback"
                        )

                if was_above and didnt_cross_to_much:
                    for i in range(0, delay + 1):
                        condition = (
                            crossing_values[candle_id - i]
                            < values_to_cross[candle_id - i]
                        )
                        if not condition:
                            crossing_data.append(0)
                            break
                    if condition:
                        crossing_data.append(1)
                else:
                    crossing_data.append(0)
                if not max_history:
                    break
            return crossing_data
        else:
            length = len(values_to_cross)
            closes = await get_candles_(maker, PriceDataSources.CLOSE.value)
            closes = closes[-length:]
            # highs = exchange_public_data.High(context, limit=data_limit)
            highs = await get_candles_(maker, PriceDataSources.HIGH.value)
            highs = highs[-length:]
            for candle_id in range(min_candles, length):
                if not max_history:
                    candle_id = length - 1
                condition = False
                was_above = None
                is_currently_below = None
                try:
                    was_above = (
                        highs[candle_id - delay - 1]
                        > values_to_cross[candle_id - delay - 1]
                    )
                    is_currently_below = (
                        closes[candle_id - 1] < values_to_cross[candle_id - 1]
                    )
                except IndexError:
                    raise RuntimeError(
                        "crossing_up: not enough values_to_cross, length needs to be same as delay"
                    )

                didnt_cross_to_much = True
                if max_cross_up is not None:
                    try:
                        didnt_cross_to_much = max(
                            values_to_cross[
                                candle_id - max_cross_up_lookback : candle_id
                            ]
                        ) + float(
                            await offset.get_offset(maker.ctx, "-" + max_cross_up)
                        ) > max(
                            highs[candle_id - max_cross_up_lookback : candle_id]
                        )
                    except ValueError:
                        raise RuntimeError(
                            "crossing_up: not enough values_to_cross, length needs to be same "
                            "as max_cross_down_lookback"
                        )

                if was_above and is_currently_below and didnt_cross_to_much:
                    # check if closed above within delay time
                    for i in range(1, delay + 2):
                        condition = (
                            closes[candle_id - i] < values_to_cross[candle_id - i]
                        )
                        if not condition:
                            crossing_data.append(0)
                            break
                    if condition:
                        crossing_data.append(1)
                else:
                    crossing_data.append(0)
                if not max_history:
                    break
            return crossing_data


async def crossing_(
    maker=None,
    values_to_cross=None,
    crossing_values=None,
    delay=0,
    max_cross=None,
    max_cross_lookback=5,
    max_history=False,
):
    # true if price just went below or over value and stayed there for delay time and didnt cross to much
    c_up = await crossing_up_(
        maker=maker,
        values_to_cross=values_to_cross,
        crossing_values=crossing_values,
        delay=delay,
        max_cross_down=max_cross,
        max_cross_down_lookback=max_cross_lookback,
        max_history=max_history,
    )

    c_down = await crossing_down_(
        maker=maker,
        values_to_cross=values_to_cross,
        crossing_values=crossing_values,
        delay=delay,
        max_cross_up=max_cross,
        max_cross_up_lookback=max_cross_lookback,
        max_history=max_history,
    )
    return c_up, c_down
