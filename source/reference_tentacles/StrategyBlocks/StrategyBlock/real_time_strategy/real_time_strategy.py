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

import typing
import numpy
from octobot_commons.enums import ActivationTopics, PlotCharts
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)
from tentacles.Meta.Keywords.block_factory import (
    abstract_action_block,
    abstract_entry_order_block,
)
import tentacles.Meta.Keywords.block_factory.abstract_strategy_block as abstract_strategy_block
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums


class RealTimeStrategy(abstract_strategy_block.StrategyBlock):
    NAME = "real_time_strategy"
    TITLE = "Real Time Based Strategy"
    TITLE_SHORT = "Real Time Strategy"
    DESCRIPTION = (
        "Make sure to enable 'once per second' as a strategy trigger. "
        "The real time based strategy can be used to trade on each websocket update. "
        "Note that this mode doesnt support backtesting yet. "
    )

    enable_strategy: bool
    signal_color: block_factory_enums.Colors
    enable_plot: bool
    live_recording_mode: bool
    trigger_time_frames: list
    trigger_pairs: list
    chart_location: typing.Optional[str]

    def init_block_settings(self) -> None:
        self.trigger_time_frames: list = self.user_select_trigger_time_frames()
        self.trigger_pairs: list = self.user_select_trigger_pairs()
        self.enable_plot = True
        backtest_plotting_mode: matrix_enums.BacktestPlottingModes = (
            matrix_enums.BacktestPlottingModes.ENABLE_PLOTTING
        )
        live_plotting_mode: matrix_enums.LivePlottingModes = (
            matrix_enums.LivePlottingModes.REPLOT_VISIBLE_HISTORY
        )
        self.live_recording_mode = False
        if (
            self.trading_mode.exchange_manager.is_backtesting
            and backtest_plotting_mode
            == matrix_enums.BacktestPlottingModes.ENABLE_PLOTTING
        ) or (
            backtest_plotting_mode == matrix_enums.BacktestPlottingModes.ENABLE_PLOTTING
            or live_plotting_mode
            in (
                matrix_enums.LivePlottingModes.PLOT_RECORDING_MODE,
                matrix_enums.LivePlottingModes.REPLOT_VISIBLE_HISTORY,
            )
        ):
            self.enable_plot = self.user_input(
                "enable_plots",
                "boolean",
                title="Plot Strategy Signals",
                def_val=True,
            )
            if self.enable_plot:
                self.signal_color = self.user_select_color(
                    name="signal_color",
                    default_color=block_factory_enums.Colors.GREEN,
                    title="Strategy Signal Color",
                )
                self.chart_location = self.user_select_chart_location(
                    default_chart_location=PlotCharts.MAIN_CHART.value,
                    title="Strategy Signal Chart Location",
                    name=f"chart_{self.NAME}",
                )
        self.register_strategy_start_output_node(
            title="Strategy Trigger", output_node_plot_enabled=self.enable_plot
        )

        self.strategy_variations = None
        self.strategy_variations_cache = None

    strategy_variations: typing.List[abstract_strategy_block.StrategySignals]
    strategy_variations_cache: typing.List[abstract_strategy_block.StrategySignals]

    async def execute_block(
        self,
    ) -> None:
        if self.is_allowed_to_trade():
            s_time = None
            if self.is_live_or_doesnt_have_cache():
                s_time = await self.generate_signals()
            await self.execute_signals(s_time)
            await self.execute_cron_jobs()

    def is_live_or_doesnt_have_cache(self):
        return (
            not self.block_factory.ctx.exchange_manager.is_backtesting
            or not self.strategy_variations
        )

    def is_allowed_to_trade(self):
        return (
            self.block_factory.ctx.trigger_source
            == ActivationTopics.IN_CONSTRUCTION_CANDLES.value
            and self.block_factory.ctx.time_frame in self.trigger_time_frames
            and self.block_factory.ctx.symbol in self.trigger_pairs
        )

    async def execute_cron_jobs(self):
        for strategy_variation in self.strategy_variations_cache:
            strategy_variation: abstract_strategy_block.StrategySignals
            for action_block in strategy_variation.actions:
                if isinstance(action_block, abstract_action_block.ActionBlock):
                    await action_block.execute_cron_jobs(
                        self.block_factory, triggering_block=self
                    )

    async def execute_signals(self, s_time: float):
        trades_count = 0
        for strategy_variation in self.strategy_variations_cache:
            if (
                self.block_factory.ctx.trigger_cache_timestamp
                in strategy_variation.signals_cache
            ):
                for action_block in strategy_variation.actions:
                    if isinstance(
                        action_block, abstract_entry_order_block.EntryOrderBlock
                    ):
                        trades_count += 1
                    await action_block.execute_block_from_factory(
                        self.block_factory, triggering_block=self
                    )
        if not self.block_factory.ctx.exchange_manager.is_backtesting and s_time:
            self.block_factory.end_measure_time(
                s_time,
                f"building strategy for {trades_count} trades on {self.block_factory.ctx.symbol} "
                f"{self.block_factory.ctx.time_frame} {self.block_factory.ctx.exchange_name}",
            )

    async def generate_signals(self) -> float:
        s_time = self.block_factory.start_measure_time(
            f"building strategy on {self.block_factory.ctx.symbol} "
            f"{self.block_factory.ctx.time_frame} {self.block_factory.ctx.exchange_name}"
        )
        trades_count = 0
        self.strategy_variations = []
        self.strategy_variations_cache = []
        await self.get_strategy_signals()
        timestamps = None
        candles_closes = None
        whitelist_timestamps = []
        for strategy_variation in self.strategy_variations:
            strategy_variation: abstract_strategy_block.StrategySignals
            if len(strategy_variation.actions) and len(strategy_variation.signals):
                # cut signals to the same length stating from the end
                timestamps = (
                    timestamps
                    if timestamps is not None
                    else await self.get_candles(
                        matrix_enums.PriceDataSources.TIME.value
                    )
                )
                # merge signals
                if strategy_variation.signals == [True]:
                    # directly connected action
                    true_signal = [True] * len(timestamps)
                else:
                    cutted_signals = cut_data_to_same_len(
                        strategy_variation.signals, get_list=True
                    )
                    true_signal = numpy.prod(cutted_signals, axis=0, dtype=bool)
                aux = numpy.array(timestamps[-len(true_signal) :], dtype=int)
                # filter timestamps
                variation_cache = aux[true_signal]
                if len(variation_cache):
                    if self.enable_plot:
                        source_timeframe = self.get_block_time_frame()
                        candles_closes = (
                            candles_closes
                            if candles_closes is not None
                            else await self.get_candles(
                                matrix_enums.PriceDataSources.CLOSE.value
                            )
                        )
                        (
                            cutted_candles_closes,
                            cutted_signals,
                        ) = cut_data_to_same_len((candles_closes, true_signal))
                        await self.plot_and_store_signals(
                            signal_values=cutted_candles_closes,
                            signals=cutted_signals,
                            reset_cache_before_writing=True,
                            # TODO make unique title
                            title=f"Strategy Signals ({strategy_variation.flow_name})",
                            source_timeframe=source_timeframe,
                            chart_location=self.chart_location,
                            plot_color=self.signal_color.value,
                        )
                    strategy_variation.write_strategy_cache(variation_cache)
                    trades_count += len(variation_cache)
                    self.strategy_variations_cache.append(strategy_variation)
                    if self.block_factory.ctx.exchange_manager.is_backtesting:
                        whitelist_timestamps += list(variation_cache)
        if self.block_factory.ctx.exchange_manager.is_backtesting:
            self.block_factory.whitelist_timestamps += list(set(whitelist_timestamps))
            self.block_factory.end_measure_time(
                s_time,
                f"building strategy for {trades_count} trades on {self.block_factory.ctx.symbol} "
                f"{self.block_factory.ctx.time_frame} {self.block_factory.ctx.exchange_name}",
            )
        return s_time
