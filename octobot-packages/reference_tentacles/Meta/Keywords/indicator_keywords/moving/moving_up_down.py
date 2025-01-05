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

import numpy as np
from typing import List


def moving_up(
    indicator_data: np.ndarray[int] | np.ndarray[float] | List[float] | List[int],
    consecutive_rising_bars: int,
    sideways_is_rising: bool = True,
    only_first_signal: bool = False,
) -> np.ndarray[int]:
    indicator_data = np.asarray(indicator_data)
    length = len(indicator_data)
    _consecutive_rising_bars: int = consecutive_rising_bars - 1

    if sideways_is_rising:
        is_rising = np.all(
            np.lib.stride_tricks.sliding_window_view(
                indicator_data, consecutive_rising_bars + 1
            )[:, 1:]
            >= np.lib.stride_tricks.sliding_window_view(
                indicator_data, consecutive_rising_bars + 1
            )[:, :-1],
            axis=1,
        )
    else:
        is_rising = np.all(
            np.lib.stride_tricks.sliding_window_view(
                indicator_data, consecutive_rising_bars + 1
            )[:, 1:]
            > np.lib.stride_tricks.sliding_window_view(
                indicator_data, consecutive_rising_bars + 1
            )[:, :-1],
            axis=1,
        )

    rising_data = np.zeros(length - consecutive_rising_bars, dtype=int)
    rising_data[_consecutive_rising_bars:] = is_rising.astype(int)

    if only_first_signal:
        rising_data = remove_consecutive_signals(rising_data)

    return rising_data.tolist()


def moving_down(
    indicator_data: np.ndarray[int] | np.ndarray[float] | List[float] | List[int],
    consecutive_falling_bars: int,
    sideways_is_falling: bool = True,
    only_first_signal: bool = False,
) -> np.ndarray[int]:
    indicator_data = np.asarray(indicator_data)
    length = len(indicator_data)
    _consecutive_falling_bars: int = consecutive_falling_bars - 1

    if sideways_is_falling:
        is_falling = np.all(
            np.lib.stride_tricks.sliding_window_view(
                indicator_data, consecutive_falling_bars + 1
            )[:, 1:]
            <= np.lib.stride_tricks.sliding_window_view(
                indicator_data, consecutive_falling_bars + 1
            )[:, :-1],
            axis=1,
        )
    else:
        is_falling = np.all(
            np.lib.stride_tricks.sliding_window_view(
                indicator_data, consecutive_falling_bars + 1
            )[:, 1:]
            < np.lib.stride_tricks.sliding_window_view(
                indicator_data, consecutive_falling_bars + 1
            )[:, :-1],
            axis=1,
        )

    falling_data = np.zeros(length - consecutive_falling_bars, dtype=int)
    falling_data[_consecutive_falling_bars:] = is_falling.astype(int)

    if only_first_signal:
        falling_data = remove_consecutive_signals(falling_data)

    return falling_data.tolist()


def moving_up_or_down(
    indicator_data: np.ndarray[int] | np.ndarray[float] | List[float] | List[int],
    consecutive_bars: int,
    sideways_is_direction: bool = True,
    only_first_signal: bool = False,
) -> np.ndarray[int]:
    rising_data = moving_up(
        indicator_data,
        consecutive_bars,
        sideways_is_rising=sideways_is_direction,
        only_first_signal=only_first_signal,
    )

    falling_data = moving_down(
        indicator_data,
        consecutive_bars,
        sideways_is_falling=sideways_is_direction,
        only_first_signal=only_first_signal,
    )

    combined_data = np.logical_or(np.array(rising_data), np.array(falling_data)).astype(
        int
    )

    return combined_data.tolist()


def remove_consecutive_signals(signal_data: np.ndarray[int]) -> np.ndarray[int]:
    mask = np.diff(signal_data, prepend=0) != 0
    return signal_data * mask
