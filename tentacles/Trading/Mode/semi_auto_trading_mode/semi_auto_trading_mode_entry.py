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

import octobot_commons.logging as logging
import octobot_trading.enums as trading_enums
from octobot_trading.modes.script_keywords import context_management
import tentacles.Meta.Keywords.basic_tentacles.basic_modes.mode_base.abstract_mode_base as abstract_mode_base
import tentacles.Meta.Keywords.pro_tentacles.pro_modes.semi_auto_mode.semi_auto_trading_mode as semi_auto_trading_mode
import tentacles.Meta.Keywords.basic_tentacles.basic_modes.scripted_trading_mode.use_scripted_trading_mode as use_scripted_trading_mode


class SemiAutoTradingMode(abstract_mode_base.AbstractBaseMode):
    def __init__(self, config, exchange_manager):
        super().__init__(config, exchange_manager)
        self.producer = SemiAutoTradingModeProducer
        if exchange_manager:
            use_scripted_trading_mode.initialize_scripted_trading_mode(self)
        else:
            logging.get_logger(self.get_name()).error(
                "At least one exchange must be enabled to use SemiAutoTradingMode"
            )

    def get_mode_producer_classes(self) -> list:
        return [SemiAutoTradingModeProducer]

    @classmethod
    def get_supported_exchange_types(cls) -> list:
        """
        :return: The list of supported exchange types
        """
        return [
            trading_enums.ExchangeTypes.SPOT,
            trading_enums.ExchangeTypes.FUTURE,
        ]


class SemiAutoTradingModeProducer(semi_auto_trading_mode.SemiAutoTradingModeMaking):
    async def make_strategy(self, ctx: context_management.Context, action: str):
        self.action = action
        self.ctx = ctx
        await self.make_semi_auto_strategy()
