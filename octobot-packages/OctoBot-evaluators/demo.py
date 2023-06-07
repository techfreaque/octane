#  Drakkar-Software OctoBot-Evaluators
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import asyncio
import logging

from octobot_commons.enums import TimeFrames

from octobot_commons.logging.logging_util import get_logger

from octobot_evaluators.api.evaluators import initialize_evaluators, create_and_start_all_type_evaluators
from octobot_evaluators.api.initialization import create_evaluator_channels
from octobot_evaluators.evaluators.channel.evaluator_channel import get_chan
from octobot_evaluators.constants import MATRIX_CHANNEL

config = {
    "crypto-currencies": {
        "Bitcoin": {
            "pairs": [
                "BTC/USDT"
            ]
        },
        "Ethereum": {
            "pairs": [
                "ETH/USDT"
            ]
        }
    },
    "exchanges": {},
}


async def matrix_callback(matrix_id,
                          evaluator_name,
                          evaluator_type,
                          eval_note,
                          eval_note_type,
                          eval_time,
                          exchange_name,
                          cryptocurrency,
                          symbol,
                          time_frame):
    logging.info(f"MATRIX : EXCHANGE = {exchange_name} || EVALUATOR = {evaluator_name} ||"
                 f" CRYPTOCURRENCY = {cryptocurrency} || SYMBOL = {symbol} || TF = {time_frame} || NOTE = {eval_note}")


async def create_evaluators_channel():
    matrix_id: str = await initialize_evaluators(config)
    await create_evaluator_channels(matrix_id)
    await get_chan(MATRIX_CHANNEL, matrix_id).new_consumer(matrix_callback)
    await create_and_start_all_type_evaluators(matrix_id=matrix_id,
                                               exchange_name="test",
                                               symbols=["BTC/USDT"],
                                               time_frames=[TimeFrames.ONE_HOUR])

    await get_chan(MATRIX_CHANNEL, matrix_id).get_internal_producer().send(matrix_id=matrix_id,
                                                                           evaluator_name="test",
                                                                           evaluator_type="test",
                                                                           eval_note=1)

    await asyncio.sleep(10)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    get_logger().info("starting...")

    main_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(main_loop)

    main_loop.run_until_complete(create_evaluators_channel())
