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


def pivot_high_(high, swing_history=1, unbroken=True):
    swing_range = swing_history * 2
    is_swing_high = False
    if len(high) >= swing_range:
        swing_high = high[-swing_history]
        for j in range(1, swing_range + 1):
            is_swing_high = True
            if j <= swing_history:
                if high[-j] > swing_high:
                    is_swing_high = False
                    break
            if j > swing_history:
                if high[-j] >= swing_high:
                    is_swing_high = False
                    break
    return is_swing_high


def pivot_low_(low, swing_history=1):
    swing_range = swing_history * 2
    is_swing_low = False
    if len(low) >= swing_range:
        swing_low = low[-swing_history]
        for j in range(1, swing_range + 1):
            is_swing_low = True
            if j <= swing_history:
                if low[-j] < swing_low:
                    is_swing_low = False
                    break
            if j > swing_history:
                if low[-j] <= swing_low:
                    is_swing_low = False
                    break
    return is_swing_low


#
# def pivot_(low=None, high=None, swing_history=4, unbroken=False):
#     pivot_highs_data = []
#     pivot_lows_data = []
#
#     if high is not None:
#         pivot_highs_data = pivot_high_(high, swing_history, unbroken)
#         if low is None:
#             return pivot_highs_data
#         else:
#             pivot_lows_data = pivot_low_(low, swing_history, unbroken)
#             return [pivot_lows_data, pivot_highs_data]
#
#     elif low is not None:
#         pivot_lows_data = pivot_low_(low, swing_history, unbroken)
#         if high is None:
#             return pivot_lows_data
#
#
# # print(pivots(high=High(time_frame="1h"), low=Low(time_frame="1h")))
#
#
# def all_pivot_(ctx=None, tf_counter=2, base_time_frame="15m", time_frames=None, side="all"):
#     if time_frames is None:
#         time_frames = ["30m", "1h", "4h", "1d"]
#     pivots_dont_exist = True  # todo find a way to check if exists in db - if it exists only update missing ones
#     if pivots_dont_exist:
#         all_timeframe_pivots = []
#         for time_frame in time_frames:
#             time_data = Time(ctx, ctx.traded_pair, time_frame)
#             lows_data = []
#             highs_data = []
#             pivot_lows_data = []
#             major_pivot_lows_data = []
#             pivot_highs_data = []
#             major_pivot_highs_data = []
#             if side == PriceDataSources.LOW.value:
#                 lows_data = Low(ctx, ctx.traded_pair, time_frame)
#                 pivot_lows_data = pivot_low(low=lows_data)
#                 major_pivot_lows_data = major_pivot_low(low=lows_data)
#
#             elif side == "all":
#                 lows_data = Low(ctx, ctx.traded_pair, time_frame)
#                 highs_data = High(ctx, ctx.traded_pair, time_frame)
#                 pivots_data = pivot(high=highs_data, low=lows_data)
#                 pivot_lows_data, pivot_highs_data = pivots_data
#                 major_pivots_data = major_pivot(high=highs_data, low=lows_data)
#                 major_pivot_lows_data, major_pivot_highs_data = major_pivots_data
#
#             elif side == PriceDataSources.HIGH.value:
#                 highs_data = High(ctx, ctx.traded_pair, time_frame)
#                 pivot_highs_data = pivot_high(high=highs_data)
#                 major_pivot_highs_data = major_pivot_high(high=highs_data)
#
#             all_timeframe_pivots.append({
#                 'time_frame': time_frame,
#                 'time': time_data,
#                 'lows': lows_data,
#                 'pivot_lows': pivot_lows_data,
#                 'major_pivot_lows': major_pivot_lows_data,
#                 'highs': highs_data,
#                 'pivot_highs': pivot_highs_data,
#                 'major_pivot_highs': major_pivot_highs_data,
#             })
#
#             # todo write to candles db, pair, exchange, time and timeframe are needed to identify db and candle data row
#             #  only write pivot_lows = pivots_data[0], pivot_highs = pivots_data[1]
#             #  and major_pivot_lows = major_pivots_data[0], major_pivot_highs = pivots_data[1]
#         base_time_data = Time(ctx, ctx.traded_pair, base_time_frame)
#         base_timeframe_pivots = []
#         base_lows_data = []
#         base_highs_data = []
#         base_pivot_lows_data = []
#         base_pivot_highs_data = []
#         base_major_pivot_lows_data = []
#         base_major_pivot_highs_data = []
#         combined_pivots = defaultdict(list)
#         if side == "all":
#             base_lows_data = Low(ctx, ctx.traded_pair, base_time_frame)
#             base_highs_data = High(ctx, ctx.traded_pair, base_time_frame)
#             base_pivots_data = pivot(high=base_highs_data, low=base_lows_data)
#             base_pivot_lows_data, base_pivot_highs_data = base_pivots_data
#             base_major_pivots_data = major_pivot(high=base_highs_data, low=base_lows_data)
#             base_major_pivot_lows_data, base_major_pivot_highs_data = base_major_pivots_data
#
#         for base_candle in range(1, len(base_time_data) + 1):
#             start_time = base_time_data[-base_candle]
#             base_time_frame_time = base_time_data[2] - base_time_data[1]
#             end_datetime = start_time + base_time_frame_time
#             base_candle_low = base_lows_data[-base_candle]
#             base_candle_high = base_highs_data[-base_candle]
#             count = 0
#             major_count = 0
#             if base_pivot_lows_data[-base_candle]:
#                 count = 1
#             if base_major_pivot_lows_data[-base_candle]:
#                 major_count = 1
#             for time_frame in range(0, len(time_frames)):
#                 current_timeframe_pivots = all_timeframe_pivots[time_frame]
#                 current_timeframe = current_timeframe_pivots["time_frame"]
#                 candle_is_pivot = False
#                 candle_is_major_pivot = False
#                 current_time_frame_var = commons_enums.TimeFrames(current_timeframe)
#                 current_time_frame_start_time = start_time - commons_enums.TimeFramesMinutes[current_time_frame_var] * 60
#
#                 for candle_low_nr in range(1, len(current_timeframe_pivots[PriceDataSources.TIME.value]) + 1):
#                     candle_time = current_timeframe_pivots[PriceDataSources.TIME.value][-candle_low_nr]
#                     candle_low = current_timeframe_pivots["lows"][-candle_low_nr]
#                     candle_pivot_low = current_timeframe_pivots["pivot_lows"][-candle_low_nr]
#                     candle_major_pivot_low = current_timeframe_pivots["major_pivot_lows"][-candle_low_nr]
#
#                     if candle_low == base_candle_low and current_time_frame_start_time <= candle_time < end_datetime:
#                         if candle_pivot_low:
#                             candle_is_pivot = True
#                             count = count + 1
#                             if candle_major_pivot_low:
#                                 candle_is_major_pivot = True
#                                 major_count = major_count + 1
#                                 break
#                             else:
#                                 break
#
#                 combined_pivots["pivot_" + current_timeframe].insert(0, candle_is_pivot)
#                 combined_pivots["major_pivot_" + current_timeframe].insert(0, candle_is_major_pivot)
#
#             combined_pivots["low_counter"].insert(0, count)
#             combined_pivots["major_low_counter"].insert(0, major_count)
#             if count >= tf_counter:
#                 combined_pivots["is_strong_low"].insert(0, True)
#                 if major_count >= tf_counter:
#                     combined_pivots["is_strong_major_low"].insert(0, True)
#                 else:
#                     combined_pivots["is_strong_major_low"].insert(0, False)
#             else:
#                 combined_pivots["is_strong_major_low"].insert(0, False)
#                 combined_pivots["is_strong_low"].insert(0, False)
#
#         combined_pivots['time_frame'].append(base_time_frame)
#         combined_pivots['time'].append(base_time_data)
#         combined_pivots['lows'].append(base_lows_data)
#         combined_pivots['pivot_lows'].append(base_pivot_lows_data)
#         combined_pivots['major_pivot_lows'].append(base_major_pivot_lows_data)
#         combined_pivots['highs'].append(base_highs_data)
#         combined_pivots['pivot_highs'].append(base_pivot_highs_data)
#         combined_pivots['major_pivot_highs'].append(base_major_pivot_highs_data)
#
#         #
#         # for candle_high_nr in range(1, len(current_timeframe_pivots[PriceDataSources.TIME.value])):
#         #     candle_time = current_timeframe_pivots[PriceDataSources.TIME.value][-candle_high_nr]
#         #     candle_high = current_timeframe_pivots["highs"][-candle_high_nr]
#         #
#         #     test = 1  # todo append candle timeframe to base_candle in base_timeframe_pivots list
#         #     #  new column pivot_low_timeframes ["1h", "4h"]
#         #     # todo if no record write empty so that len is the same
#         #
#         # # todo append count pivot_low_timeframes to base_timeframe_pivots count entries ["1h", "4h"]  empty is 0
#
#         # combined_pivot_low.append({
#         #     'time_frame': base_time_frame,
#         #     'time': base_time_data.append(),
#         #     'lows': base_lows_data,
#         #     'pivot_lows': base_pivot_lows_data,
#         #    # 'major_pivot_lows': base_major_pivots_data,
#         #     'highs': base_highs_data,
#         #     'pivot_highs': base_pivot_highs_data,
#         #     'major_pivot_highs': base_major_pivot_highs_data,
#         # })
#
#         return [combined_pivots["is_strong_low"], combined_pivots["is_strong_major_low"]]
#         # return combined_pivots


