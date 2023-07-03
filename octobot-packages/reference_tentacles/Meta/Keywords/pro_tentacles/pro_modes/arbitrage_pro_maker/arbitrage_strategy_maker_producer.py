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

from __future__ import annotations
import typing
from octobot_trading.modes.script_keywords import basic_keywords

import octobot_trading.modes.script_keywords.context_management as context_management
import octobot_trading.modes as trading_modes
import octobot_trading.enums as trading_enums
import octobot_trading.constants as trading_constants
import octobot_trading.errors as errors
import octobot_trading.exchange_channel as exchanges_channel
import octobot_trading.api as api

import octobot_commons.databases as databases
import octobot_commons.enums as commons_enums
import octobot_commons.errors as commons_errors
import octobot_commons.constants as commons_constants
import tentacles.Meta.Keywords.RunAnalysis.AnalysisKeywords.analysis_enums as analysis_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data as public_exchange_data
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders import (
    expired_orders_cancelling,
)
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as basic_utilities
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.pro_tentacles.pro_modes.indicator_only_mode as indicator_only_mode
import tentacles.Meta.Keywords.pro_tentacles.trade_analysis.trade_analysis_activation as trade_analysis_activation
import tentacles.Meta.Keywords.pro_tentacles.evaluators.supported_evaluators as supported_evaluators
import tentacles.Meta.Keywords.pro_tentacles.strategy_maker.init_strategy as init_strategy
import tentacles.Meta.Keywords.pro_tentacles.strategy_maker.strategy_building_base as strategy_building_base


STRATEGIES_SETTINGS_TAB_NAME: str = "strategies_settings_tab"


