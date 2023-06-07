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
import aiohttp.streams

import trading_backend.exchanges as exchanges


class Binance(exchanges.Exchange):
    LEGACY_SPOT_ID = "T9698EB7"
    SPOT_ID = "HR452G85"
    MARGIN_ID = None
    LEGACY_FUTURE_ID = "uquVg2pc"
    FUTURE_ID = "uquVg2pc"
    LEGACY_REF_ID = "135007948"
    REF_ID = "528112221"
    IS_SPONSORING = True

    @classmethod
    def get_name(cls):
        return 'binance'

    def _get_order_custom_id(self):
        return f"x-{self._get_id()}{self._exchange.connector.client.uuid22()}"

    @classmethod
    def use_legacy_ids(cls):
        cls.SPOT_ID = cls.LEGACY_SPOT_ID
        cls.FUTURE_ID = cls.LEGACY_FUTURE_ID

    def get_orders_parameters(self, params=None) -> dict:
        params = super().get_orders_parameters(params)
        params.update({'newClientOrderId': self._get_order_custom_id()})
        return params

    async def _ensure_broker_status(self):
        try:
            details = await self._get_account_referral_details()
            if not details.get("rebateWorking", False):
                if (ref_id := details.get("referrerId", None)) and ref_id == self.LEGACY_REF_ID:
                    self.use_legacy_ids()
                    details = await self._get_account_referral_details()
                    if details.get("rebateWorking", False):
                        return "Using legacy broker id"
                return f"Broker rebate not working: {details}"
            return f"Broker rebate is enabled."
        except Exception as err:
            return f"Broker rebate check error: {err}"

    async def _get_account_referral_details(self) -> dict:
        return await self._exchange.connector.client.sapi_get_apireferral_ifnewuser(
            params=self._exchange._get_params({
                "apiAgentCode": self._get_id()
            })
        )

    async def _inner_is_valid_account(self) -> (bool, str):
        details = None
        try:
            details = await self._get_account_referral_details()
            if not details.get("rebateWorking", False):
                ref_id = details.get("referrerId", None)
                if ref_id is not None:
                    return False, f"This account has a referral id equal to {ref_id} " \
                                  f"which is incompatible ({self.REF_ID} as referral id or no referral id is required)"
                return False, f"This account is incompatible, details: {details}. Please report this message to " \
                              f"admins for investigation. " \
                              f"An account with {self.REF_ID} as referral id or no referral id is required."
            if not details.get("ifNewUser", False):
                return False, "Binance requires accounts that were created after july 1st 2021, " \
                              "this account is too old."
        except AttributeError:
            if isinstance(details, aiohttp.streams.StreamReader):
                return False, "Error when fetching exchange data (unreadable response)"
            return False, "Invalid request parameters"
        return True, None
