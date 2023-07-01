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


def entering_channel_up(price, val1, val2, delay=0):
    condition = False
    delay = delay + 1
    for i in range(1, delay):
        if val1 < val2:
            condition = price[-i] > val1[-i] and price[-i - 1] < val1[-i - 1]
            if not condition:
                return
        if val1 > val2:
            condition = price[-i] > val2[-i] and price[-i - 1] < val2[-i - 1]
            if not condition:
                return
    return condition


def entering_channel_down(price, val1, val2, delay=0):
    condition = False
    delay = delay + 1
    for i in range(1, delay):
        if val1 > val2:
            condition = price[-i] < val1[-i] and price[-i - 1] > val1[-i - 1]
            if not condition:
                return False
        if val1 < val2:
            condition = price[-i] < val2[-i] and price[-i - 1] > val2[-i - 1]
            if not condition:
                return False
    return condition


def entering_channel(price, val1, val2, delay=0):
    delay = delay + 1
    if entering_channel_up(price, val1, val2, delay):
        return True
    if entering_channel_down(price, val1, val2, delay):
        return True


def inside_channel(price, val1, val2, delay=0):
    condition = False
    delay = delay + 2
    for i in range(1, delay):
        if val1 < val2:
            condition = val1[-i] < price[-i] < val2[-i]
            if not condition:
                return False
        if val1 > val2:
            condition = val1[-i] > price[-i] > val2[-i]
        if not condition:
            return False
    return condition


def outside_channel(price, val1, val2, delay=0):
    condition = False
    delay = delay + 1
    for i in range(0, delay):
        if val1 < val2:
            condition = val1[-i] > price[-i] > val2[-i]
            if not condition:
                return False
        if val1 > val2:
            condition = val1[-i] < price[-i] < val2[-i]
        if not condition:
            return False
    return condition
