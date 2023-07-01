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


import octobot_commons.enums as commons_enums
from octobot_trading.api.exchange import (
    get_all_exchange_ids_from_matrix_id,
    get_exchange_managers_from_exchange_ids,
)
from octobot_trading.modes.script_keywords.basic_keywords.user_inputs import user_input
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums


class RealTimeStrategy:
    def __init__(self, symbol, exchange_name, trigger_price, trigger_operator):
        self.activated = True
        self.symbol: list = symbol
        self.exchange_name: list = exchange_name
        self.trigger_price: list = trigger_price
        self.trigger_operator: list = trigger_operator

    def update_strategy(self, symbol, exchange_name, trigger_price, trigger_operator):
        self.symbol: list = symbol
        self.exchange_name: list = exchange_name
        self.trigger_price: list = trigger_price
        self.trigger_operator: list = trigger_operator

    def disable_strategy(self):
        self.activated = False


class TriggerOperators:
    GREATER_THEN = ">"
    LESS_THEN = "<"
    DISABLED = "disabled"
    AVAILABLE: list = [DISABLED, GREATER_THEN, LESS_THEN]


class RealTimeStrategies:
    activated: bool = False
    strategies: dict = {}

    def activate_strategy(self):
        self.activated = True

    def disable_strategies(self):
        self.activated = False
        self.clear_strategies_cache()

    def clear_strategies_cache(self):
        self.strategies: dict = {}

    async def run_real_time_strategies(
        self,
        trading_mode,
        exchange: str,
        exchange_id: str,
        symbol: str,
        mark_price,
    ):
        if self.activated:
            strategy_settings: RealTimeStrategy = self._get_strategy_settings(
                exchange, symbol
            )
            if strategy_settings and strategy_settings.activated:
                if strategy_settings.trigger_operator == TriggerOperators.GREATER_THEN:
                    if mark_price > strategy_settings.trigger_price:
                        await self._call_trading_mode(trading_mode, exchange_id, symbol)
                        strategy_settings.disable_strategy()  # only call once
                elif strategy_settings.trigger_operator == TriggerOperators.LESS_THEN:
                    if mark_price < strategy_settings.trigger_price:
                        await self._call_trading_mode(trading_mode, exchange_id, symbol)
                        strategy_settings.disable_strategy()  # only call once

    async def _call_trading_mode(self, trading_mode, exchange_id, symbol):
        for producer in trading_mode.producers:
            for (
                call_args_by_symbols
            ) in producer.last_calls_by_time_frame_and_symbol.values():
                if symbol in call_args_by_symbols:
                    return await producer.call_script(
                        *call_args_by_symbols[symbol],
                        action=matrix_enums.TradingModeCommands.EXECUTE,
                    )

    async def create_real_time_strategy(
        self,
        maker,
        symbols,
        parent_user_input_name: str = None,
        input_suffix: str = "1",  # must be unique
        title_name: str = "1",
    ):
        if maker.trading_mode.enable_real_time_strategy:
            this_strategy_settings_name = f"real_time_strategy_{input_suffix}"
            await user_input(
                maker.ctx,
                this_strategy_settings_name,
                commons_enums.UserInputTypes.OBJECT.value,
                None,
                title=f"Real time strategy {title_name}",
                show_in_optimizer=False,
                show_in_summary=False,
                parent_input_name=parent_user_input_name,
                editor_options={
                    commons_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
                    commons_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
                    commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
                },
            )

            trigger_operator: list = await user_input(
                maker.ctx,
                f"real_time_strategy_trigger_operator_{input_suffix}",
                commons_enums.UserInputTypes.OPTIONS.value,
                TriggerOperators.DISABLED,
                options=TriggerOperators.AVAILABLE,
                title="Trigger operator",
                show_in_optimizer=False,
                show_in_summary=False,
                parent_input_name=this_strategy_settings_name,
                other_schema_values={
                    "description": "Will compare like this: mark_price < trigger_price",
                },
            )
            if TriggerOperators.DISABLED != trigger_operator:
                trigger_price: list = await user_input(
                    maker.ctx,
                    f"real_time_strategy_trigger_price_{input_suffix}",
                    commons_enums.UserInputTypes.FLOAT.value,
                    100,
                    title="Trigger price",
                    show_in_optimizer=False,
                    show_in_summary=False,
                    parent_input_name=this_strategy_settings_name,
                )
                valid_on_symbols: list = {}
                if len(symbols) > 1:
                    valid_on_symbols: list = await user_input(
                        maker.ctx,
                        f"real_time_strategy_symbols_{input_suffix}",
                        commons_enums.UserInputTypes.MULTIPLE_OPTIONS.value,
                        symbols[0],
                        options=symbols,
                        title="Symbols to execute this strategy on",
                        show_in_optimizer=False,
                        show_in_summary=False,
                        parent_input_name=this_strategy_settings_name,
                    )
                else:
                    valid_on_symbols = symbols
                matrix_id = maker.ctx.matrix_id
                exchange_ids = get_all_exchange_ids_from_matrix_id(matrix_id)
                exchange_managers = get_exchange_managers_from_exchange_ids(
                    exchange_ids
                )
                exchanges = [
                    exchange_manager.exchange_name
                    for exchange_manager in exchange_managers
                ]
                if len(exchanges) > 1:
                    valid_on_exchanges: list = await user_input(
                        maker.ctx,
                        f"real_time_strategy_exchanges_{input_suffix}",
                        commons_enums.UserInputTypes.MULTIPLE_OPTIONS.value,
                        exchanges[0],
                        options=exchanges,
                        title="Exchanges to execute this strategy on",
                        show_in_optimizer=False,
                        show_in_summary=False,
                        parent_input_name=this_strategy_settings_name,
                    )
                else:
                    valid_on_exchanges = exchanges
                self._cache_strategy_settings(
                    valid_on_exchanges,
                    valid_on_symbols,
                    trigger_price,
                    trigger_operator,
                )

    def _get_strategy_settings(
        self, exchange_name: str, symbol: str
    ) -> RealTimeStrategy:
        try:
            return self.strategies[exchange_name][symbol]
        except KeyError:
            pass

    def _cache_strategy_settings(
        self,
        valid_on_exchanges,
        valid_on_symbols,
        trigger_price,
        trigger_operator,
    ) -> None:
        for symbol in valid_on_symbols:
            for exchange_name in valid_on_exchanges:
                if exchange_name not in self.strategies:
                    self.strategies[exchange_name] = {}
                if symbol in self.strategies[exchange_name]:
                    self.strategies[exchange_name][symbol].update_strategy(
                        symbol, exchange_name, trigger_price, trigger_operator
                    )
                else:
                    self.strategies[exchange_name][symbol] = RealTimeStrategy(
                        symbol=symbol,
                        exchange_name=exchange_name,
                        trigger_price=trigger_price,
                        trigger_operator=trigger_operator,
                    )
