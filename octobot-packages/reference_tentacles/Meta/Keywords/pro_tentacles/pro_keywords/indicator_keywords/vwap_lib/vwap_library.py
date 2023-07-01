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

import octobot_commons.enums as common_enums
from datetime import datetime

# from dateutil.relativedelta import relativedelta, MO


def calculate_VWAP_length(
    start_time=None, time_frame="15m", vwap_time_window="session"
):
    if vwap_time_window == "24h":
        return int(
            (60 / common_enums.TimeFramesMinutes[common_enums.TimeFrames(time_frame)])
            * 24
        )
    else:
        current_datetime = datetime.fromtimestamp(start_time)
        if vwap_time_window == "session":

            current_time_formatted = current_datetime.time()

            time_difference = (
                datetime.combine(datetime.min, current_time_formatted) - datetime.min
            )
            # returns amount of 15m candles since midnight
            return int(
                time_difference.seconds
                / 60
                / common_enums.TimeFramesMinutes[common_enums.TimeFrames(time_frame)]
            )

        elif vwap_time_window == "week":
            week_start = current_datetime.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            time_difference = current_datetime - week_start
            # returns amount of 15m candles since monday midnight
            return int(
                (time_difference.seconds / 60 / 15) + (time_difference.days * 24 * 4)
            )

        elif vwap_time_window == "month":
            week_start = current_datetime.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            time_difference = current_datetime - week_start
            # returns amount of candles since month start midnight
            return int(
                (time_difference.seconds / 60 / 15) + (time_difference.days * 24 * 4)
            )
        # elif vwap_time_window == "since last pivot":
        #     beginning = 1


def calculate_current_VWAP(candle_data, volume, length=None):
    volume_x_candle_data = []
    volume_x_candle_sum = 0.0
    volume_sum = 0.0
    for i in range(0, length):
        current_volume_x_candle = candle_data[i] * volume[i]
        volume_x_candle_sum = volume_x_candle_sum + current_volume_x_candle
        volume_sum = volume_sum + volume[i]
        volume_x_candle_data.append(current_volume_x_candle)
    try:
        return volume_x_candle_sum / volume_sum
    except ZeroDivisionError:
        return None


def calculate_historical_VWAP(
    candle_data, volume, time_data, window="session", time_frame="15m"
):
    vwap_data = []
    if window == "24h":
        length = calculate_VWAP_length(time_frame=time_frame, vwap_time_window=window)

        for candle_id in range(length, len(candle_data)):
            volume_x_candle_data = []
            volume_x_candle_sum = 0.0
            volume_sum = 0.0
            for vwap_candle_id in range(0, length):
                reversed_candle_id = length - vwap_candle_id
                current_volume_x_candle = (
                    candle_data[candle_id - reversed_candle_id]
                    * volume[candle_id - reversed_candle_id]
                )
                volume_x_candle_sum = volume_x_candle_sum + current_volume_x_candle
                volume_sum = volume_sum + volume[candle_id - reversed_candle_id]
                volume_x_candle_data.append(current_volume_x_candle)

            vwap_data.append(volume_x_candle_sum / volume_sum)

    else:
        for candle_id in range(0, len(candle_data)):
            length = calculate_VWAP_length(
                time_data[candle_id], time_frame, vwap_time_window=window
            )

            volume_x_candle_data = []
            volume_x_candle_sum = 0.0
            volume_sum = 0.0
            for vwap_candle_id in range(0, length):
                try:
                    current_volume_x_candle = (
                        candle_data[vwap_candle_id + candle_id]
                        * volume[vwap_candle_id + candle_id]
                    )
                    volume_x_candle_sum = volume_x_candle_sum + current_volume_x_candle
                    volume_sum = volume_sum + volume[vwap_candle_id + candle_id]
                    volume_x_candle_data.append(current_volume_x_candle)
                except IndexError:
                    pass  # end of data
            try:
                vwap_data.append(volume_x_candle_sum / volume_sum)
            except ZeroDivisionError:
                vwap_data.append(0)
            candle_id += length
    return vwap_data
