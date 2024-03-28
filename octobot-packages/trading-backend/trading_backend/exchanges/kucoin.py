#  Drakkar-Software trading-backend
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
import ccxt

import trading_backend.exchanges as exchanges
import trading_backend.enums


class Kucoin(exchanges.Exchange):
    SPOT_ID = "Octobot"
    SPOT_PRIVATE_KEY = "0782058c-8c05-45f1-bfe1-840e2f96335a"
    MARGIN_ID = ""
    MARGIN_PRIVATE_KEY = ""
    FUTURE_ID = "Octobotfutures"
    FUTURE_PRIVATE_KEY = "018e58ef-d9ac-4c8e-9646-0afa7fa9e37c"
    IS_SPONSORING = True

    @classmethod
    def get_name(cls):
        return 'kucoin'

    async def _get_api_key_rights(self) -> list[trading_backend.enums.APIKeyRights]:
        # It is currently impossible to fetch api key permissions: try to cancel an imaginary order,
        # if a permission error is raised instead of a cancel fail, then trading permissions are missing.
        # updated: 24/01/2024
        rights = [trading_backend.enums.APIKeyRights.READING]
        try:
            # use client api to avoid any ccxt call wrapping and error handling
            await self._exchange.connector.client.cancel_order("12345", symbol="BTC/USDT")
        except ccxt.AuthenticationError as err:
            if "permission" in str(err).lower():
                # does not have trading permission
                pass
            else:
                # another error
                raise
        except ccxt.ExchangeError:
            # has trading permission
            rights.append(trading_backend.enums.APIKeyRights.SPOT_TRADING)
            rights.append(trading_backend.enums.APIKeyRights.MARGIN_TRADING)
            rights.append(trading_backend.enums.APIKeyRights.FUTURES_TRADING)
        return rights

    def _get_partner_details(self):
        return {
            'spot': {
                'id': self.SPOT_ID,
                'key': self.SPOT_PRIVATE_KEY,
            },
            'future': {
                'id': self.FUTURE_ID,
                'key': self.FUTURE_PRIVATE_KEY,
            },
        }

    def get_orders_parameters(self, params=None) -> dict:
        if self._exchange.connector.client.options.get("partner") != self._get_partner_details():
            self._exchange.connector.client.options["partner"] = self._get_partner_details()
        return super().get_orders_parameters(params)
