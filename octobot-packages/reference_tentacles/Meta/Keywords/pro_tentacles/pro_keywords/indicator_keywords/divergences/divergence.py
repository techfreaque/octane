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


def _check_if_other_has_higher_low(
    candle_id,
    pivot_id,
    other_values,
    other_source_data,
    pivot_match_range,
    pivot_lookback_other,
    ll_only,
    current_base_pivot_val,
):
    if ll_only:
        div_other_value = min(
            other_values[
                candle_id - pivot_id - pivot_match_range : candle_id - pivot_id + 1
            ]
        )
        return 1, current_base_pivot_val, div_other_value
    else:
        # check if other data has higher low
        try:
            div_other_value = min(
                other_values[
                    candle_id - pivot_id - pivot_match_range : candle_id - pivot_id + 1
                ]
            )
            if any(
                div_other_value
                > other_source_data[
                    candle_id - pivot_id - pivot_lookback_other : candle_id + 1
                ]
            ):
                return 0, 0, 0
            else:
                # divergence found
                return 1, current_base_pivot_val, div_other_value
        except ValueError:
            pass
        return 0, 0, 0


def check_if_base_was_ll_before(
    base_source_data, candle_id, origin_range_start, time_for_ll, current_base_pivot_val
):
    return any(
        (base_source_data[candle_id - origin_range_start : candle_id - time_for_ll + 1])
        >= current_base_pivot_val
    )


def check_if_base_had_ll_within_range(
    base_source_data,
    candle_id,
    ll_range_start,
    confirmation_time,
    current_base_pivot_val,
):
    return any(
        (
            base_source_data[
                candle_id - ll_range_start : candle_id - confirmation_time + 1
            ]
        )
        < current_base_pivot_val
    )


# def _check_if_price_is_above_ll_within_confirmation_time(confirmation_time, base_source_data, candle_id, timerange_ll):
#     # check if price is above ll within confirmation time
#     didnt_break_in_delay_range = None
#     if confirmation_time != 0:
#         low_in_delay_range = min(
#             base_source_data[candle_id - confirmation_time + 1:candle_id + 1])
#         didnt_break_in_delay_range = timerange_ll <= low_in_delay_range
#     return confirmation_time == 0 or didnt_break_in_delay_range


def _check_if_base_has_ll(
    base_source_data,
    candle_id,
    time_for_ll,
    confirmation_time,
    base_values,
    pivot_id,
    pivot_lookback_base,
    wait_for_a_reversal,
):
    current_base_pivot_val = base_values[candle_id - pivot_id]

    # check if no ll before (time range between pivot and start of ll period)
    origin_range_start = (
        pivot_id - pivot_lookback_base
    )  # range between pivot and current price
    if (
        origin_range_start > time_for_ll
    ):  # check if time for ll is lower than max pivot age
        if not check_if_base_was_ll_before(
            base_source_data,
            candle_id,
            origin_range_start,
            time_for_ll,
            current_base_pivot_val,
        ):
            return False, 0
        ll_range_start = time_for_ll
    else:
        ll_range_start = origin_range_start

    # check if base has lower low within allowed range
    if check_if_base_had_ll_within_range(
        base_source_data,
        candle_id,
        ll_range_start,
        confirmation_time,
        current_base_pivot_val,
    ):

        # check for reversal
        if wait_for_a_reversal:
            try:
                confirmation_range_above_pivot = current_base_pivot_val <= min(
                    base_source_data[candle_id - confirmation_time : candle_id + 1]
                )
            except:
                confirmation_range_above_pivot = True

            if confirmation_range_above_pivot:
                return True, current_base_pivot_val
                # return _check_if_price_is_above_ll_within_confirmation_time(confirmation_time, base_source_data,
                #                                                             candle_id, timerange_ll),\
                #        current_base_pivot_val
        else:
            return True, current_base_pivot_val
    return False, 0


def _check_if_matching_pivot_found(
    base_data, candle_id, pivot_id, other_data, pivot_match_range
):
    # return True
    return base_data[candle_id - pivot_id] and any(
        other_data[candle_id - pivot_id - pivot_match_range : candle_id - pivot_id + 1]
    )


