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


def moving_up_(
    indicator_data,
    consecutive_rising_bars,
    sideways_is_rising=True,
    calculate_full_history=False,
    only_first_signal=False,
):
    if not calculate_full_history:
        is_rising = False
        if sideways_is_rising is False:
            if only_first_signal:
                for i in range(0, consecutive_rising_bars):
                    is_rising = (
                        indicator_data[-i - 1] > indicator_data[-i - 2]
                        and not indicator_data[-i - 2] > indicator_data[-i - 3]
                    )
                    if is_rising:
                        is_rising = True
                    else:
                        is_rising = False
                        break
                return 1 if is_rising else 0
            else:
                for i in range(0, consecutive_rising_bars):
                    is_rising = indicator_data[-i - 1] > indicator_data[-i - 2]
                    if is_rising:
                        is_rising = True
                    else:
                        is_rising = False
                        break
                return 1 if is_rising else 0

        else:  # sideways counts as rising
            if only_first_signal:
                was_rising = None
                for i in range(0, consecutive_rising_bars):
                    was_rising = indicator_data[-i - 2] >= indicator_data[-i - 3]
                    if was_rising:
                        was_rising = True
                    else:
                        was_rising = False
                        break
                if not was_rising:
                    for i in range(0, consecutive_rising_bars):
                        is_rising = indicator_data[-i - 1] >= indicator_data[-i - 2]
                        if is_rising:
                            is_rising = True
                        else:
                            is_rising = False
                            break
                    return 1 if is_rising else 0
            else:
                for i in range(0, consecutive_rising_bars):
                    is_rising = indicator_data[-i - 1] >= indicator_data[-i - 2]
                    if is_rising:
                        is_rising = True
                    else:
                        is_rising = False
                        break
                return 1 if is_rising else 0

    else:  # calculate full history
        rising_data = []
        if sideways_is_rising is False:
            if only_first_signal:
                for j in range(consecutive_rising_bars + 1, len(indicator_data)):
                    is_rising = False
                    for i in range(0, consecutive_rising_bars):
                        is_rising = (
                            indicator_data[j - i] > indicator_data[j - i - 1]
                            and not indicator_data[j - i - 1]
                            > indicator_data[j - i - 2]
                        )
                        if is_rising:
                            is_rising = True
                        else:
                            is_rising = False
                            break
                    rising_data.append(1 if is_rising else 0)
            else:
                for j in range(consecutive_rising_bars, len(indicator_data)):
                    is_rising = False
                    for i in range(0, consecutive_rising_bars):
                        is_rising = indicator_data[j - i] > indicator_data[j - i - 1]
                        if is_rising:
                            is_rising = True
                        else:
                            is_rising = False
                            break
                    rising_data.append(1 if is_rising else 0)

        else:  # sideways counts as rising
            if only_first_signal:
                for j in range(consecutive_rising_bars, len(indicator_data)):
                    is_rising = False
                    was_rising = None
                    for i in range(0, consecutive_rising_bars):
                        was_rising = (
                            indicator_data[j - i - 1] >= indicator_data[j - i - 2]
                        )
                        if was_rising:
                            was_rising = True
                        else:
                            was_rising = False
                            break

                    if not was_rising:
                        for i in range(0, consecutive_rising_bars):
                            is_rising = (
                                indicator_data[j - i] >= indicator_data[j - i - 1]
                            )
                            if is_rising:
                                is_rising = True
                            else:
                                is_rising = False
                                break
                    rising_data.append(1 if is_rising else 0)
            else:
                for j in range(consecutive_rising_bars, len(indicator_data)):
                    is_rising = False
                    for i in range(0, consecutive_rising_bars):
                        is_rising = indicator_data[j - i] >= indicator_data[j - i - 1]
                        if is_rising:
                            is_rising = True
                        else:
                            is_rising = False
                            break
                    rising_data.append(1 if is_rising else 0)
        return rising_data