def unbroken_pivot_low_(
    pivot_lows_data,
    lows_data,
    price_lows,
    pivots_len=100,
    confirmation=0,
    min_pivot_age=0,
):
    unbroken_pivot_lows_data = []
    count = 0
    pivot_price_list = []
    is_unbroken_low = False
    pivot_data_len = len(pivot_lows_data)
    try:
        for j in range(1 + min_pivot_age, pivot_data_len + 1):
            if count < pivots_len:
                if pivot_lows_data[-j]:
                    if j <= confirmation:
                        is_unbroken_low = True
                    else:
                        # check if unbroken from pivot low to current price
                        for i in range(0, j - confirmation):
                            if lows_data[-j] <= lows_data[-j + i]:
                                is_unbroken_low = True
                            else:
                                is_unbroken_low = False
                                break
                        # take prices into account that are not in pivots prices
                        if is_unbroken_low:
                            for i in range(len(price_lows) - confirmation):
                                if not lows_data[-j] <= price_lows[i]:
                                    is_unbroken_low = False
                                    break

                else:
                    is_unbroken_low = False
                if is_unbroken_low:
                    if price_lows[-1] > lows_data[-j]:
                        count = count + 1
                    unbroken_pivot_lows_data.insert(0, is_unbroken_low)
                    pivot_price_list.insert(0, lows_data[-j])
    except:
        print("Unbroken Pivots: cant create enough requested unbroken pivots lows")
    return unbroken_pivot_lows_data, pivot_price_list


