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

TAKE_PROFIT = "tp"
ENTRY = "e"
STOP_LOSS = "sl"


class PingPongOrderToOrderGroupIdConstants:
    GROUP_KEY = "group_key"
    ORDER_GROUP_ID = "order_group_id"
    GRID_ID = "grid_id"
    ENTRY_ORDER = "entry_order"


class PingPongConstants:
    FIRST_ORDER_CHAIN_ID = 0
    LAST_ORDER_CHAIN_ID = "last_order_chain_id"
    START_INFO_DATA: dict = {
        LAST_ORDER_CHAIN_ID: FIRST_ORDER_CHAIN_ID,
    }
    PING_PONG_INFO_STORAGE = "ping_pong_info_storage"
    PING_PONG_STORAGE = "ping_pong_storage"

    ENTRIES = "entries"
    EXITS = "exits"


class PingPongSingleDataColumns:
    GRID_ID = "grid_id"
    ORDER_ID = "order_id"
    GRID_INSTANCE_ID = "grid_instance_id"
    GROUP_KEY = "group_key"
    ENTRY_COUNTER = "entry_counter"
    PING_PONG_ACTIVE = "ping_pong_active"
    SYMBOL = "symbol"
    TAKE_PROFIT_PRICE = "take_profit_price"
    TAKE_PROFIT_TAG = "take_profit_tag"
    SIDE = "side"
    AMOUNT = "amount"
    ENTRY_PRICE = "entry_price"
    ENTRY_TAG = "entry_tag"
    STOP_LOSS_PRICE = "stop_loss_price"
    STOP_LOSS_TAG = "stop_loss_tag"
    ENTRY_COUNTER = "entry_counter"
