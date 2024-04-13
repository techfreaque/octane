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

from ast import Tuple
import typing
import octobot_trading.enums as trading_enums

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong import (
    ping_pong_constants,
)
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_storage.element as element


class PingPongGroupData:
    group_data: typing.Dict[str, element.PingPongSingleData] = {}

    def __init__(
        self,
        ping_pong_info_storage,
        group_key: str,
        order_group_id: str,
        entry_orders: list = None,
        calculated_entries: list = None,
        init_only: bool = False,
    ):
        self.ping_pong_info_storage = ping_pong_info_storage
        self.order_group_id: str = order_group_id
        self.group_key: str = group_key
        self.any_entry_placed = False
        if not init_only:
            for grid_id, order in enumerate(entry_orders):
                if isinstance(order, dict):
                    if (
                        order[trading_enums.ExchangeConstantsOrderColumns.STATUS.value]
                        == trading_enums.OrderStatus.REJECTED.value
                    ):
                        return  # Order was rejected
                    else:
                        raise RuntimeError(
                            "order dicts arent handled in ping pong mode"
                        )
                (stop_loss_price, stop_loss_tag, take_profit_price, take_profit_tag) = (
                    self.get_exit_order_data(order)
                )
                self.any_entry_placed = True
                self.set_grid_data(
                    grid_id=str(grid_id),
                    symbol=order.symbol,
                    take_profit_price=take_profit_price,
                    take_profit_tag=take_profit_tag,
                    side=order.side.value,
                    amount=float(str(order.filled_quantity)),
                    entry_price=float(str(calculated_entries[grid_id])),
                    entry_tag=order.tag,
                    stop_loss_price=stop_loss_price,
                    stop_loss_tag=stop_loss_tag,
                )

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

    async def restore_from_raw(self, raw_group_instance) -> None:
        for grid_id, raw_grid in raw_group_instance.items():
            self.group_data[grid_id] = element.PingPongSingleData(
                ping_pong_storage=self.ping_pong_info_storage,
                grid_id=grid_id,
                order_group_id=self.order_group_id,
                group_key=self.group_key,
                symbol=raw_grid[ping_pong_constants.PingPongSingleDataColumns.SYMBOL],
                take_profit_price=raw_grid[
                    ping_pong_constants.PingPongSingleDataColumns.TAKE_PROFIT_PRICE
                ],
                take_profit_tag=raw_grid[
                    ping_pong_constants.PingPongSingleDataColumns.TAKE_PROFIT_TAG
                ],
                side=raw_grid[ping_pong_constants.PingPongSingleDataColumns.SIDE],
                amount=raw_grid[ping_pong_constants.PingPongSingleDataColumns.AMOUNT],
                entry_price=raw_grid[
                    ping_pong_constants.PingPongSingleDataColumns.ENTRY_PRICE
                ],
                entry_tag=raw_grid[
                    ping_pong_constants.PingPongSingleDataColumns.ENTRY_TAG
                ],
                stop_loss_price=raw_grid[
                    ping_pong_constants.PingPongSingleDataColumns.STOP_LOSS_PRICE
                ],
                stop_loss_tag=raw_grid[
                    ping_pong_constants.PingPongSingleDataColumns.STOP_LOSS_TAG
                ],
                entry_counter=raw_grid[
                    ping_pong_constants.PingPongSingleDataColumns.ENTRY_COUNTER
                ],
                ping_pong_active=raw_grid[
                    ping_pong_constants.PingPongSingleDataColumns.PING_PONG_ACTIVE
                ],
            )

    def set_grid_data(
        self,
        grid_id,
        symbol: str,
        take_profit_price: float,
        take_profit_tag: str,
        side: str,
        amount: float,
        entry_price: float,
        entry_tag: str,
        stop_loss_price: float = None,
        stop_loss_tag: str = None,
    ) -> None:
        self.group_data[grid_id] = element.PingPongSingleData(
            ping_pong_storage=self.ping_pong_info_storage,
            grid_id=grid_id,
            order_group_id=self.order_group_id,
            group_key=self.group_key,
            symbol=symbol,
            take_profit_price=take_profit_price,
            take_profit_tag=take_profit_tag,
            side=side,
            amount=amount,
            entry_price=entry_price,
            entry_tag=entry_tag,
            stop_loss_price=stop_loss_price,
            stop_loss_tag=stop_loss_tag,
            ping_pong_active=True,
        )

    def get_grid_data(self, grid_id) -> element.PingPongSingleData:
        return self.group_data[str(grid_id)]

    # def log_replaced_entry_order(
    #     self,
    #     grid_id: str,
    #     recreated_entry_order,
    # ):
    #     self.get_grid_data(grid_id).log_replaced_entry_order(recreated_entry_order)

    # def get_last_entry_order(self, grid_id) -> PingPongSingleData:
    #     return self.get_grid_data(grid_id).get_last_entry_order()

    # def get_single_data_if_enabled(self, grid_id) -> element.PingPongSingleData or None:
    #     single_data: element.PingPongSingleData = self.get_grid_data(grid_id)
    #     if (
    #         self.order_group_settings.ping_pong.ping_pong_mode_enabled
    #         and single_data.enabled
    #     ):
    #         return single_data
    #     return None

    # def get_original_calculated_entry_price(self, grid_id):
    #     return self.get_grid_data(grid_id).get_calculated_entry()

    def to_dict(self):
        grid_dict = {}
        for grid_id, this_group_data in self.group_data.items():
            grid_dict[grid_id] = this_group_data.to_dict()
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