class ArbitrageProStrategyMakerProducer(
    trading_modes.AbstractTradingModeProducer,
    strategy_building_base.StrategyMakingBaseProducer,
):
    current_strategy_id = None
    supported_evaluators = supported_evaluators.get_supported_evaluators()
    enable_plot = True
    default_live_plotting_mode: str = (
        matrix_enums.LivePlottingModes.PLOT_RECORDING_MODE.value
    )
    default_backtest_plotting_mode: str = (
        matrix_enums.BacktestPlottingModes.DISABLE_PLOTTING.value
    )
    live_plotting_modes: list = [
        matrix_enums.LivePlottingModes.DISABLE_PLOTTING.value,
        matrix_enums.LivePlottingModes.REPLOT_VISIBLE_HISTORY.value,
        matrix_enums.LivePlottingModes.PLOT_RECORDING_MODE.value,
    ]
    backtest_plotting_modes: list = [
        matrix_enums.BacktestPlottingModes.ENABLE_PLOTTING.value,
        matrix_enums.BacktestPlottingModes.DISABLE_PLOTTING.value,
    ]

    backtest_plotting_mode = matrix_enums.BacktestPlottingModes.ENABLE_PLOTTING
    live_plotting_mode = matrix_enums.LivePlottingModes.REPLOT_VISIBLE_HISTORY
    last_calls_by_bot_id_and_time_frame: dict = {}

    # TODO remove when order storage update is ready
    #   then no other candle callbacks are required to plt orders
    SHOULD_REMOVE_CANDLE_CALLBACK_AFTER_INIT: bool = False

    BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR: dict = {}
    LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR: dict = {}

    def __init__(self, channel, config, trading_mode, exchange_manager):
        trading_modes.AbstractTradingModeProducer.__init__(
            self, channel, config, trading_mode, exchange_manager
        )
        strategy_building_base.StrategyMakingBaseProducer.__init__(
            self, channel, config, trading_mode, exchange_manager
        )
        # TODO
        self.debug_mode = True

        self.strategy_signals = {}
        self.strategy_name = ""
        # self.is_backtesting = None
        # self.trigger_time_frames = []
        self.nr_of_strategies = 2
        self.candles = {}
        self.strategies: typing.Dict[int, init_strategy.StrategyData] = {}
        self.evaluators = {}
        self.indicators = {}
        self.current_evaluator_id = None
        self.current_indicator_id = None
        self.live_plotting_mode = False
        self.live_recording_mode = False
        self.plot_signals = True
        # self.whitelist_mode = True
        self.input_path = None
        self.input_parent_backtesting = "backtesting_settings"
        self.input_parent_live = "live_settings"
        self.config_path_short = "m"
        self.strategy_cache = {}
        self.managed_order_indicator_cache = {}
        self.all_timestamps = None
        self.any_trading_timestamps = None
        self.ctx: context_management.Context = None
        self.backtesting_mode = ""
        self.trade_analysis_mode_settings = {}
        self.all_winrates = {}
        self.consumable_indicator_cache = {}
        self.standalone_indicators = {}
        self.enable_skip_runs = False
        self.skip_runs_balance_below = 0
        self.trade_analysis_activated = False

        self.is_backtesting_first_call: bool = True
        self.is_backtesting_second_call: bool = False

        self.candle_callbacks_consumers_by_pair: dict[str, dict] = {}
        # self.current_indicator_time_frame: strategy_builder_enums = None

    async def _start_strategy_maker_candle_callback(self, is_backtesting):
        """
        This adds a callback to generate strategy signals
            or data to analyse on each bar close
            for every exchange
        """
        if self.exchange_manager.id not in self.candle_callbacks_consumers_by_pair:
            self.candle_callbacks_consumers_by_pair[self.exchange_manager.id] = {}
        self.candle_callbacks_consumers_by_pair[self.exchange_manager.id][
            self.trading_mode.symbol
        ] = await exchanges_channel.get_chan(
            trading_constants.OHLCV_CHANNEL, self.exchange_manager.id
        ).new_consumer(
            self.candle_callback, symbol=self.trading_mode.symbol
        )

    async def stop_strategy_maker_candle_callback(self):
        """
        will be called in a backtest when candle callbacks arent required anymore
        """
        await exchanges_channel.get_chan(
            trading_constants.OHLCV_CHANNEL, self.exchange_manager.id
        ).remove_consumer(
            self.candle_callbacks_consumers_by_pair[self.exchange_manager.id][
                self.trading_mode.symbol
            ]
        )

    async def call_strategy_maker(self, exchange_name):
        if self.ctx.exchange_manager.is_backtesting:
            await self.call_strategy_maker_backtesting(exchange_name)
        else:
            # live uses candle_callback -  backtesting uses mark_price_callback
            await expired_orders_cancelling.cancel_expired_orders_for_this_candle(
                self.ctx,
                tag="entry",
                limit_max_age_in_bars=self.trading_mode.arbitrage_settings.cancel_expired_orders_minutes,
                time_frame=commons_enums.TimeFrames.ONE_MINUTE,
            )
            await self.call_strategy_maker_live(exchange_name)

    async def call_strategy_maker_backtesting(self, exchange_name):
        # TODO remove when order storage is ready
        await trade_analysis_activation.handle_trade_analysis_for_current_candle(
            self.ctx, parent_input=None  # self.plot_settings_name,
        )

        if self.is_backtesting_second_call:
            self.is_backtesting_second_call = False
            # generate data to analyse on the chart later on
            await indicator_only_mode.run_indicator_only_mode(self)
            if self.SHOULD_REMOVE_CANDLE_CALLBACK_AFTER_INIT:
                # remove the candle callback after the second bar when backtesting
                # as the cache and data gets generated on the first and second bar
                await self.stop_strategy_maker_candle_callback()

        elif self.is_backtesting_first_call:
            self.is_backtesting_first_call = False
            self.is_backtesting_second_call = True
            if self.is_trend_strategy():
                s_time = basic_utilities.start_measure_time(
                    " strategy maker - building backtesting cache"
                )
                # TODO allow settings
                # await self.init_strategy_maker(is_backtesting=True)

                self.all_timestamps = await public_exchange_data.get_candles_(
                    self, matrix_enums.PriceDataSources.TIME.value
                )
                if (
                    exchange_name
                    not in self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR
                ):
                    self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name] = {}
                if (
                    self.ctx.symbol
                    not in self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR[
                        exchange_name
                    ]
                ):
                    self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name][
                        self.ctx.symbol
                    ] = {}
                for strategy_id in range(self.nr_of_strategies):
                    await self.build_strategy_backtesting_cache(strategy_id)
                (
                    self.any_trading_timestamps,
                    trades_count,
                ) = await self.merge_signals_in_backtesting()

                self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name][
                    self.ctx.symbol
                ] = self.strategy_cache
                # TODO handle whitelist mode
                self.handle_backtesting_timestamp_whitelist(
                    plot_only_mode=False,
                    any_trading_timestamps=self.any_trading_timestamps,
                )
                # self.trading_mode.set_initialized_trading_pair_by_bot_id(
                #     self.ctx.symbol, self.ctx.time_frame, initialized=True
                # )
                basic_utilities.end_measure_time(
                    s_time,
                    f" strategy maker - building strategy for "
                    f"{self.ctx.time_frame} / {trades_count} candles allowed to trade",
                )

    async def call_strategy_maker_live(self, exchange_name):
        # TODO only execute when trend_exchange
        # user inputs not loading properly when skipped
        # if self.exchange_name in self.trading_mode.arbitrage_settings.trend_exchanges:

        # TODO allow settings
        # await self.init_strategy_maker(is_backtesting=True)
        await basic_keywords.user_input(
            self.ctx,
            STRATEGIES_SETTINGS_TAB_NAME,
            input_type="object",
            title="Arbitrage Filter Strategies",
            def_val=None,
            path=self.input_path,
            editor_options={
                "grid_columns": 12,
                analysis_enums.UserInputEditorOptionsTypes.ANT_ICON.value: "FilterOutlined",
            },
            other_schema_values={
                matrix_enums.UserInputOtherSchemaValuesTypes.DISPLAY_AS_TAB.value: True,
                analysis_enums.UserInputOtherSchemaValuesTypes.TAB_ORDER.value: -1,
            },
        )
        for strategy_id in range(self.nr_of_strategies):
            self.current_strategy_id = strategy_id
            self.strategies[
                self.current_strategy_id
            ]: init_strategy.StrategyData = init_strategy.StrategyData(
                self, parent_input_name=STRATEGIES_SETTINGS_TAB_NAME
            )
            self.strategies[self.current_strategy_id].trading_side = (
                matrix_enums.TradingSidesNames.LONG
                if strategy_id == 0
                else matrix_enums.TradingSidesNames.SHORT
            )
            self.strategies[self.current_strategy_id].trading_side_key = (
                matrix_enums.TradingSideKeys.LONG
                if strategy_id == 0
                else matrix_enums.TradingSideKeys.SHORT
            )
            signal = bool(
                await self.strategies[
                    self.current_strategy_id
                ].build_and_trade_strategy_live(self, self.ctx, strategy_only=True)
            )

            # await self.merge_signals_in_backtesting()

            if exchange_name not in self.LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR:
                self.LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name] = {}
            if (
                self.ctx.symbol
                not in self.LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name]
            ):
                self.LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name][
                    self.ctx.symbol
                ] = {}
            self.LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name][self.ctx.symbol][
                strategy_id
            ] = signal

            if any(
                self.exchange_name == trend_exchange
                for trend_exchange in self.trading_mode.arbitrage_settings.trend_exchanges
            ):
                self.logger.info(
                    f"Strategy {strategy_id} "
                    f"{'allowed to trade' if signal else 'not allowed to trade'} on"
                    f" {exchange_name} {self.ctx.symbol} {self.ctx.time_frame}"
                )
        await trade_analysis_activation.handle_trade_analysis_for_current_candle(
            self.ctx, parent_input=None  # self.plot_settings_name,
        )
        await indicator_only_mode.run_indicator_only_mode(self)

    async def get_strategy_signal(
        self,
        traded_exchange_name,
        trading_side: trading_enums.EvaluatorStates,
        symbol: str,
    ) -> bool:
        exchange_settings = self.trading_mode.arbitrage_settings.exchange_settings[
            traded_exchange_name
        ]
        if trading_side == trading_enums.EvaluatorStates.LONG:
            strategy_id = exchange_settings.long_strategy_id - 1
        elif trading_side == trading_enums.EvaluatorStates.SHORT:
            strategy_id = exchange_settings.short_strategy_id - 1
        if self.exchange_manager.is_backtesting:
            return await self.get_backtesting_strategy_signal(
                strategy_id, exchange_settings, symbol
            )
        else:
            return self.get_live_strategy_signal(strategy_id, exchange_settings, symbol)

    async def get_backtesting_strategy_signal(
        self,
        strategy_id: int,
        exchange_settings,
        symbol: str,
    ) -> bool:
        signals_cache = self.get_evaluation_mode_producer(
            exchange_settings
        ).BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR[
            exchange_settings.evaluation_exchange
        ][
            symbol
        ]
        if api.get_exchange_current_time(self.exchange_manager) in signals_cache.get(
            strategy_id, []
        ):
            return True
        return False

    def get_live_strategy_signal(
        self,
        strategy_id: int,
        exchange_settings,  #: arbitrage_pro_settings.ArbitrageProExchangeSettings,
        symbol: str,
    ) -> bool:
        try:
            return self.get_evaluation_mode_producer(
                exchange_settings
            ).LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR[
                exchange_settings.evaluation_exchange
            ][
                symbol
            ][
                strategy_id
            ]
        except KeyError:
            self.ctx.logger.warning(
                f"No strategy signal for strategy {strategy_id} - "
                f"{exchange_settings.evaluation_exchange} - {symbol} stored in cache. "
            )
            return False
        except IndexError:
            # this should never happen
            self.ctx.logger.error(
                f"Failed to get live strategy signal for strategy {strategy_id}. "
                "Error: not able to get the strategy producer"
            )
            return False

    async def candle_callback(
        self,
        exchange: str,
        exchange_id: str,
        cryptocurrency: str,
        symbol: str,
        time_frame: str,
        candle: dict,
        trigger_source=commons_enums.ActivationTopics.FULL_CANDLES.value,
    ):
        async with self.trading_mode_trigger():
            # add a full candle to time to get the real time
            trigger_time = (
                candle[commons_enums.PriceIndexes.IND_PRICE_TIME.value]
                + commons_enums.TimeFramesMinutes[commons_enums.TimeFrames(time_frame)]
                * commons_constants.MINUTE_TO_SECONDS
            )
            if time_frame in self.time_frame_filter:
                self.log_last_call_by_exchange_id(
                    matrix_id=self.matrix_id,
                    exchange=exchange,
                    cryptocurrency=cryptocurrency,
                    symbol=symbol,
                    time_frame=time_frame,
                    trigger_cache_timestamp=trigger_time,
                    candle=candle,
                )
                await self.pre_strategy_maker_call(
                    self.matrix_id,
                    exchange=exchange,
                    cryptocurrency=cryptocurrency,
                    symbol=symbol,
                    time_frame=time_frame,
                    trigger_cache_timestamp=trigger_time,
                    candle=candle,
                )

    def is_trend_strategy(self, exchange_name: str = None) -> bool:
        exchange_name = exchange_name or self.exchange_name
        return exchange_name in self.trading_mode.arbitrage_settings.trend_exchanges

    async def pre_strategy_maker_call(
        self,
        matrix_id,
        exchange,
        cryptocurrency,
        symbol,
        time_frame,
        trigger_cache_timestamp,
        candle,
    ):
        self.ctx = context_management.get_full_context(
            trading_mode=self.trading_mode,
            matrix_id=matrix_id,
            cryptocurrency=cryptocurrency,
            symbol=symbol,
            time_frame=time_frame,
            trigger_source=commons_enums.ActivationTopics.FULL_CANDLES.value,
            trigger_cache_timestamp=trigger_cache_timestamp,
            candle=candle,
            kline=None,
            init_call=False,
        )

        self.ctx.matrix_id = matrix_id
        self.ctx.cryptocurrency = cryptocurrency
        self.ctx.symbol = symbol
        self.ctx.time_frame = time_frame
        initialized = True
        run_data_writer = databases.RunDatabasesProvider.instance().get_run_db(
            self.exchange_manager.bot_id
        )
        try:
            # if self.exchange_name in self.trading_mode.trend_exchanges:
            await self.call_strategy_maker(exchange)
        except errors.UnreachableExchange:
            raise
        except (
            commons_errors.MissingDataError,
            commons_errors.ExecutionAborted,
        ) as error:
            self.logger.debug(f"Strategy evaluation aborted: {error}")
            initialized = run_data_writer.are_data_initialized
        except Exception as error:
            self.logger.exception(error, True, f"Strategy evaluation failed: {error}")
        finally:
            if not self.exchange_manager.is_backtesting:
                if self.ctx.has_cache(self.ctx.symbol, self.ctx.time_frame):
                    await self.ctx.get_cache().flush()
                for symbol in self.exchange_manager.exchange_config.traded_symbol_pairs:
                    await databases.RunDatabasesProvider.instance().get_symbol_db(
                        self.exchange_manager.bot_id,
                        self.exchange_manager.exchange_name,
                        symbol,
                    ).flush()
            run_data_writer.set_initialized_flags(initialized)
            databases.RunDatabasesProvider.instance().get_symbol_db(
                self.exchange_manager.bot_id, self.exchange_name, symbol
            ).set_initialized_flags(initialized, (time_frame,))

    def log_last_call_by_exchange_id(
        self,
        matrix_id,
        exchange,
        cryptocurrency,
        symbol,
        time_frame,
        trigger_cache_timestamp,
        candle,
    ):
        if self.exchange_manager.bot_id not in self.last_calls_by_bot_id_and_time_frame:
            self.last_calls_by_bot_id_and_time_frame[self.exchange_manager.bot_id] = {}
        if (
            time_frame
            not in self.last_calls_by_bot_id_and_time_frame[
                self.exchange_manager.bot_id
            ]
        ):
            self.last_calls_by_bot_id_and_time_frame[self.exchange_manager.bot_id][
                time_frame
            ] = {}

        self.last_calls_by_bot_id_and_time_frame[self.exchange_manager.bot_id][
            time_frame
        ][symbol] = (
            matrix_id,
            exchange,
            cryptocurrency,
            symbol,
            time_frame,
            trigger_cache_timestamp,
            candle,
        )

    async def post_trigger(self):
        if not self.exchange_manager.is_backtesting:
            # update db after each run only in live mode
            for database in self.all_databases().values():
                if database:
                    try:
                        await database.flush()
                    except Exception as err:
                        self.logger.exception(
                            err, True, f"Error when flushing database: {err}"
                        )

    def get_evaluation_mode_producer(
        self, exchange_settings
    ) -> ArbitrageProStrategyMakerProducer:
        """
        get the producer for the trend evaluation strategy
        """
        return (
            self.exchange_managers_by_exchange_name[
                exchange_settings.evaluation_exchange
            ]
            .trading_modes[0]
            .producers[0]
        )
