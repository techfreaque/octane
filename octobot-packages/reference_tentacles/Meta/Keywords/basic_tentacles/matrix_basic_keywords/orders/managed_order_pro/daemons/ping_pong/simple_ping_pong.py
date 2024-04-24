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
from octobot_services.interfaces.util.util import run_in_bot_main_loop
import octobot_trading.enums as trading_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords import matrix_enums
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_constants as ping_pong_constants
from .ping_pong_storage import storage as storage
from .ping_pong_storage import element as element
import tentacles.Meta.Keywords.scripting_library.orders.order_types as order_types


RETRY_RECREATE_ENTRY_ATTEMPTS_COUNT: int = 30

PING_PONG_TIMEOUT = 1000


async def play_ping_pong(
    trading_mode,
    symbol,
    triggered_order,
):
    if is_relevant_take_profit_order(
        triggered_order=triggered_order,
    ):
        if trading_mode.exchange_manager.is_backtesting:
            await play_simple_ping_pong(
                trading_mode=trading_mode,
                symbol=symbol,
                triggered_order=triggered_order,
            ),
        else:
            run_in_bot_main_loop(
                play_simple_ping_pong(
                    trading_mode=trading_mode,
                    symbol=symbol,
                    triggered_order=triggered_order,
                ),
                blocking=False,
                timeout=PING_PONG_TIMEOUT,
            )


async def play_simple_ping_pong(
    trading_mode,
    symbol,
    triggered_order,
):
    retry_counter = 0
    tag_info = triggered_order["tag"].split(matrix_enums.TAG_SEPERATOR)
    group_key = tag_info[1]
    grid_id = tag_info[2]
    grid_instance_id = tag_info[3]
    order_id = tag_info[4]
    ping_pong_group_data: element.PingPongSingleData = await get_entry_ping_pong_data(
        trading_mode=trading_mode,
        triggered_order=triggered_order,
        group_key=group_key,
        grid_instance_id=grid_instance_id,
        grid_id=grid_id,
        order_id=order_id,
        retry_counter=retry_counter,
    )
    if ping_pong_group_data:
        retry_counter = 0
        trading_mode.ctx.enable_trading = True

        await recreate_entry_order(
            trading_mode=trading_mode,
            ping_pong_single_data=ping_pong_group_data,
            symbol=symbol,
            triggered_order=triggered_order,
            retry_counter=retry_counter,
        )
        trading_mode.ctx.enable_trading = False


def is_relevant_take_profit_order(
    triggered_order: dict,
) -> bool:
    return (
        triggered_order.get("status") == trading_enums.OrderStatus.FILLED.value
        and triggered_order.get("type") == trading_enums.TradeOrderType.LIMIT.value
        and triggered_order["tag"]
        and triggered_order["tag"].startswith(ping_pong_constants.TAKE_PROFIT)
    )


async def get_entry_ping_pong_data(
    trading_mode,
    triggered_order: dict,
    group_key: str,
    grid_instance_id: str,
    grid_id: str,
    order_id: str,
    retry_counter: int,
) -> element.PingPongSingleData | None:
    ping_pong_storage: storage.PingPongStorage = storage.get_ping_pong_storage(
        trading_mode.exchange_manager
    )
    return await ping_pong_storage.get_entry_order(
        triggered_order=triggered_order,
        group_key=group_key,
        grid_instance_id=grid_instance_id,
        order_id=order_id,
        grid_id=grid_id,
        retry_counter=retry_counter,
    )