def moving_down_(
    indicator_data,
    consecutive_falling_bars,
    sideways_is_falling=True,
    calculate_full_history=False,
    only_first_signal=False,
):
    if not calculate_full_history:
        is_falling = False
        if sideways_is_falling is False:
            if only_first_signal:
                for i in range(0, consecutive_falling_bars):
                    is_falling = (
                        indicator_data[-i - 1] < indicator_data[-i - 2]
                        and not indicator_data[-i - 2] < indicator_data[-i - 3]
                    )
                    if is_falling:
                        is_falling = True
                    else:
                        is_falling = False
                        break
                return 1 if is_falling else 0
            else:
                for i in range(0, consecutive_falling_bars):
                    is_falling = indicator_data[-i - 1] < indicator_data[-i - 2]
                    if is_falling:
                        is_falling = True
                    else:
                        is_falling = False
                        break
                return 1 if is_falling else 0

        else:  # sideways counts as falling
            if only_first_signal:
                was_falling = None
                for i in range(0, consecutive_falling_bars):
                    was_falling = indicator_data[-i - 2] <= indicator_data[-i - 3]
                    if was_falling:
                        was_falling = True
                    else:
                        was_falling = False
                        break
                if not was_falling:
                    for i in range(0, consecutive_falling_bars):
                        is_falling = indicator_data[-i - 1] <= indicator_data[-i - 2]
                        if is_falling:
                            is_falling = True
                        else:
                            is_falling = False
                            break
                    return 1 if is_falling else 0
            else:
                for i in range(0, consecutive_falling_bars):
                    is_falling = indicator_data[-i - 1] <= indicator_data[-i - 2]
                    if is_falling:
                        is_falling = True
                    else:
                        is_falling = False
                        break
                return 1 if is_falling else 0

    else:  # calculate full history
        falling_data = []
        if sideways_is_falling is False:
            if only_first_signal:
                for j in range(consecutive_falling_bars + 1, len(indicator_data)):
                    is_falling = False
                    for i in range(0, consecutive_falling_bars):
                        is_falling = (
                            indicator_data[j - i] < indicator_data[j - i - 1]
                            and not indicator_data[j - i - 1]
                            < indicator_data[j - i - 2]
                        )
                        if is_falling:
                            is_falling = True
                        else:
                            is_falling = False
                            break
                    falling_data.append(1 if is_falling else 0)
            else:
                for j in range(consecutive_falling_bars, len(indicator_data)):
                    is_falling = False
                    for i in range(0, consecutive_falling_bars):
                        is_falling = indicator_data[j - i] < indicator_data[j - i - 1]
                        if is_falling:
                            is_falling = True
                        else:
                            is_falling = False
                            break
                    falling_data.append(1 if is_falling else 0)

        else:  # sideways counts as falling
            if only_first_signal:
                for j in range(consecutive_falling_bars, len(indicator_data)):
                    is_falling = False
                    was_falling = None
                    for i in range(0, consecutive_falling_bars):
                        was_falling = (
                            indicator_data[j - i - 1] <= indicator_data[j - i - 2]
                        )
                        if was_falling:
                            was_falling = True
                        else:
                            was_falling = False
                            break

                    if not was_falling:
                        for i in range(0, consecutive_falling_bars):
                            is_falling = (
                                indicator_data[j - i] <= indicator_data[j - i - 1]
                            )
                            if is_falling:
                                is_falling = True
                            else:
                                is_falling = False
                                break
                    falling_data.append(1 if is_falling else 0)
            else:
                for j in range(consecutive_falling_bars, len(indicator_data)):
                    is_falling = False
                    for i in range(0, consecutive_falling_bars):
                        is_falling = indicator_data[j - i] <= indicator_data[j - i - 1]
                        if is_falling:
                            is_falling = True
                        else:
                            is_falling = False
                            break
                    falling_data.append(1 if is_falling else 0)
        return falling_data