def unbroken_pivot_high_(
    pivot_highs_data,
    highs_data,
    price_highs,
    pivots_len=100,
    confirmation=1,
    min_pivot_age=0,
):
    unbroken_pivot_highs_data = []
    count = 0
    pivot_price_list = []
    is_unbroken_high = False
    pivot_data_len = len(pivot_highs_data)
    try:
        for j in range(1 + min_pivot_age, pivot_data_len + 1):
            if count < pivots_len:
                if pivot_highs_data[-j]:
                    if j <= confirmation:
                        is_unbroken_high = True
                    else:
                        # check if unbroken from pivot high to current price
                        for i in range(0, j - confirmation):
                            if highs_data[-j] >= highs_data[-j + i]:
                                is_unbroken_high = True
                            else:
                                is_unbroken_high = False
                                break
                        # take prices into account that are not in pivots prices
                        if is_unbroken_high:
                            for i in range(len(price_highs) - confirmation):
                                if not highs_data[-j] >= price_highs[i]:
                                    is_unbroken_high = False
                                    break

                else:
                    is_unbroken_high = False
                if is_unbroken_high:
                    if price_highs[-1] < highs_data[-j]:
                        count = count + 1
                    unbroken_pivot_highs_data.insert(0, is_unbroken_high)
                    pivot_price_list.insert(0, highs_data[-j])
    except:
        print("Unbroken Pivots: cant create enough requested unbroken pivot highs")
    return unbroken_pivot_highs_data, pivot_price_list