async def recreate_entry_order(
    trading_mode,
    ping_pong_single_data: element.PingPongSingleData,
    symbol: str,
    triggered_order: dict,
    retry_counter: int,
    next_entry_data: element.PingPongSingleData = None,
):
    if not next_entry_data:
        ping_pong_single_data.update_to_replace_order_details()
        next_entry_data = ping_pong_single_data

    stop_loss_tag = next_entry_data.stop_loss_tag
    sl_price = next_entry_data.stop_loss_price
    stop_loss_offset = None
    if sl_price:
        stop_loss_offset = f"@{sl_price}"
    tp_price = next_entry_data.take_profit_price
    take_profit_offset = f"@{tp_price}"
    take_profit_tag = next_entry_data.take_profit_tag
    bundled_exit_group = None
    if sl_price and tp_price:
        bundled_exit_group = None  # TODO
    try:
        trading_mode.ctx.enable_trading = True
        trading_mode.logger.debug(
            f'A ping pong order is about to be recreated: symbol={symbol}, side={next_entry_data.side}, amount={next_entry_data.amount}, offset={f"@{next_entry_data.entry_price}"}, tag={next_entry_data.entry_tag}, stop_loss_offset={stop_loss_offset}, stop_loss_tag={stop_loss_tag}, take_profit_offset={take_profit_offset}, take_profit_tag={take_profit_tag}'
        )
        created_orders = await order_types.limit(
            trading_mode.ctx,
            symbol=symbol,
            side=next_entry_data.side,
            amount=next_entry_data.amount,
            offset=f"@{next_entry_data.entry_price}",
            tag=next_entry_data.entry_tag,
            stop_loss_offset=stop_loss_offset,
            stop_loss_tag=stop_loss_tag,
            take_profit_offset=take_profit_offset,
            take_profit_tag=take_profit_tag,
            stop_loss_group=bundled_exit_group,
            take_profit_group=bundled_exit_group,
        )
    except Exception as error:
        retry_counter += 1
        return await retry_recreate_entry_order(
            trading_mode=trading_mode,
            ping_pong_single_data=ping_pong_single_data,
            symbol=symbol,
            triggered_order=triggered_order,
            retry_counter=retry_counter,
            next_entry_data=next_entry_data,
            error=error,
        )
    try:
        recreated_entry_order = created_orders[0]
        if recreated_entry_order and recreated_entry_order.status in (
            trading_enums.OrderStatus.CLOSED,
            trading_enums.OrderStatus.OPEN,
            trading_enums.OrderStatus.FILLED,
            trading_enums.OrderStatus.PARTIALLY_FILLED,
        ):
            ping_pong_single_data.log_replaced_entry_order(
                recreated_entry_order=recreated_entry_order,
            )
            return recreated_entry_order
        raise PingPongRecreatedEntryOrderNotFilledError(
            f"Recreated order status is: {recreated_entry_order.status if recreated_entry_order else ''}"
        )
    except (
        IndexError,
        AttributeError,
        PingPongRecreatedEntryOrderNotFilledError,
    ) as error:
        retry_counter += 1
        return await retry_recreate_entry_order(
            trading_mode=trading_mode,
            symbol=symbol,
            triggered_order=triggered_order,
            retry_counter=retry_counter,
            ping_pong_single_data=ping_pong_single_data,
            next_entry_data=next_entry_data,
            error=error,
        )


async def retry_recreate_entry_order(
    trading_mode,
    symbol,
    triggered_order: dict,
    retry_counter: int,
    ping_pong_single_data: element.PingPongSingleData,
    next_entry_data: dict = None,
    error=None,
):
    if (
        retry_counter < RETRY_RECREATE_ENTRY_ATTEMPTS_COUNT
        and not trading_mode.exchange_manager.is_backtesting
    ):
        await asyncio.sleep(5)
        return await recreate_entry_order(
            trading_mode=trading_mode,
            symbol=symbol,
            triggered_order=triggered_order,
            retry_counter=retry_counter,
            ping_pong_single_data=ping_pong_single_data,
            next_entry_data=next_entry_data,
        )
    raise RuntimeError(
        "Failed to recreate entry order, when take profit got filled. "
        f"Recreated entry order: {next_entry_data}"
    ) from error


class PingPongRecreatedEntryOrderNotFilledError(Exception):
    pass
