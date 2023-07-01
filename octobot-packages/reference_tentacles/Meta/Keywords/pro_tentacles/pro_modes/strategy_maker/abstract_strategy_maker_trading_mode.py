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
import octobot_trading.modes.script_keywords.basic_keywords as basic_keywords
import octobot_trading.modes.script_keywords.context_management as context_management
import octobot_trading.enums as trading_enums
import octobot_commons.enums as common_enums
import octobot_commons.errors as commons_errors
import tentacles.Meta.Keywords.basic_tentacles.basic_modes.mode_base.abstract_mode_base as abstract_mode_base

# circular import when import as
from tentacles.Meta.Keywords.basic_tentacles.basic_modes.spot_master.spot_master_3000_trading_mode import (
    SpotMaster3000Making,
)
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.enums as maker_enums
import tentacles.Meta.Keywords.pro_tentacles.strategy_maker.strategy_builder_enums as strategy_builder_enums
import tentacles.Meta.Keywords.pro_tentacles.strategy_maker.strategy_building as strategy_building
import tentacles.Meta.Keywords.pro_tentacles.pro_modes.semi_auto_mode.semi_auto_trading_mode as semi_auto_trading_mode


class StrategyMaker(
    semi_auto_trading_mode.SemiAutoTradingModeMaking,
    SpotMaster3000Making,
    strategy_building.StrategyMakingProducer,
):
    strategy_mode: str = None
    should_execute_semi_auto: bool = False
    pairs_to_execute: list = None
    action: str = None
    SUPPORTS_PLOT_SIGNALS: bool = True

    def __init__(self, channel, config, trading_mode, exchange_manager):
        semi_auto_trading_mode.SemiAutoTradingModeMaking.__init__(
            self, channel, config, trading_mode, exchange_manager
        )
        SpotMaster3000Making.__init__(
            self, channel, config, trading_mode, exchange_manager
        )
        strategy_building.StrategyMakingProducer.__init__(
            self, channel, config, trading_mode, exchange_manager
        )

    async def make_strategy(
        self,
        ctx: context_management.Context,
        action: str,
        action_data: typing.Optional[dict] = None,
    ):
        await self.init_strategy_mode(ctx, action)
        if self.strategy_mode == maker_enums.StrategyModes.SEMI_AUTOMATED_TRADING:
            await self.make_semi_auto_strategy()
        elif (
            self.strategy_mode
            == maker_enums.StrategyModes.AUTOMATED_BASED_ON_INDICATORS
        ):
            self.SUPPORTS_PLOT_SIGNALS: bool = True
            await self.make_auto_strategy()
        elif (
            self.strategy_mode
            == maker_enums.StrategyModes.AUTOMATED_BASED_ON_INDICATORS
        ):
            self.SUPPORTS_PLOT_SIGNALS: bool = True
            await self.make_auto_strategy()
        elif (
            self.strategy_mode
            == maker_enums.StrategyModes.AUTOMATED_PORTFOLIO_BALANCING
        ):
            self.SUPPORTS_PLOT_SIGNALS: bool = False
            await self.execute_rebalancing_strategy(ctx)

    async def init_strategy_mode(self, ctx: context_management.Context, action):
        self.ctx: context_management.Context = ctx
        self.action = action
        self.strategy_mode = await basic_keywords.user_input(
            self.ctx,
            "strategy_mode",
            common_enums.UserInputTypes.OPTIONS,
            title="Strategy mode",
            def_val=maker_enums.StrategyModes.AUTOMATED_BASED_ON_INDICATORS,
            options=maker_enums.StrategyModes.ALL_MODES,
            show_in_summary=True,
            show_in_optimizer=False,
        )

    async def make_auto_strategy(self):
        try:
            await self.handle_trigger_time_frame()
        except commons_errors.ExecutionAborted:
            return

        available_timeframes = [
            timeframe.value
            for timeframe in self.ctx.exchange_manager.exchange_config.get_relevant_time_frames()
        ]
        trigger_time_frame: str = None
        if len(available_timeframes) > 1:
            trigger_time_frame = await basic_keywords.user_input(
                self.ctx,
                "time_frame_strategy_maker",
                "options",
                title="Select the time frame for the strategy maker",
                def_val=available_timeframes[0],
                options=available_timeframes,
            )
            # if time_frame != self.ctx.time_frame:
            #     commons_errors.ExecutionAborted(
            #         f"Execution aborted: disallowed time frame: {self.ctx.time_frame}"
            #     )
        elif len(available_timeframes) == 1:
            trigger_time_frame = available_timeframes[-1]
        if not self.ctx.exchange_manager.is_backtesting:
            # live trading
            if trigger_time_frame == self.ctx.time_frame:
                await self.get_backtesting_mode()
                await self.build_and_trade_strategies_live()
        elif not self.trading_mode.get_initialized_trading_pair_by_bot_id(
            self.ctx.symbol, self.ctx.time_frame
        ):
            initialized_trading_pair_by_bot_id = (
                self.trading_mode.get_initialized_trading_pair_by_bot_id(
                    self.ctx.symbol
                )
            )
            if self.ctx.time_frame != trigger_time_frame:
                self.trading_mode.set_initialized_trading_pair_by_bot_id(
                    self.ctx.symbol, self.ctx.time_frame, True
                )
                # self.handle_backtesting_timestamp_whitelist(True)
                return

            if not initialized_trading_pair_by_bot_id and 1 < len(
                self.time_frame_filter
            ):
                # other timeframes not initialized yet
                return
            if initialized_trading_pair_by_bot_id:
                if any(
                    not (
                        time_frame in initialized_trading_pair_by_bot_id
                        or trigger_time_frame == time_frame
                    )
                    for time_frame in self.time_frame_filter
                ):
                    # at least one other timeframes not initialized yet
                    return

            if (
                await self.get_backtesting_mode()
                == strategy_builder_enums.BacktestingMode.normal_backtesting_mode
            ):
                # first back-testing candle
                await self.build_strategies_backtesting_cache()
            elif (
                await self.get_backtesting_mode()
                == strategy_builder_enums.BacktestingMode.plot_only_backtesting_mode
            ):
                # first back-testing candle
                await self.build_strategies_backtesting_cache(plot_only_mode=True)
            else:
                await self.execute_in_trade_analysis_mode()
        else:
            # back-testing on all the other candles
            await self.trade_strategies_backtesting()


class AbstractStrategyMakerMode(abstract_mode_base.AbstractBaseMode):
    async def get_additional_metadata(self, is_backtesting):
        additional_metadata = {}
        if is_backtesting:
            additional_metadata[
                common_enums.BacktestingMetadata.TRADES.value
            ] = self.producers[0].strategy_cache.__len__()
            all_winrates = self.producers[0].all_winrates
            for take_profit_target in all_winrates:
                for winrate_side in all_winrates[take_profit_target]:
                    for sl_target in all_winrates[take_profit_target][winrate_side]:
                        if all_winrates[take_profit_target][winrate_side][sl_target]:
                            additional_metadata[
                                f"P{str(take_profit_target).replace('.', '-').replace('-0', '')}/"
                                f"S{str(sl_target).replace('.', '-').replace('-0', '')}"
                            ] = round(
                                all_winrates[take_profit_target][winrate_side][
                                    sl_target
                                ],
                                1,
                            )
        return additional_metadata

    def get_mode_producer_classes(self) -> list:
        return [StrategyMaker]

    @classmethod
    def get_supported_exchange_types(cls) -> list:
        """
        :return: The list of supported exchange types
        """
        return [trading_enums.ExchangeTypes.SPOT, trading_enums.ExchangeTypes.FUTURE]
