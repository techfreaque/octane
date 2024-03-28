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
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import openai._extras
import os

import octobot_commons.logging


def _log_loaded_unused_lib_factory(lib):
    logger = octobot_commons.logging.get_logger("openai_adapters")
    logger.debug(f"Disabling {lib} openai proxy")

    def _log_loaded_unused_lib(*_):
        logger.debug(
            f"Loading {lib} unavailable lib. Skipping call returning 'proxy_mock'."
        )
        return "proxy_mock"

    return _log_loaded_unused_lib


def _disable_openai_unused_libs_proxy():
    try:
        import pandas
    except ImportError:
        openai._extras.pandas_proxy.PandasProxy.__load__ = _log_loaded_unused_lib_factory("pandas")


def _set_openai_default_key():
    # prevent OpenAI Proxy to crash when used
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")


def patch_openai_proxies():
    _disable_openai_unused_libs_proxy()
    _set_openai_default_key()
