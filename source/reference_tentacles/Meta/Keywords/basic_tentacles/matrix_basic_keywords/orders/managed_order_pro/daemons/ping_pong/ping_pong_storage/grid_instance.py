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

import decimal
import typing
import octobot_trading.enums as trading_enums

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong import (
    ping_pong_constants,
)
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_storage.element as element


class PingPongGridInstanceData:
    def __init__(
        self,
        ping_pong_storage,
        grid_id: str,
        group_key: str,
        grid_instance_id: str,
    ):
        self.grid_instance_data: typing.Dict[str, element.PingPongSingleData] = {}
        self.any_entry_placed: bool = False
        self.ping_pong_storage = ping_pong_storage
        self.grid_id: str = grid_id
        self.group_key: str = group_key
        self.grid_instance_id: str = grid_instance_id

    @staticmethod
    def get_exit_order_data(
        order,
    ) -> typing.Tuple[float | None, str | None, float | None, str | None]:
        take_profit_price: float = None
        take_profit_tag: str = None
        stop_loss_price: float = None
        stop_loss_tag: str = None
        for exit_order in order.chained_orders:
            if is_stop_loss(exit_order.order_type.value):
                stop_loss_price = float(str(exit_order.origin_price))
                stop_loss_tag = exit_order.tag
            elif is_take_profit(exit_order.order_type.value):
                take_profit_price = float(str(exit_order.origin_price))
                take_profit_tag = exit_order.tag
        return (stop_loss_price, stop_loss_tag, take_profit_price, take_profit_tag)

    async def restore_from_raw(self, raw_grid_instance) -> None:
        for order_id, raw_order in raw_grid_instance.items():
            self.grid_instance_data[order_id] = element.PingPongSingleData(
                ping_pong_storage=self.ping_pong_storage,
                order_id=order_id,
                grid_id=self.grid_id,
                grid_instance_id=self.grid_instance_id,
                group_key=self.group_key,
                symbol=raw_order[ping_pong_constants.PingPongSingleDataColumns.SYMBOL],
                take_profit_price=raw_order[
                    ping_pong_constants.PingPongSingleDataColumns.TAKE_PROFIT_PRICE
                ],
                take_profit_tag=raw_order[
                    ping_pong_constants.PingPongSingleDataColumns.TAKE_PROFIT_TAG
                ],
                side=raw_order[ping_pong_constants.PingPongSingleDataColumns.SIDE],
                amount=raw_order[ping_pong_constants.PingPongSingleDataColumns.AMOUNT],
                entry_price=raw_order[
                    ping_pong_constants.PingPongSingleDataColumns.ENTRY_PRICE
                ],
                entry_tag=raw_order[
                    ping_pong_constants.PingPongSingleDataColumns.ENTRY_TAG
                ],
                stop_loss_price=raw_order[
                    ping_pong_constants.PingPongSingleDataColumns.STOP_LOSS_PRICE
                ],
                stop_loss_tag=raw_order[
                    ping_pong_constants.PingPongSingleDataColumns.STOP_LOSS_TAG
                ],
                entry_counter=raw_order[
                    ping_pong_constants.PingPongSingleDataColumns.ENTRY_COUNTER
                ],
                ping_pong_active=raw_order[
                    ping_pong_constants.PingPongSingleDataColumns.PING_PONG_ACTIVE
                ],
            )

    def set_order_data(
        self,
        created_orders: list,
        calculated_entries: typing.List[decimal.Decimal],
        calculated_amounts: typing.List[decimal.Decimal],
    ) -> None:
        for order_id, order in enumerate(created_orders):
            if isinstance(order, dict):
                if (
                    order[trading_enums.ExchangeConstantsOrderColumns.STATUS.value]
                    == trading_enums.OrderStatus.REJECTED.value
                ):
                    continue
                else:
                    raise RuntimeError("order dicts arent handled in ping pong mode")
            (stop_loss_price, stop_loss_tag, take_profit_price, take_profit_tag) = (
                self.get_exit_order_data(order)
            )
            self.any_entry_placed = True
            self.grid_instance_data[str(order_id)] = element.PingPongSingleData(
                ping_pong_storage=self.ping_pong_storage,
                order_id=str(order_id),
                group_key=self.group_key,
                grid_id=self.grid_id,
                grid_instance_id=self.grid_instance_id,
                symbol=order.symbol,
                take_profit_price=take_profit_price,
                take_profit_tag=take_profit_tag,
                side=order.side.value,
                amount=float(str(calculated_amounts[order_id])),
                entry_price=float(str(calculated_entries[order_id])),
                entry_tag=order.tag,
                stop_loss_price=stop_loss_price,
                stop_loss_tag=stop_loss_tag,
                ping_pong_active=True,
            )

    def get_order_data(self, order_id) -> element.PingPongSingleData:
        return self.grid_instance_data[str(order_id)]

    def to_dict(self):
        grid_dict = {}
        for order_id, order in self.grid_instance_data.items():
            order_dict = order.to_dict()
            if order_dict:
                grid_dict[order_id] = order_dict
        return grid_dict


def is_stop_loss(order_type: str):
    return order_type in (
        trading_enums.TraderOrderType.STOP_LOSS,
        trading_enums.TraderOrderType.STOP_LOSS_LIMIT,
        trading_enums.TraderOrderType.STOP_LOSS.value,
        trading_enums.TraderOrderType.STOP_LOSS_LIMIT.value,
    )


def is_take_profit(order_type: str):
    return order_type in (
        trading_enums.TraderOrderType.SELL_LIMIT,
        trading_enums.TraderOrderType.BUY_LIMIT,
        trading_enums.TraderOrderType.SELL_LIMIT.value,
        trading_enums.TraderOrderType.BUY_LIMIT.value,
        trading_enums.TradeOrderType.LIMIT.value,
        trading_enums.TradeOrderType.LIMIT,
    )
