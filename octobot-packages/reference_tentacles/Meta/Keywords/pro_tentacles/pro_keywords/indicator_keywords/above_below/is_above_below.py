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


def is_above(
    below_data, above_data, confirmation_time=1, above_percent=1, max_history=True
):
    data_len = min([len(below_data), len(above_data)])
    below_data = below_data[-data_len:]
    above_data = above_data[-data_len:]
    below_data = np.asarray(below_data)
    above_data = np.asarray(above_data)
    signals = []
    for i in range(0, data_len):
        range_start = -i - confirmation_time - 1
        range_end = -i if i != 0 else None
        signals.append(
            1
            if all(
                (below_data[range_start:range_end] * ((100 + above_percent) / 100))
                < above_data[range_start:range_end]
            )
            else 0
        )
        if not max_history:
            break
    signals.reverse()
    return signals


def is_below(
    above_data, below_data, confirmation_time=1, below_percent=1, max_history=True
):
    data_len = min([len(below_data), len(above_data)])
    below_data = below_data[-data_len:]
    above_data = above_data[-data_len:]
    below_data = np.asarray(below_data)
    above_data = np.asarray(above_data)
    signals = []
    for i in range(0, data_len):
        range_start = -i - confirmation_time - 1
        range_end = -i if i != 0 else None
        signals.append(
            1
            if all(
                (above_data[range_start:range_end] * ((100 - below_percent) / 100))
                > below_data[range_start:range_end]
            )
            else 0
        )
        if not max_history:
            break
    signals.reverse()
    return signals
