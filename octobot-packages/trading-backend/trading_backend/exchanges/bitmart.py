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
import trading_backend.exchanges as exchanges


class Bitmart(exchanges.Exchange):
    SPOT_ID = "OCTOBOTBROKER01"
    FUTURE_ID = "OCTOBOTBROKER01"
    IS_SPONSORING = True

    @classmethod
    def get_name(cls):
        return 'bitmart'

    def get_orders_parameters(self, params=None) -> dict:
        if self._exchange.connector.client.options.get("brokerId", None) != self._get_id():
            self._exchange.connector.client.options["brokerId"] = self._get_id()
        return super().get_orders_parameters(params)
