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

import tentacles.Meta.Keywords.pro_tentacles.strategy_maker.strategy_building_base as strategy_building_base
import tentacles.Meta.Keywords.basic_tentacles.basic_modes.mode_base.abstract_producer_base as abstract_producer_base


class StrategyMakingProducer(
    abstract_producer_base.AbstractBaseModeProducer,
    strategy_building_base.StrategyMakingBaseProducer,
):
    def __init__(self, channel, config, trading_mode, exchange_manager):
        abstract_producer_base.AbstractBaseModeProducer.__init__(
            self, channel, config, trading_mode, exchange_manager
        )
        strategy_building_base.StrategyMakingBaseProducer.__init__(
            self, channel, config, trading_mode, exchange_manager
        )

    # def __init__(self, channel, config, trading_mode, exchange_manager):
    #     super().__init__(channel, config, trading_mode, exchange_manager)
    #     self.default_live_plotting_mode: str = (
    #         matrix_enums.LivePlottingModes.PLOT_RECORDING_MODE.value
    #     )
    #     self.default_backtest_plotting_mode: str = (
    #         matrix_enums.BacktestPlottingModes.DISABLE_PLOTTING.value
    #     )
    #     self.live_plotting_modes: list = [
    #         matrix_enums.LivePlottingModes.DISABLE_PLOTTING.value,
    #         matrix_enums.LivePlottingModes.REPLOT_VISIBLE_HISTORY.value,
    #         matrix_enums.LivePlottingModes.PLOT_RECORDING_MODE.value,
    #     ]
    #     self.backtest_plotting_modes: list = [
    #         matrix_enums.BacktestPlottingModes.ENABLE_PLOTTING.value,
    #         matrix_enums.BacktestPlottingModes.DISABLE_PLOTTING.value,
    #     ]

    #     # TODO
    #     self.debug_mode = True

    #     self.strategy_signals = {}
    #     self.strategy_name = ""
    #     self.is_backtesting = None
    #     self.trigger_time_frames = []
    #     self.nr_of_strategies = 0
    #     self.enable_copy_trading = False
    #     self.candles = {}
    #     self.strategies: typing.Dict[int, init_strategy.StrategyData] = {}
    #     self.evaluators = {}
    #     self.indicators = {}
    #     self.current_strategy_id = None
    #     self.current_evaluator_id = None
    #     self.current_indicator_id = None
    #     self.live_plotting_mode = False
    #     self.live_recording_mode = False
    #     self.enable_plot = True
    #     self.plot_signals = True
    #     self.whitelist_mode = True
    #     self.input_path = None
    #     # self.input_path_backtesting = "trading/Backtesting only settings"
    #     # self.input_path_live = "trading/Live only settings"
    #     self.input_parent_backtesting = "backtesting_settings"
    #     self.input_parent_live = "live_settings"
    #     self.config_path_short = "m"
    #     self.strategy_cache = {}
    #     self.managed_order_indicator_cache = {}
    #     self.all_timestamps = None
    #     self.any_trading_timestamps = None
    #     self.supported_evaluators = supported_evaluators.get_supported_evaluators()
    #     self.ctx = None
    #     self.backtesting_mode = ""
    #     self.trade_analysis_mode_settings = {}
    #     self.all_winrates = {}
    #     self.enable_skip_runs = False
    #     self.skip_runs_balance_below = 0
    #     self.trade_analysis_activated = False
    #     self.current_indicator_time_frame: strategy_builder_enums = None

    # async def build_and_trade_strategies_live(self):
    #     m_time = start_measure_time()
    #     await self.set_position_mode_to_one_way()
    #     await self.init_strategy_maker(is_backtesting=False)
    #     self.allow_trading_only_on_execution(self.ctx)

    #     for strategy_id in range(0, self.nr_of_strategies):
    #         await self.build_and_trade_strategy_live(strategy_id)
    #     if self.enable_copy_trading:
    #         await basic_keywords.emit_trading_signals(self.ctx)
    #     await trade_analysis_activation.handle_trade_analysis_for_current_candle(
    #         self.ctx,
    #         parent_input=self.plot_settings_name,
    #     )
    #     end_measure_live_time(self.ctx, m_time, " strategy maker - live trading")

    # async def build_strategies_backtesting_cache(self, plot_only_mode=False):
    #     s_time = start_measure_time(" strategy maker - building backtesting cache")
    #     await self.init_strategy_maker(is_backtesting=True)

    #     self.all_timestamps = await get_candles_(self, PriceDataSources.TIME.value)
    #     for strategy_id in range(0, self.nr_of_strategies):
    #         await self.build_strategy_backtesting_cache(strategy_id)

    #     (
    #         self.any_trading_timestamps,
    #         trades_count,
    #     ) = await self.merge_signals_in_backtesting()
    #     self.handle_backtesting_timestamp_whitelist(plot_only_mode)

    #     self.trading_mode.set_initialized_trading_pair_by_bot_id(
    #         self.ctx.symbol, self.ctx.time_frame, initialized=True
    #     )
    #     # await handle_trade_analysis_for_backtesting_first_candle(ctx, strategy_maker_data)
    #     end_measure_time(
    #         s_time,
    #         f" strategy maker - building strategy for "
    #         f"{self.ctx.time_frame} {trades_count} trades",
    #     )

    # async def trade_strategies_backtesting(self):
    #     m_time = start_measure_time()
    #     await skip_runs.skip_backtesting_runs_if_condition(
    #         self.ctx, self.skip_runs_balance_below
    #     )
    #     current_signals = self.get_signal_while_backtesting()
    #     for strategy_id in current_signals:
    #         await self.strategies[strategy_id].trade_strategy_backtesting(
    #             self.ctx, self
    #         )
    #     for strategy_id, strategy in self.strategies.items():
    #         if strategy.enable_strategy:
    #             await strategy.handle_trailing_stop(self.ctx, self)

    #     await trade_analysis_activation.handle_trade_analysis_for_current_candle(
    #         self.ctx,
    #         parent_input=self.plot_settings_name,
    #     )
    #     end_measure_time(
    #         m_time,
    #         " strategy maker - warning backtesting candle took longer than expected",
    #         min_duration=1,
    #     )

    # async def get_backtesting_mode(self):
    #     self.backtesting_mode = await basic_keywords.user_input(
    #         self.ctx,
    #         "Backtesting mode",
    #         options=strategy_builder_enums.BacktestingMode.backtesting_options,
    #         input_type="options",
    #         def_val=strategy_builder_enums.BacktestingMode.normal_backtesting_mode,
    #         parent_input_name=self.input_parent_backtesting,
    #     )
    #     return self.backtesting_mode

    # async def init_skip_backtesting_runs(self):
    #     if (
    #         self.backtesting_mode
    #         == strategy_builder_enums.BacktestingMode.normal_backtesting_mode
    #     ):
    #         skip_runs_section = "skip_runs"
    #         await basic_keywords.user_input(
    #             self.ctx,
    #             name=skip_runs_section,
    #             input_type=commons_enums.UserInputTypes.OBJECT,
    #             def_val=None,
    #             title="Backtesting Run Stopper Settings",
    #             parent_input_name=self.input_parent_backtesting,
    #             editor_options={
    #                 "grid_columns": 12,
    #             },
    #             other_schema_values={
    #                 "description": "Whenever a backtest reaches any condition, "
    #                 "all orders get closed and the backtest stops",
    #             },
    #             path="trading",
    #         )
    #         self.enable_skip_runs = await basic_keywords.user_input(
    #             self.ctx,
    #             "enable_skip_backtesting_runs",
    #             "boolean",
    #             title="enable skip backtesting runs",
    #             def_val=False,
    #             show_in_summary=False,
    #             show_in_optimizer=False,
    #             parent_input_name=skip_runs_section,
    #             editor_options={
    #                 "grid_columns": 12,
    #             },
    #         )
    #         if self.enable_skip_runs:
    #             self.skip_runs_balance_below = await basic_keywords.user_input(
    #                 self.ctx,
    #                 "skip_runs_if_below_percent",
    #                 "float",
    #                 title="stop backtesting if balance falls "
    #                 "x percent below original value",
    #                 def_val=40,
    #                 min_val=0,
    #                 max_val=100,
    #                 show_in_summary=False,
    #                 show_in_optimizer=False,
    #                 parent_input_name=skip_runs_section,
    #             )

    # async def init_trade_analysis_mode(self):
    #     if self.backtesting_mode == "Trade analysis mode":
    #         input_parent_trade_analysis_mode = "tamode"
    #         await basic_keywords.user_input(
    #             self.ctx,
    #             name=input_parent_trade_analysis_mode,
    #             input_type=commons_enums.UserInputTypes.OBJECT,
    #             def_val=None,
    #             title="Trade analysis mode settings",
    #             path="trading",
    #             parent_input_name=self.input_parent_backtesting,
    #             other_schema_values={
    #                 "description": "In this mode, order settings will be ignored "
    #                 "and no trades are simulated, in this mode the results are "
    #                 "winrates and other metrics based on the take profit and"
    #                 " stop loss settings provided here",
    #             },
    #             editor_options={
    #                 "grid_columns": 12,
    #             },
    #         )
    #         tp_settings = await basic_keywords.user_input(
    #             self.ctx,
    #             "tam_take_profits_in_percent",
    #             title="Take profits to test in percent (Comma separated)",
    #             input_type="text",
    #             def_val="1.5, 2, 2.5, 3, 4, 5",
    #             show_in_optimizer=False,
    #             parent_input_name=input_parent_trade_analysis_mode,
    #         )
    #         tp_settings = tp_settings.split(",")
    #         tp_settings = [float(ele) for ele in tp_settings]
    #         self.trade_analysis_mode_settings["requested_long_tp"] = tp_settings
    #         self.trade_analysis_mode_settings["requested_short_tp"] = tp_settings
    #         sl_settings = await basic_keywords.user_input(
    #             self.ctx,
    #             "tam_stop_losses_in_percent",
    #             title="Stop losses to test in percent (Comma separated)",
    #             input_type="text",
    #             def_val="0.5, 1, 2, 3, 4",
    #             show_in_optimizer=False,
    #             parent_input_name=input_parent_trade_analysis_mode,
    #         )
    #         sl_settings = sl_settings.split(",")
    #         sl_settings = [float(ele) for ele in sl_settings]
    #         self.trade_analysis_mode_settings["requested_long_sl"] = sl_settings
    #         self.trade_analysis_mode_settings["requested_short_sl"] = sl_settings

    # async def execute_in_trade_analysis_mode(self):
    #     s_time = start_measure_time(" strategy maker - building backtesting cache")
    #     await self.init_strategy_maker(is_backtesting=True)

    #     self.all_timestamps = await get_candles_(self, PriceDataSources.TIME.value)
    #     for strategy_id in range(0, self.nr_of_strategies):
    #         await self.build_strategy_backtesting_cache(strategy_id)
    #     (
    #         self.any_trading_timestamps,
    #         trades_count,
    #     ) = await self.merge_signals_in_backtesting()
    #     end_measure_time(
    #         s_time,
    #         f" strategy maker - building strategy for "
    #         f"{self.ctx.time_frame} {trades_count} trades",
    #     )

    #     s_time = start_measure_time(" strategy maker - trade analysis mode")
    #     self.all_winrates = await handle_trade_analysis_for_backtesting_first_candle(
    #         self.ctx, self
    #     )

    #     skip_runs.register_backtesting_timestamp_whitelist(self.ctx, [])
    #     end_measure_time(s_time, " strategy maker - trade analysis mode")

    # async def init_strategy_maker(self, is_backtesting=False):
    #     self.strategy_signals = {}
    #     self.candles = {}
    #     self.strategies = {}
    #     self.evaluators = {}
    #     self.indicators = {}
    #     self.strategy_cache = {}
    #     self.is_backtesting = is_backtesting

    #     self.ctx.tentacle.script_name = (
    #         self.strategy_name
    #     ) = await basic_keywords.user_input(
    #         self.ctx,
    #         "strategy_name_and_version",
    #         "text",
    #         def_val="my strategy",
    #         title="Strategy name and version",
    #         show_in_optimizer=False,
    #         path=self.input_path,
    #     )

    #     await self.init_plotting_modes(
    #         self.input_parent_live, self.input_parent_backtesting
    #     )
    #     await self.init_user_input_sections()

    #     await set_candles_history_size(self.ctx, 1000)

    #     self.nr_of_strategies = await basic_keywords.user_input(
    #         self.ctx,
    #         "amount_of_strategies",
    #         "int",
    #         def_val=1,
    #         min_val=1,
    #         title="Amount of Strategies",
    #         order=9.5,
    #     )

    #     # await gains.simulate_hedge_fund_gains(ctx)
    #     # if not backtesting_settings.is_registered_backtesting_timestamp_whitelist(ctx):
    #     # final_whitelist = await gains.get_simulated_hedge_fund_gain_timestamps(ctx)
    #     if (
    #         self.backtesting_mode
    #         == strategy_builder_enums.BacktestingMode.normal_backtesting_mode
    #     ):
    #         # if self.nr_of_strategies > 1:
    #         #     self.whitelist_mode = False
    #         # else:
    #         self.whitelist_mode = await basic_keywords.user_inputs.user_input(
    #             self.ctx,
    #             "Whitelist mode: backtest only candles with signals",
    #             "boolean",
    #             def_val=True,
    #             parent_input_name=self.input_parent_backtesting,
    #         )

    #     self.enable_copy_trading = False
    #     if not self.is_backtesting:
    #         self.enable_copy_trading = await basic_keywords.user_inputs.user_input(
    #             self.ctx,
    #             "enable copy trading host",
    #             "boolean",
    #             def_val=False,
    #         )
    #         if self.enable_copy_trading:
    #             await basic_keywords.user_select_emit_trading_signals(
    #                 self.ctx, "my-strategy-id"
    #             )

    #     await self.init_trade_analysis_mode()
    #     await self.init_skip_backtesting_runs()

    # async def build_and_trade_strategy_live(self, strategy_id):
    #     self.current_strategy_id = strategy_id
    #     self.strategies[strategy_id] = init_strategy.StrategyData(self)
    #     await self.strategies[strategy_id].build_and_trade_strategy_live(self, self.ctx)

    # async def build_strategy_backtesting_cache(self, strategy_id):
    #     self.current_strategy_id = strategy_id
    #     self.strategies[strategy_id] = init_strategy.StrategyData(self)
    #     await self.strategies[strategy_id].build_strategy_backtesting_cache(
    #         self, self.ctx
    #     )
    #     self.strategy_signals[strategy_id] = self.strategies[strategy_id].signals

    # async def init_user_input_sections(self):
    #     await basic_keywords.user_input(
    #         self.ctx,
    #         name=self.input_parent_live,
    #         input_type=commons_enums.UserInputTypes.OBJECT,
    #         def_val=None,
    #         title="Live only Settings",
    #         other_schema_values={
    #             "description": "Settings that are only relevant " "for live trading",
    #         },
    #         editor_options={
    #             "grid_columns": 12,
    #         },
    #     )
    #     await basic_keywords.user_input(
    #         self.ctx,
    #         name=self.input_parent_backtesting,
    #         input_type=commons_enums.UserInputTypes.OBJECT,
    #         def_val=None,
    #         title="Backtesting only Settings",
    #         other_schema_values={
    #             "description": "Settings that are only relevant "
    #             "for backtesing and optimizing",
    #         },
    #         editor_options={
    #             "grid_columns": 12,
    #         },
    #     )
    #     await basic_keywords.user_input(
    #         self.ctx,
    #         name=self.plot_settings_name,
    #         input_type=commons_enums.UserInputTypes.OBJECT,
    #         def_val=None,
    #         title="Plot Settings",
    #         editor_options={
    #             "grid_columns": 12,
    #         },
    #         other_schema_values={
    #             "description": "Use those options wisely as it will slow "
    #             "down the backtesting speed. Combined with indicator plotting "
    #             "for backtests, it will be drastically slower. "
    #             "So better use only one at a time or wait longer",
    #         },
    #     )

    # async def merge_signals_in_backtesting(self):
    #     try:
    #         tmp_signals = {}
    #         for strategy_id, signal in self.strategy_signals.items():
    #             for evaluator_id in signal:
    #                 signals_len = -len(signal[evaluator_id] or [])
    #                 times = self.all_timestamps[signals_len:] if signals_len else []
    #                 tmp_signals[f"{strategy_id}-{evaluator_id}"] = pd.Series(
    #                     data=signal[evaluator_id],
    #                     index=times,
    #                     dtype="int8",
    #                 )
    #         signals_df = pd.DataFrame(tmp_signals)
    #         any_signals_df = signals_df
    #         trades_count = 0
    #         for strategy_id, signal in self.strategy_signals.items():
    #             temp_strategy_cache = signals_df
    #             for evaluator_id in signal:
    #                 any_signals_df = any_signals_df[
    #                     (any_signals_df[f"{strategy_id}-{evaluator_id}"] == 1)
    #                 ]
    #                 temp_strategy_cache = temp_strategy_cache[
    #                     (temp_strategy_cache[f"{strategy_id}-{evaluator_id}"] == 1)
    #                 ]
    #             trades_count += self.store_backtesting_signals_cache(
    #                 temp_strategy_cache.index.values, strategy_id
    #             )

    #         await self.handle_plot_signals()

    #         # signals times
    #         return any_signals_df.index.values, trades_count
    #     except ValueError:
    #         return [], 0

    # async def handle_plot_signals(self):
    #     if self.plot_signals:
    #         signals_by_strategies = {}
    #         for timestamp, strategies in self.strategy_cache.items():
    #             for strategy_id in strategies.keys():
    #                 if strategy_id not in signals_by_strategies:
    #                     signals_by_strategies[strategy_id] = [[], []]
    #                 signals_by_strategies[strategy_id][0].append(timestamp)
    #                 signals_by_strategies[strategy_id][1].append(strategy_id)
    #         for strategy_id, signals in signals_by_strategies.items():
    #             value_key = f"sgnls_s{strategy_id+1}"
    #             await self.ctx.set_cached_values(
    #                 values=signals[1],
    #                 cache_keys=signals[0],
    #                 value_key=value_key,
    #             )
    #             await plotting.plot(
    #                 self.ctx,
    #                 f"Strategy {strategy_id+1}",
    #                 cache_value=value_key,
    #                 mode="markers",
    #                 chart="main-chart",
    #                 color="green",
    #             )

    # def store_backtesting_signals_cache(self, trading_timestamps, strategy_id):
    #     trade_count = 0
    #     if self.strategies[strategy_id].enable_strategy:
    #         for timestamp_id in trading_timestamps:
    #             if timestamp_id not in self.strategy_cache:
    #                 self.strategy_cache[timestamp_id] = {}
    #             self.strategy_cache[timestamp_id][strategy_id] = self.strategies[
    #                 strategy_id
    #             ].trading_side_key
    #             trade_count += 1
    #     return trade_count

    # def get_signal_while_backtesting(self):
    #     try:
    #         return self.strategy_cache[self.ctx.trigger_cache_timestamp]
    #     except KeyError:
    #         return []

    # def handle_backtesting_timestamp_whitelist(self, plot_only_mode):
    #     final_whitelist = []
    #     if plot_only_mode:
    #         skip_runs.register_backtesting_timestamp_whitelist(
    #             self.ctx, final_whitelist
    #         )
    #     else:
    #         time_frame_sec = (
    #             commons_enums.TimeFramesMinutes[
    #                 commons_enums.TimeFrames(self.ctx.time_frame)
    #             ]
    #             * 60
    #         )
    #         for timestamp in self.any_trading_timestamps:
    #             final_whitelist.append(timestamp - time_frame_sec)
    #             final_whitelist.append(timestamp)
    #         if self.whitelist_mode and len(self.trigger_time_frames) == 1:
    #             skip_runs.register_backtesting_timestamp_whitelist(
    #                 self.ctx, final_whitelist
    #             )

    # def get_current_strategy(self):
    #     return self.strategies[self.current_strategy_id]

    # def get_supported_shared_conf_indicators(self, indicator):
    #     source_list = ["this indicator"]
    #     sources_available = False
    #     for indicator_key, _indicator in self.indicators.items():
    #         if indicator.indicator_class_name == _indicator.indicator_class_name:
    #             source_list.append(indicator_key)
    #             sources_available = True
    #     return source_list, sources_available
