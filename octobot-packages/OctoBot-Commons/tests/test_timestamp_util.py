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

from octobot_commons.timestamp_util import is_valid_timestamp, get_now_time, datetime_to_timestamp, \
    convert_timestamp_to_datetime


def test_is_valid_timestamp():
    assert not is_valid_timestamp(get_now_time())
    assert is_valid_timestamp(time.time())


def test_datetime_to_timestamp():
    assert datetime_to_timestamp(convert_timestamp_to_datetime(322548600, time_format="%d/%m/%y %H:%M"),
                                 date_time_format="%d/%m/%y %H:%M") == 322548600

