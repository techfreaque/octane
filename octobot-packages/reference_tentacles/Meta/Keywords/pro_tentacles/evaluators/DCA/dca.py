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

import datetime
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_evaluator_data,
    allow_enable_plot,
)


def get_buy_signal_from_time(current_time, day, hour, minute):
    current_datetime = datetime.datetime.fromtimestamp(current_time)
    time_to_buy = current_datetime
    if day:
        time_to_buy = time_to_buy.replace(day=int(day), second=0, microsecond=0)
    if hour:
        time_to_buy = time_to_buy.replace(hour=int(hour), second=0, microsecond=0)
    if minute:
        time_to_buy = time_to_buy.replace(minute=int(minute), second=0, microsecond=0)
    return current_datetime == time_to_buy


async def get_dollar_cost_average(maker, evaluator):
    day = await user_input2(
        maker,
        evaluator,
        "signals on day of the month",
        "options",
        "every",
        options=[
            "every",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
            "25",
            "26",
            "27",
            "28",
            "29",
            "30",
            "31",
        ],
    )
    if day == "every":
        day = None
    hour = await user_input2(
        maker,
        evaluator,
        "signals on hour",
        "options",
        "0",
        options=[
            "every",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
        ],
    )
    if hour == "every":
        hour = None

    minute = await user_input2(
        maker,
        evaluator,
        "signals on minute",
        "options",
        "0",
        options=[
            "every",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
            "25",
            "26",
            "27",
            "28",
            "29",
            "30",
            "31",
            "32",
            "33",
            "34",
            "35",
            "36",
            "37",
            "38",
            "39",
            "40",
            "41",
            "42",
            "43",
            "44",
            "45",
            "46",
            "47",
            "48",
            "49",
            "50",
            "51",
            "52",
            "53",
            "54",
            "55",
            "56",
            "57",
            "58",
            "59",
        ],
    )
    if minute == "every":
        minute = None

    await allow_enable_plot(maker, evaluator, "Plot DCA signals")

    evaluator.chart_location, evaluator.title = (
        "main-chart",
        f"DCA buy signal (d:{day} h:{hour} m:{minute})",
    )
    evaluator.values = await get_candles_(maker, PriceDataSources.LOW.value)
    times = await get_candles_(maker, PriceDataSources.TIME.value)
    evaluator.signals = []

    for timestamp in times:
        evaluator.signals.append(get_buy_signal_from_time(timestamp, day, hour, minute))

    return await store_evaluator_data(maker, evaluator)
