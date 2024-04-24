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

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_storage.grid_instance as grid_instance


class PingPongGridData:
    def __init__(
        self,
        ping_pong_storage,
        grid_id: str,
        group_key: str,
    ):
        self.grid_data: typing.Dict[str, grid_instance.PingPongGridInstanceData] = {}
        self.any_entry_placed: bool = False
        self.ping_pong_storage = ping_pong_storage
        self.grid_id: str = grid_id
        self.group_key: str = group_key

    async def restore_from_raw(self, raw_grid_instance) -> None:
        for grid_instance_id, raw_grid_instance in raw_grid_instance.items():
            self.grid_data[grid_instance_id] = grid_instance.PingPongGridInstanceData(
                ping_pong_storage=self.ping_pong_storage,
                grid_id=self.grid_id,
                group_key=self.group_key,
                grid_instance_id=grid_instance_id,
            )
            await self.grid_data[grid_instance_id].restore_from_raw(raw_grid_instance)

    def set_grid_data(
        self,
        grid_instance_id: str,
        created_orders: list,
        calculated_entries: typing.List[decimal.Decimal],
        calculated_amounts: typing.List[decimal.Decimal],
    ) -> None:
        if grid_instance_id in self.grid_data:
            _grid_instance = self.grid_data[grid_instance_id]
        else:
            _grid_instance = grid_instance.PingPongGridInstanceData(
                ping_pong_storage=self.ping_pong_storage,
                grid_id=self.grid_id,
                group_key=self.group_key,
                grid_instance_id=grid_instance_id,
            )
        _grid_instance.set_order_data(
            created_orders=created_orders,
            calculated_entries=calculated_entries,
            calculated_amounts=calculated_amounts,
        )
        if _grid_instance.any_entry_placed:
            self.any_entry_placed = True
            self.grid_data[grid_instance_id] = _grid_instance

    def get_grid_instance_data(
        self, grid_instance_id
    ) -> grid_instance.PingPongGridInstanceData:
        return self.grid_data[grid_instance_id]

    def to_dict(self):
        grid_dict = {}
        for grid_instance_id, _grid_instance in self.grid_data.items():
            grid_instance_dict = _grid_instance.to_dict()
            if grid_instance_id:
                grid_dict[grid_instance_id] = grid_instance_dict
        return grid_dict
