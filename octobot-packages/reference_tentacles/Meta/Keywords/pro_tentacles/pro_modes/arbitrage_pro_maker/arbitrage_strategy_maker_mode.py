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

import time

import octobot_commons.enums as commons_enums
import octobot_commons.constants as commons_constants
import octobot_commons.databases as databases
import octobot_trading.modes.modes_util as modes_util
import octobot_trading.modes as trading_modes


class ArbitrageProStrategyMakerMode(trading_modes.AbstractTradingMode):
    INITIALIZED_TRADING_PAIR_BY_BOT_ID = {}
    enable_ping_pong: bool = False

    def __init__(self, config, exchange_manager):
        super().__init__(config, exchange_manager)
        self.timestamp = time.time()

    async def user_commands_callback(self, bot_id, subject, action, data) -> None:
        # do not call super as reload_config is called by reload_scripts already
        # on RELOAD_CONFIG command
        self.logger.debug(f"Received {action} command")
        if action == commons_enums.UserCommands.RELOAD_CONFIG.value:
            # also reload script on RELOAD_CONFIG
            await self.reload_config(bot_id)
            await self.start_over_database()
            self.logger.debug("Reloaded configuration")
        elif action == commons_enums.UserCommands.CLEAR_PLOTTING_CACHE.value:
            await modes_util.clear_plotting_cache(self)
        elif action == commons_enums.UserCommands.CLEAR_SIMULATED_ORDERS_CACHE.value:
            await modes_util.clear_simulated_orders_cache(self)

    async def start_over_database(self):
        await modes_util.clear_plotting_cache(self)
        symbol_db = databases.RunDatabasesProvider.instance().get_symbol_db(
            self.bot_id, self.exchange_manager.exchange_name, self.symbol
        )
        symbol_db.set_initialized_flags(False)
        for producer in self.producers:
            for (
                time_frame,
                call_args_by_symbols,
            ) in producer.last_calls_by_bot_id_and_time_frame[
                self.exchange_manager.bot_id
            ].items():
                if self.symbol in call_args_by_symbols:
                    run_db = databases.RunDatabasesProvider.instance().get_run_db(
                        self.bot_id
                    )
                    await producer.init_user_inputs(False)
                    run_db.set_initialized_flags(False, (time_frame,))
                    await databases.CacheManager().close_cache(
                        commons_constants.UNPROVIDED_CACHE_IDENTIFIER,
                        reset_cache_db_ids=True,
                    )
                    await producer.pre_strategy_maker_call(
                        *call_args_by_symbols[self.symbol],
                    )
                    await run_db.flush()
                else:
                    self.logger.debug(
                        "Wont't call strategy maker as last_calls_by_bot_id_and_time_frame "
                        f"is not initialized for {self.symbol}."
                    )
