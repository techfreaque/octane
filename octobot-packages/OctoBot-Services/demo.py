#  Drakkar-Software OctoBot-Services
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
import os
from logging.config import fileConfig

from octobot_commons.constants import CONFIG_ENABLED_OPTION

from octobot_services.api.services import create_service_factory, stop_services, get_available_services
from octobot_services.constants import CONFIG_CATEGORY_SERVICES, CONFIG_REDDIT, CONFIG_TELEGRAM, \
    CONFIG_USERNAMES_WHITELIST, CONFIG_TOKEN, CONFIG_TWITTER, CONFIG_WEB, CONFIG_WEB_PORT, CONFIG_WEB_IP, \
    CONFIG_CHAT_ID, CONFIG_REDDIT_CLIENT_ID, CONFIG_REDDIT_PASSWORD, CONFIG_REDDIT_CLIENT_SECRET, \
    CONFIG_REDDIT_USERNAME, CONFIG_TW_ACCESS_TOKEN_SECRET, CONFIG_TW_ACCESS_TOKEN, CONFIG_TW_API_SECRET, \
    CONFIG_TW_API_KEY

config = {
    CONFIG_CATEGORY_SERVICES: {
        CONFIG_REDDIT: {
            CONFIG_REDDIT_CLIENT_ID: os.getenv('REDDIT_CLIENT_ID'),
            CONFIG_REDDIT_CLIENT_SECRET: os.getenv('REDDIT_CLIENT_SECRET'),
            CONFIG_REDDIT_PASSWORD: os.getenv('REDDIT_PASSWORD'),
            CONFIG_REDDIT_USERNAME: os.getenv('REDDIT_USERNAME')
        },
        CONFIG_TELEGRAM: {
            CONFIG_CHAT_ID: os.getenv('TELEGRAM_CHAT_ID'),
            CONFIG_TOKEN: os.getenv('TELEGRAM_TOKEN'),
            CONFIG_USERNAMES_WHITELIST: []
        },
        CONFIG_TWITTER: {
            CONFIG_TW_ACCESS_TOKEN: os.getenv('TW_ACCESS_TOKEN'),
            CONFIG_TW_ACCESS_TOKEN_SECRET: os.getenv('TW_ACCESS_TOKEN_SECRET'),
            CONFIG_TW_API_KEY: os.getenv('TW_API_KEY'),
            CONFIG_TW_API_SECRET: os.getenv('TW_API_SECRET')
        },
        CONFIG_WEB: {
            CONFIG_ENABLED_OPTION: True,
            CONFIG_WEB_IP: "0.0.0.0",
            CONFIG_WEB_PORT: 5000
        }
    },
}


async def _create_services():
    try:
        import tentacles
        service_list = get_available_services()
        backtesting_enabled = False
        for service_class in service_list:
            service_factory = create_service_factory(config)
            await service_factory.create_or_get_service(service_class, backtesting_enabled, {})
    except ImportError as e:
        logging.error("Error: tentacle architecture doesn't exist in running directory, to run this test file please "
                      "add a tentacle folder containing services tentacles in running directory.")
        raise e


if __name__ == '__main__':
    fileConfig("logs/logging_config.ini")

    async def start_stop():
        logging.info("** Starting services **")
        await _create_services()

        logging.info("** Stopping services **")
        await stop_services()

    asyncio.run(start_stop)

    logging.info("** End of services checkup **")
