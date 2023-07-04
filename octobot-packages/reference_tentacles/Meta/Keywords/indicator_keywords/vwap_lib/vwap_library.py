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

import typing

import numpy
import octobot_commons.enums as common_enums
from datetime import datetime

# from dateutil.relativedelta import relativedelta, MO

SECONDS_PER_MINUTE = 60
MINUTES_PER_DAY = 24 * 60


def calculate_VWAP_length(
    start_time=None,
    time_frame="15m",
    vwap_time_window="session",
    custom_window_in_minutes: typing.Optional[int] = None,
):
    minutes_in_time_frame = common_enums.TimeFramesMinutes[
        common_enums.TimeFrames(time_frame)
    ]
    if custom_window_in_minutes:
        return int(custom_window_in_minutes / minutes_in_time_frame)
    if vwap_time_window == "24h":
        return int((SECONDS_PER_MINUTE / minutes_in_time_frame) * 24)
    current_datetime = datetime.fromtimestamp(
        start_time - minutes_in_time_frame * SECONDS_PER_MINUTE
    )
    if vwap_time_window == "session":
        current_time_formatted = current_datetime.time()

        time_difference = (
            datetime.combine(datetime.min, current_time_formatted) - datetime.min
        )
        # returns amount of 15m candles since midnight
        return int(time_difference.seconds / SECONDS_PER_MINUTE / minutes_in_time_frame)

    if vwap_time_window == "week":
        week_start = current_datetime.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        time_difference = current_datetime - week_start
        # returns amount of 15m candles since monday midnight
        return int(
            (time_difference.seconds / SECONDS_PER_MINUTE / minutes_in_time_frame)
            + (time_difference.days * MINUTES_PER_DAY / minutes_in_time_frame)
        )

    if vwap_time_window == "month":
        week_start = current_datetime.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        time_difference = current_datetime - week_start
        # returns amount of candles since month start midnight
        return int(
            (time_difference.seconds / SECONDS_PER_MINUTE / minutes_in_time_frame)
            + (time_difference.days * MINUTES_PER_DAY / minutes_in_time_frame)
        )
    # elif vwap_time_window == "since last pivot":
    #     beginning = 1


def calculate_historical_VWAP(
    candle_data,
    volume,
    time_data,
    window="session",
    time_frame="15m",
    custom_window_in_minutes: typing.Optional[int] = None,
):
    vwap_data = []
    standard_diviations = []
    if window == "24h" or custom_window_in_minutes:
        length = calculate_VWAP_length(
            time_frame=time_frame,
            vwap_time_window=window,
            custom_window_in_minutes=custom_window_in_minutes,
        )
        volume_x_candle_data = []

        for candle_id, current_candle in enumerate(candle_data):
            current_volume_x_candle = current_candle * volume[candle_id]

            volume_x_candle_data.append(current_volume_x_candle)

            relative_candle_id = candle_id + 1

            if relative_candle_id >= length:
                volume_x_candle_data = volume_x_candle_data[-length:]
                volume_x_candle_sum = sum(volume_x_candle_data)

                volumes = volume[relative_candle_id - length : relative_candle_id]
                volume_sum = sum(volumes)

                vwap_data.append(volume_x_candle_sum / volume_sum)
                standard_diviations.append(numpy.std(vwap_data[-length:]))

    else:
        volume_x_candle_data = []

        for candle_id, current_candle in enumerate(candle_data):
            length = calculate_VWAP_length(
                time_data[candle_id], time_frame, vwap_time_window=window
            )

            current_volume_x_candle = current_candle * volume[candle_id]

            volume_x_candle_data.append(current_volume_x_candle)

            relative_candle_id = candle_id + 1

            if relative_candle_id >= length:
                if length == 0:
                    vwap_data.append(current_volume_x_candle / volume[candle_id])
                    standard_diviations.append(0)

                else:
                    volume_x_candle_data = volume_x_candle_data[-length:]
                    volume_x_candle_sum = sum(volume_x_candle_data)

                    volumes = volume[relative_candle_id - length : relative_candle_id]
                    volume_sum = sum(volumes)

                    vwap_data.append(volume_x_candle_sum / volume_sum)
                    standard_diviations.append(numpy.std(vwap_data[-length:]))

            # volume_x_candle_data = []
            # volume_x_candle_sum = 0.0
            # volume_sum = 0.0
            # for vwap_candle_id in range(0, length):
            #     try:
            #         current_volume_x_candle = (
            #             candle_data[vwap_candle_id + candle_id]
            #             * volume[vwap_candle_id + candle_id]
            #         )
            #         volume_x_candle_sum = volume_x_candle_sum + current_volume_x_candle
            #         volume_sum = volume_sum + volume[vwap_candle_id + candle_id]
            #         volume_x_candle_data.append(current_volume_x_candle)
            #     except IndexError:
            #         pass  # end of data
            # try:
            #     vwap_data.append(volume_x_candle_sum / volume_sum)
            # except ZeroDivisionError:
            #     vwap_data.append(0)
            # candle_id += length
    return vwap_data, numpy.array(standard_diviations)
