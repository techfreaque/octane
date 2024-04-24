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

import asyncio
import decimal
import typing
import octobot_services.interfaces.util as interfaces_util
import octobot_tentacles_manager.api as tentacles_manager_api
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_constants as ping_pong_constants
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_storage.group as group
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_storage.grid as grid
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_storage.grid_instance as grid_instance
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_storage.element as element

RETRY_GET_ENTRY_ORDER_ATTEMPTS_COUNT: int = 20
RETRY_GET_ENTRY_ORDER_WAITING_TIME: int = 5


def get_all_ping_pong_data_as_dict(exchange_manager) -> dict:
    ping_pong_storage: PingPongStorage = get_ping_pong_storage(exchange_manager)
    if ping_pong_storage:
        return {
            "exchange_name": exchange_manager.exchange_name,
            "data": ping_pong_storage.to_dict(),
        }
    else:
        return {}


def reset_all_ping_pong_data(exchange_manager):
    ping_pong_storage: PingPongStorage = get_ping_pong_storage(exchange_manager)
    if ping_pong_storage:
        ping_pong_storage.reset_ping_pong_storage()
    else:
        raise RuntimeError(
            "Failed to reset ping pong storage. Storage not initialized yet"
        )


async def init_ping_pong_storage(exchange_manager) -> None:
    trading_mode = exchange_manager.trading_modes[0]
    trading_mode.ping_pong_storage = PingPongStorage(exchange_manager)
    if not exchange_manager.is_backtesting:
        await trading_mode.ping_pong_storage.restore_ping_pong_storage()


def get_ping_pong_storage(exchange_manager):
    ping_pong_storage: PingPongStorage = exchange_manager.trading_modes[
        0
    ].ping_pong_storage
    return ping_pong_storage