def _check_if_divergence_for_pivot(
    base_source_data,
    candle_id,
    time_for_ll,
    confirmation_time,
    base_values,
    pivot_id,
    pivot_lookback_base,
    other_values,
    base_data,
    other_data,
    pivot_match_range,
    other_source_data,
    pivot_lookback_other,
    wait_for_a_reversal,
    ll_only,
):
    if _check_if_matching_pivot_found(
        base_data, candle_id, pivot_id, other_data, pivot_match_range
    ):
        try:
            ll_found, current_base_pivot_val = _check_if_base_has_ll(
                base_source_data,
                candle_id,
                time_for_ll,
                confirmation_time,
                base_values,
                pivot_id,
                pivot_lookback_base,
                wait_for_a_reversal,
            )
            if ll_found:
                (
                    bullish_divergence,
                    div_base_value,
                    div_other_value,
                ) = _check_if_other_has_higher_low(
                    candle_id,
                    pivot_id,
                    other_values,
                    other_source_data,
                    pivot_match_range,
                    pivot_lookback_other,
                    ll_only,
                    current_base_pivot_val,
                )
                return bullish_divergence, div_base_value, div_other_value

        except ValueError:
            pass
    return None, 0, 0


def _find_divergence_for_candle(
    min_pivot_age,
    max_pivot_age,
    base_data,
    candle_id,
    other_data,
    base_source_data,
    time_for_ll,
    confirmation_time,
    base_values,
    pivot_lookback_base,
    other_values,
    pivot_match_range,
    other_source_data,
    pivot_lookback_other,
    wait_for_a_reversal,
    ll_only,
):
    for pivot_id in range(min_pivot_age, max_pivot_age):
        (
            bullish_divergence,
            div_base_value,
            div_other_value,
        ) = _check_if_divergence_for_pivot(
            base_source_data,
            candle_id,
            time_for_ll,
            confirmation_time,
            base_values,
            pivot_id,
            pivot_lookback_base,
            other_values,
            base_data,
            other_data,
            pivot_match_range,
            other_source_data,
            pivot_lookback_other,
            wait_for_a_reversal,
            ll_only,
        )
        if bullish_divergence:
            return bullish_divergence, div_base_value, div_other_value
    return None, 0, 0


def _add_divergence_data(
    div_data,
    bullish_divergence,
    div_base_values,
    div_base_value,
    div_other_values,
    div_other_value,
    cleaned_div_data,
    cleaned_div_base_values,
    cleaned_div_other_values,
):
    div_data.append(bullish_divergence)
    div_base_values.append(div_base_value)
    div_other_values.append(div_other_value)
    # dont flash a signal if it was one candle before
    try:
        if div_data[-2] == 1:
            bullish_divergence = None
            div_base_value = 0
            div_other_value = 0
    except IndexError:
        pass  # first result is empty
    cleaned_div_data.append(bullish_divergence)
    cleaned_div_base_values.append(div_base_value)
    cleaned_div_other_values.append(div_other_value)


def divergence_(
    base_data,
    other_data,
    base_values,
    other_values,
    base_source_data,
    other_source_data,
    max_pivot_age,
    min_pivot_age,
    time_for_ll,
    confirmation_time,
    pivot_lookback_base,
    pivot_lookback_other,
    pivot_match_range,
    wait_for_a_reversal,
    ll_only,
):
    d_length = min(len(base_data), len(other_data), len(base_values), len(other_values))
    base_data = base_data[-d_length:]
    other_data = other_data[-d_length:]
    base_values = base_values[-d_length:]
    other_values = other_values[-d_length:]
    base_source_data = base_source_data[-d_length:]
    other_source_data = other_source_data[-d_length:]
    div_data = []
    div_base_values = []
    div_other_values = []
    cleaned_div_data = []
    cleaned_div_base_values = []
    cleaned_div_other_values = []
    for candle_id in range(max_pivot_age, d_length):
        # find pivots between min and max age
        (
            bullish_divergence,
            div_base_value,
            div_other_value,
        ) = _find_divergence_for_candle(
            min_pivot_age,
            max_pivot_age,
            base_data,
            candle_id,
            other_data,
            base_source_data,
            time_for_ll,
            confirmation_time,
            base_values,
            pivot_lookback_base,
            other_values,
            pivot_match_range,
            other_source_data,
            pivot_lookback_other,
            wait_for_a_reversal,
            ll_only,
        )
        _add_divergence_data(
            div_data,
            bullish_divergence,
            div_base_values,
            div_base_value,
            div_other_values,
            div_other_value,
            cleaned_div_data,
            cleaned_div_base_values,
            cleaned_div_other_values,
        )

    return (
        div_data,
        div_other_values,
        div_base_values,
        cleaned_div_data,
        cleaned_div_other_values,
        cleaned_div_base_values,
    )
