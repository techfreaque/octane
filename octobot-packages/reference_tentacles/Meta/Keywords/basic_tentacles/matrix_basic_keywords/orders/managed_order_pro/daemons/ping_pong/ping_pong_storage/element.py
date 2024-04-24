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

import typing
import octobot_commons.logging.logging_util as logging_util
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_constants as ping_pong_constants


class PingPongSingleData:
    def __init__(
        self,
        ping_pong_storage,
        order_id: str,
        grid_id: str,
        group_key: str,
        grid_instance_id: str,
        symbol: str,
        take_profit_price: float,
        take_profit_tag: str,
        side: str,
        amount: float,
        entry_price: float,
        entry_tag: str,
        stop_loss_price: float = None,
        stop_loss_tag: str = None,
        entry_counter: int = None,
        ping_pong_active: bool = True,
    ):
        self.ping_pong_storage = ping_pong_storage
        self.grid_id: str = grid_id
        self.order_id: str = order_id
        self.group_key: str = group_key
        self.grid_instance_id: str = grid_instance_id
        self.entry_price: float = entry_price
        self.entry_counter: int = entry_counter or 1
        self.ping_pong_active: bool = ping_pong_active
        self.enabled: bool = True
        self.symbol: str = symbol
        self.take_profit_price: float = take_profit_price
        self.take_profit_tag: str = take_profit_tag
        self.side: str = side
        self.amount: float = amount
        self.entry_price: float = entry_price
        self.entry_tag: str = entry_tag
        self.stop_loss_price: float = stop_loss_price
        self.stop_loss_tag: str = stop_loss_tag

    def log_replaced_entry_order(
        self,
        recreated_entry_order,
    ) -> typing.List[str]:
        self.entry_counter += 1
        if not self.ping_pong_storage.exchange_manager.is_backtesting:
            try:
                self.ping_pong_storage.store_ping_pong_storage()
            except Exception as error:
                logging_util.get_logger("PingPongStorage").exception(
                    error, True, "Failed to permanently store ping pong storage"
                )

    def update_to_replace_order_details(self):
        self.entry_counter += 1

    def to_dict(self):
        if self.ping_pong_active:
            return {
                ping_pong_constants.PingPongSingleDataColumns.GRID_ID: self.grid_id,
                ping_pong_constants.PingPongSingleDataColumns.ORDER_ID: self.order_id,
                ping_pong_constants.PingPongSingleDataColumns.GRID_INSTANCE_ID: self.grid_instance_id,
                ping_pong_constants.PingPongSingleDataColumns.GROUP_KEY: self.group_key,
                ping_pong_constants.PingPongSingleDataColumns.ENTRY_COUNTER: self.entry_counter,
                ping_pong_constants.PingPongSingleDataColumns.PING_PONG_ACTIVE: self.ping_pong_active,
                ping_pong_constants.PingPongSingleDataColumns.SYMBOL: self.symbol,
                ping_pong_constants.PingPongSingleDataColumns.TAKE_PROFIT_PRICE: self.take_profit_price,
                ping_pong_constants.PingPongSingleDataColumns.TAKE_PROFIT_TAG: self.take_profit_tag,
                ping_pong_constants.PingPongSingleDataColumns.SIDE: self.side,
                ping_pong_constants.PingPongSingleDataColumns.AMOUNT: self.amount,
                ping_pong_constants.PingPongSingleDataColumns.ENTRY_PRICE: self.entry_price,
                ping_pong_constants.PingPongSingleDataColumns.ENTRY_TAG: self.entry_tag,
                ping_pong_constants.PingPongSingleDataColumns.STOP_LOSS_PRICE: self.stop_loss_price,
                ping_pong_constants.PingPongSingleDataColumns.STOP_LOSS_TAG: self.stop_loss_tag,
                ping_pong_constants.PingPongSingleDataColumns.ENTRY_COUNTER: self.entry_counter,
            }
        return {}
