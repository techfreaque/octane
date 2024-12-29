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
from octobot_commons import enums
from octobot_commons.enums import PlotCharts, UserInputEditorOptionsTypes
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)
from tentacles.Meta.Keywords.block_factory import abstract_entry_order_block
import tentacles.Meta.Keywords.block_factory.abstract_strategy_block as abstract_strategy_block
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums


class TradingViewWebhookStrategy(abstract_strategy_block.StrategyBlock):
    NAME = "trading_view_webhook_strategy"
    TITLE = "Trading View Webhook Strategy"
    TITLE_SHORT = "Trading View Webhook Strategy"
    DESCRIPTION = (
        "Trading view webhook  strategy can  be used to trade based on "
        "tradingview signals. Make sure to setup tradingview webhooks first"
    )
    enable_strategy: bool
    signal_color: block_factory_enums.Colors
    enable_plot: bool
    trigger_time_frame: str
    trigger_pairs: list
    chart_location: typing.Optional[str]

    def init_block_settings(self) -> None:
        self.enable_plot = self.user_input(
            "trading_view_alert_message",
            "object",
            title="Trading View Example Alert",
            def_val=True,
            description=(
                f"EXCHANGE={self.block_factory.trading_mode.exchange_manager.exchange_name}; "
                f"SYMBOL={self.block_factory.trading_mode.symbol}; "
                f"STRATEGY_ID={self.strategy_id}"
            ),
            editor_options={UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: True},
        )
        self.trigger_time_frame: str = self.user_select_trigger_time_frame(
            "Data Source Time Frame", "data_source_time_frame"
        )
        self.enable_plot = True
        backtest_plotting_mode: matrix_enums.BacktestPlottingModes = (
            matrix_enums.BacktestPlottingModes.ENABLE_PLOTTING
        )
        live_plotting_mode: matrix_enums.LivePlottingModes = (
            matrix_enums.LivePlottingModes.REPLOT_VISIBLE_HISTORY
        )
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
        if (
            (
                self.block_factory.ctx.trigger_source
                == matrix_enums.TradingModeCommands.TRADING_VIEW_CALLBACK
                and str(self.strategy_id)
                == self.block_factory.execution_action_data.get("STRATEGY_ID")
            )
            or self.block_factory.ctx.trigger_source
            in (
                enums.ActivationTopics.FULL_CANDLES.value,
                enums.ActivationTopics.IN_CONSTRUCTION_CANDLES.value,
            )
            and self.block_factory.ctx.time_frame == self.trigger_time_frame
        ) and not self.block_factory.ctx.exchange_manager.is_backtesting:
            should_trade: bool = (
                self.block_factory.ctx.trigger_source
                == matrix_enums.TradingModeCommands.TRADING_VIEW_CALLBACK
            )
            if should_trade:
                self.block_factory.ctx.time_frame = self.trigger_time_frame
            s_time = self.block_factory.start_measure_time(
                f"building trading view strategy {self.strategy_id} on {self.block_factory.ctx.symbol} "
                f"{self.block_factory.ctx.time_frame} {self.block_factory.ctx.exchange_name}"
            )
            trades_count = 0
            self.strategy_variations = []
            self.strategy_variations_cache = []
            await self.get_strategy_signals()
            if should_trade:
                timestamps = None
                candles_closes = None
                for strategy_variation in self.strategy_variations:
                    strategy_variation: abstract_strategy_block.StrategySignals
                    if len(strategy_variation.actions) and len(
                        strategy_variation.signals
                    ):
                        # cut signals to the same length stating from the end
                        timestamps = (
                            timestamps
                            if timestamps is not None
                            else await self.get_candles(
                                matrix_enums.PriceDataSources.TIME.value
                            )
                        )
                        if strategy_variation.signals == [True]:
                            await self.execute_strategy_variation(
                                signals=[True],
                                flow_name=strategy_variation.flow_name,
                                action_blocks=strategy_variation.actions,
                                candles_closes=candles_closes,
                                trades_count=trades_count,
                            )
                        else:
                            cutted_signals = cut_data_to_same_len(
                                strategy_variation.signals, get_list=True
                            )
                            # merge signals
                            true_signal = numpy.prod(cutted_signals, axis=0, dtype=bool)
                            aux = numpy.array(
                                timestamps[-len(true_signal) :], dtype=int
                            )
                            # filter timestamps
                            variation_cache = aux[true_signal]
                            if len(variation_cache):
                                await self.execute_strategy_variation(
                                    signals=true_signal,
                                    flow_name=strategy_variation.flow_name,
                                    action_blocks=strategy_variation.actions,
                                    candles_closes=candles_closes,
                                    trades_count=trades_count,
                                )
            self.block_factory.end_measure_time(
                s_time,
                f"building trading view strategy {self.strategy_id} for {trades_count} signals on {self.block_factory.ctx.symbol} "
                f"{self.block_factory.ctx.time_frame} {self.block_factory.ctx.exchange_name}",
            )

    async def execute_strategy_variation(
        self, signals, flow_name, action_blocks, candles_closes, trades_count
    ):
        if self.enable_plot:
            source_timeframe = self.get_block_time_frame()
            candles_closes = (
                candles_closes
                if candles_closes is not None
                else await self.get_candles(matrix_enums.PriceDataSources.CLOSE.value)
            )
            (
                cutted_candles_closes,
                cutted_signals,
            ) = cut_data_to_same_len((candles_closes, signals))
            await self.plot_and_store_signals(
                signal_values=[cutted_candles_closes[-1]],
                signals=[cutted_signals[-1]],
                reset_cache_before_writing=False,
                title=flow_name,
                source_timeframe=source_timeframe,
                chart_location=self.chart_location,
                plot_color=self.signal_color.value,
                should_keep_values=True,
            )
        if cutted_signals[-1]:
            for action_block in action_blocks:
                if isinstance(
                    action_block,
                    abstract_entry_order_block.EntryOrderBlock,
                ):
                    trades_count += 1
                await action_block.execute_block_from_factory(
                    self.block_factory, triggering_block=self
                )
                trades_count += 1