class PingPongStorage:
    ping_pong_storage: typing.Dict[str, group.PingPongGroupData] = {}
    ping_pong_info_storage: dict = ping_pong_constants.PingPongConstants.START_INFO_DATA

    def __init__(self, exchange_manager):
        self.exchange_manager = exchange_manager

    def set_ping_pong_data(
        self,
        group_key: str,
        grid_id: str,
        grid_instance_id: str,
        created_orders: list,
        calculated_entries: typing.List[decimal.Decimal],
        calculated_amounts: typing.List[decimal.Decimal],
    ):
        if group_key in self.ping_pong_storage:
            _group = self.ping_pong_storage[group_key]
        else:
            _group = group.PingPongGroupData(
                ping_pong_storage=self,
                group_key=group_key,
            )
        _group.set_group_data(
            grid_id=grid_id,
            grid_instance_id=grid_instance_id,
            created_orders=created_orders,
            calculated_entries=calculated_entries,
            calculated_amounts=calculated_amounts,
        )
        if _group.any_entry_placed:
            self.ping_pong_storage[group_key] = _group
            if not self.exchange_manager.is_backtesting:
                self.store_ping_pong_storage()

    def get_ping_pong_data(self, group_key: str) -> group.PingPongGroupData:
        return self.ping_pong_storage[group_key]

    def get_single_data_if_enabled(
        self, group_key: str, grid_id: str, grid_instance_id: str, order_id: str
    ) -> element.PingPongSingleData | None:
        group_data: group.PingPongGroupData = self.get_ping_pong_data(
            group_key=group_key,
        )
        grid_data: grid.PingPongGridData = group_data.get_grid_data(grid_id)
        grid_instance_data: grid_instance.PingPongGridInstanceData = (
            grid_data.get_grid_instance_data(grid_instance_id)
        )
        single_data: element.PingPongSingleData = grid_instance_data.get_order_data(
            order_id
        )
        if single_data.enabled:
            return single_data
        return None

    async def get_entry_order(
        self,
        triggered_order: dict,
        group_key: str,
        grid_instance_id: str,
        grid_id: str,
        order_id: str,
        retry_counter: int,
    ) -> element.PingPongSingleData | None:
        try:
            return self.get_single_data_if_enabled(
                group_key=group_key,
                grid_id=grid_id,
                grid_instance_id=grid_instance_id,
                order_id=order_id,
            )
        except Exception as error:
            if (
                retry_counter <= RETRY_GET_ENTRY_ORDER_ATTEMPTS_COUNT
                and not self.exchange_manager.is_backtesting
            ):
                retry_counter += 1
                await asyncio.sleep(RETRY_GET_ENTRY_ORDER_WAITING_TIME)
                return await self.get_entry_order(
                    triggered_order=triggered_order,
                    group_key=group_key,
                    grid_instance_id=grid_instance_id,
                    grid_id=grid_id,
                    order_id=order_id,
                    retry_counter=retry_counter,
                )
            raise RuntimeError(
                f"Ping pong failed. Failed to get entry order. Entry id: g{group_key}-"
                f"og{group_key}-gr{grid_id}-gi{grid_instance_id}-o{order_id} / take profit: {triggered_order}"
            ) from error

    def to_dict(self):
        storage_dict = {}
        for (
            group_key,
            _group,
        ) in self.ping_pong_storage.items():
            group_dict = _group.to_dict()
            if group_dict:
                storage_dict[group_key] = group_dict
        return storage_dict

    def generate_next_grid_instance_id(self):
        self.ping_pong_info_storage[
            ping_pong_constants.PingPongConstants.LAST_ORDER_CHAIN_ID
        ] += 1
        return str(
            self.ping_pong_info_storage[
                ping_pong_constants.PingPongConstants.LAST_ORDER_CHAIN_ID
            ]
        )

    async def restore_ping_pong_storage(self):
        orders_manager = self.exchange_manager.exchange_personal_data.orders_manager
        if not (
            orders_manager.are_exchange_orders_initialized
            and orders_manager.is_initialized
        ):
            await asyncio.sleep(5)
            return await self.restore_ping_pong_storage()
        storage_file_content = _restore_ping_pong_storage() or {}
        self.ping_pong_info_storage = storage_file_content.get(
            ping_pong_constants.PingPongConstants.PING_PONG_INFO_STORAGE,
            ping_pong_constants.PingPongConstants.START_INFO_DATA,
        )
        await self._restore_from_raw(
            storage_file_content.get(
                ping_pong_constants.PingPongConstants.PING_PONG_STORAGE, {}
            )
        )
        # store updated storage
        self.store_ping_pong_storage()

    async def _restore_from_raw(self, raw_ping_pong_storage):
        self.ping_pong_storage = {}
        for group_key, raw_group in raw_ping_pong_storage.items():
            self.ping_pong_storage[group_key] = group.PingPongGroupData(
                ping_pong_storage=self, group_key=group_key
            )
            await self.ping_pong_storage[group_key].restore_from_raw(raw_group)

    def store_ping_pong_storage(self):
        storage_dict = self.to_dict()
        self._store_ping_pong_storage(storage_dict)

    def _store_ping_pong_storage(self, ping_pong_storage_dict: dict = None):
        storage_file_content = {
            ping_pong_constants.PingPongConstants.PING_PONG_INFO_STORAGE: self.ping_pong_info_storage,
            ping_pong_constants.PingPongConstants.PING_PONG_STORAGE: ping_pong_storage_dict,
        }
        _store_ping_pong_storage(storage_file_content)

    def reset_ping_pong_storage(self):
        self.ping_pong_storage = {}
        self.store_ping_pong_storage()

    @staticmethod
    def get_name():
        return "PingPongStorage"


def _restore_ping_pong_storage():
    return (
        tentacles_manager_api.get_tentacle_config(
            interfaces_util.get_edited_tentacles_config(),
            PingPongStorage,
        )
        or {}
    )


def _store_ping_pong_storage(ping_pong_storage):
    try:
        tentacles_manager_api.update_tentacle_config(
            interfaces_util.get_edited_tentacles_config(),
            PingPongStorage,
            ping_pong_storage,
            keep_existing=False,
        )
    except TypeError:
        tentacles_manager_api.update_tentacle_config(
            interfaces_util.get_edited_tentacles_config(),
            PingPongStorage,
            ping_pong_storage,
        )
