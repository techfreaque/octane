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
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_storage.grid as grid


class PingPongGroupData:
    def __init__(
        self,
        ping_pong_storage,
        group_key: str,
    ):
        self.group_data: typing.Dict[str, grid.PingPongGridData] = {}
        self.any_entry_placed: bool = False
        self.ping_pong_storage = ping_pong_storage
        self.group_key: str = group_key

    async def restore_from_raw(self, raw_group_instance) -> None:
        for grid_id, raw_grid in raw_group_instance.items():
            self.group_data[grid_id] = grid.PingPongGridData(
                ping_pong_storage=self.ping_pong_storage,
                grid_id=grid_id,
                group_key=self.group_key,
            )
            await self.group_data[grid_id].restore_from_raw(raw_grid)

    def set_group_data(
        self,
        grid_id: str,
        grid_instance_id: str,
        created_orders: list,
        calculated_entries: typing.List[decimal.Decimal],
        calculated_amounts: typing.List[decimal.Decimal],
    ) -> None:
        if grid_id in self.group_data:
            _grid = self.group_data[grid_id]
        else:
            _grid = grid.PingPongGridData(
                ping_pong_storage=self.ping_pong_storage,
                grid_id=grid_id,
                group_key=self.group_key,
            )
        _grid.set_grid_data(
            grid_instance_id=grid_instance_id,
            created_orders=created_orders,
            calculated_entries=calculated_entries,
            calculated_amounts=calculated_amounts,
        )
        if _grid.any_entry_placed:
            self.any_entry_placed = True
            self.group_data[grid_id] = _grid

    def get_grid_data(self, grid_id) -> grid.PingPongGridData:
        return self.group_data[str(grid_id)]

    def to_dict(self):
        group_dict = {}
        for grid_id, _grid in self.group_data.items():
            grid_dict = _grid.to_dict()
            if grid_dict:
                group_dict[grid_id] = grid_dict
        return group_dict
