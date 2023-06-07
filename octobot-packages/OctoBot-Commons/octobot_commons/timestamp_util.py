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

import time
from datetime import datetime

_EPOCH = time.time()
TIMEZONE_DELTA = datetime.fromtimestamp(_EPOCH) - datetime.utcfromtimestamp(_EPOCH)


def convert_timestamp_to_datetime(
    timestamp, time_format="%d/%m/%y %H:%M", force_timezone=False
):
    """
    Convert a timestamp to a datetime object
    :param timestamp: the timestamp to convert
    :param time_format: the time format
    :param force_timezone: if the timezone should be forced
    :return: the created datetime object
    """
    if force_timezone:
        timestamp += TIMEZONE_DELTA.seconds
    return datetime.fromtimestamp(timestamp).strftime(time_format)


def convert_timestamps_to_datetime(
    timestamps, time_format="%d/%m/%y %H:%M", force_timezone=False
):
    """
    Convert multiple timestamps to datetime objects
    :param timestamps: the timestamp to convert list
    :param time_format: the time format
    :param force_timezone: if the timezone should be forced
    :return: the created datetime objects
    """
    return [
        convert_timestamp_to_datetime(
            timestamp, time_format=time_format, force_timezone=force_timezone
        )
        for timestamp in timestamps
    ]


def is_valid_timestamp(timestamp):
    """
    Check if the timestamp is valid
    :param timestamp: the timestamp to check
    :return: the check result
    """
    if timestamp:
        try:
            datetime.fromtimestamp(timestamp)
        except OSError:
            return False
        except ValueError:
            return False
        except OverflowError:
            return False
        except TypeError:
            return False
    return True


def get_now_time(time_format="%Y-%m-%d %H:%M:%S"):
    """
    Get the current time
    :param time_format: the time format
    :return: the current timestamp
    """
    return datetime.fromtimestamp(time.time()).strftime(time_format)


def datetime_to_timestamp(date_time_str: str, date_time_format: str) -> float:
    """
    Convert a datetime to timestamp
    :param date_time_str: the datetime string
    :param date_time_format: the datetime format
    :return: the timestamp
    """
    return time.mktime(
        create_datetime_from_string(date_time_str, date_time_format).timetuple()
    )


def create_datetime_from_string(date_time_str: str, date_time_format: str) -> datetime:
    """
    Convert a string to datetime
    :param date_time_str: the datetime string
    :param date_time_format: the datetime format
    :return: the converted datetime
    """
    return datetime.strptime(date_time_str, date_time_format)
