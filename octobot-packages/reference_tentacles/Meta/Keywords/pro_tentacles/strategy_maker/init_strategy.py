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
from octobot_commons.enums import (
    UserInputEditorOptionsTypes,
    UserInputOtherSchemaValuesTypes,
    UserInputTypes,
)
import octobot_trading.enums as enums
import octobot_trading.modes.script_keywords.basic_keywords as basic_keywords
import octobot_trading.modes.script_keywords.context_management as context_management
import tentacles.Meta.Keywords.scripting_library.orders.order_types.market_order as market_order
import tentacles.Meta.Keywords.scripting_library.orders.cancelling as cancelling
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.matrix_constants as matrix_constants
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.orders.managed_order_pro.activate_managed_order as activate_managed_order
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.orders.managed_order_pro.daemons.trailing_stop_loss.trail_stop_losses as trail_stop_losses
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.orders.managed_order_pro.settings.sl_settings as sl_settings
import tentacles.Meta.Keywords.pro_tentacles.evaluators.evaluators_handling as evaluators_handling
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.expired_orders_cancelling as expired_orders_cancelling
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.orders.managed_order_pro.settings.entry_types as entry_types
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.matrix_constants as matrix_constants


class StrategyData:
    enable_plot: bool = None
    live_recording_mode: bool = None
    display_each_strategy_in_a_tab: bool = True

    def __init__(
        self,
        maker,
        # provide a parent_input_name to define a different location in the ui
        parent_input_name: typing.Optional[str] = None,
    ):
        self.supported_evaluators = maker.supported_evaluators
        self.signals = {}
        self.strategy_id = maker.current_strategy_id
        self.input_path = f"evaluator/Strategy_{maker.current_strategy_id + 1}_Settings"
        self.parent_input_name: str = parent_input_name
        if self.parent_input_name:
            self.display_each_strategy_in_a_tab = False
        self.input_name = f"strategy_{maker.current_strategy_id + 1}_settings"
        self.config_path_short = f"s{self.strategy_id + 1}"
        self.trading_side = ""
        self.trading_side_key = ""
        self.nr_of_indicators = 0
        self.evaluators = {}
        self.strategy_signal = 0
        self.managed_order_root_name = f"S{self.strategy_id + 1}_Order_Settings"
        self.managed_order_root_name_prefix = f"S{self.strategy_id + 1}"
        self.managed_order_root_path = (
            f"evaluator/S{self.strategy_id + 1}_Order_Settings"
        )
        self.order_settings = None
        self.enable_strategy: bool = False

    async def build_and_trade_strategy_live(self, maker, ctx, strategy_only=False):
        await self.init_strategy(maker, strategy_only)
        if not self.enable_strategy:
            return
        self.strategy_signal = 0
        has_signal = 1
        for evaluator_id in range(0, self.nr_of_indicators):
            await self.get_evaluator(maker, ctx, evaluator_id)
            if self.evaluators and evaluator_id in self.evaluators:
                has_signal = self.strategy_signal = (
                    self.signals[evaluator_id] if has_signal == 1 else 0
                )
        if not strategy_only:
            await self.set_managed_order_settings(ctx, maker)
            if self.strategy_signal == 1:
                await self.execute_managed_order(ctx, maker)
            await self.handle_order_daemons(ctx, maker)
        return self.strategy_signal

    async def build_strategy_backtesting_cache(self, maker, ctx):
        m_time = utilities.start_measure_time()
        await self.init_strategy(maker)
        if not self.enable_strategy:
            return
        for evaluator_id in range(0, self.nr_of_indicators):
            await self.get_evaluator(maker, ctx, evaluator_id)

        await self.set_managed_order_settings(ctx, maker)
        utilities.end_measure_time(
            m_time,
            f" strategy maker - calculating evaluators for strategy {self.strategy_id}",
            min_duration=9,
        )

    async def trade_strategy_backtesting(self, ctx, maker):
        await self.execute_managed_order(ctx, maker)

    async def init_strategy(self, maker, strategy_only=False):
        if self.display_each_strategy_in_a_tab:
            await basic_keywords.user_input(
                maker.ctx,
                self.config_path_short,
                input_type=UserInputTypes.OBJECT.value,
                title=f"Strategy {maker.current_strategy_id + 1} Settings",
                def_val=None,
                path=self.input_path,
                editor_options={"grid_columns": 12, "antIcon": "PartitionOutlined"},
                other_schema_values={
                    matrix_enums.UserInputOtherSchemaValuesTypes.DISPLAY_AS_TAB.value: True
                },
            )
        else:
            await basic_keywords.user_input(
                maker.ctx,
                self.config_path_short,
                input_type="object",
                title=f"Strategy {maker.current_strategy_id + 1} Settings",
                def_val=None,
                path=self.input_path,
                editor_options={
                    UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
                    UserInputEditorOptionsTypes.COLLAPSED.value: True,
                },
                parent_input_name=self.parent_input_name,
            )
        self.enable_strategy = await basic_keywords.user_input(
            maker.ctx,
            f"enable_strategy_{self.config_path_short}",
            input_type="boolean",
            def_val=True,
            title="Enable Strategy",
            parent_input_name=self.config_path_short,
            order=1,
            editor_options={
                "grid_columns": 3,
            },
        )
        if not self.enable_strategy:
            return

        self.nr_of_indicators = await basic_keywords.user_input(
            maker.ctx,
            f"evaluator_slots_{self.config_path_short}",
            "int",
            def_val=2,
            title="Amount of evaluator slots for this strategy",
            min_val=1,
            parent_input_name=self.config_path_short,
            other_schema_values={
                UserInputOtherSchemaValuesTypes.DESCRIPTION.value: "Defines how many "
                "evaluators this strategy can use. All evaluators in this strategy must"
                " have a signal on the same bar to allow trading."
            },
            order=0,
            editor_options={
                "grid_columns": 6,
            },
        )
        if not strategy_only:
            self.trading_side = (
                await basic_keywords.user_input(
                    maker.ctx,
                    f"trading_direction_s{self.strategy_id + 1}",
                    "options",
                    def_val=matrix_enums.TradingSidesNames.LONG_TITLE,
                    title="Trading direction",
                    options=[
                        matrix_enums.TradingSidesNames.LONG_TITLE,
                        matrix_enums.TradingSidesNames.SHORT_TITLE,
                        matrix_enums.TradingSidesNames.LONG_EXIT_TITLE,
                        matrix_enums.TradingSidesNames.SHORT_EXIT_TITLE,
                    ],
                    parent_input_name=self.config_path_short,
                )
            ).lower()
        self.enable_plot = maker.enable_plot
        self.live_recording_mode = maker.live_recording_mode
        if (
            maker.ctx.exchange_manager.is_backtesting
            and maker.backtest_plotting_mode
            == matrix_enums.BacktestPlottingModes.ENABLE_PLOTTING
        ) or (
            maker.backtest_plotting_mode
            == matrix_enums.BacktestPlottingModes.ENABLE_PLOTTING
            or maker.live_plotting_mode
            in (
                matrix_enums.LivePlottingModes.PLOT_RECORDING_MODE,
                matrix_enums.LivePlottingModes.REPLOT_VISIBLE_HISTORY,
            )
        ):
            self.enable_plot = await basic_keywords.user_input(
                maker.ctx,
                f"enable_plots_strategy_{self.strategy_id + 1}",
                "boolean",
                title="Enable plots for this strategy",
                def_val=True,
                parent_input_name=self.config_path_short,
                editor_options={
                    "grid_columns": 3,
                },
                order=50,
            )
            if not self.enable_plot:
                self.live_recording_mode = True
        self.trading_side_key = (
            matrix_enums.TradingSideKeys.LONG
            if self.trading_side
            in (
                matrix_enums.TradingSidesNames.LONG,
                matrix_enums.TradingSidesNames.SHORT_EXIT,
            )
            else (
                matrix_enums.TradingSideKeys.SHORT
                if self.trading_side
                in (
                    matrix_enums.TradingSidesNames.SHORT,
                    matrix_enums.TradingSidesNames.LONG_EXIT,
                )
                else ""
            )
        )
        # self.input_path = f"{self.input_path}/Strategy"

    async def get_evaluator(
        self, maker, ctx: context_management.Context, evaluator_id: int
    ):
        sm_time = utilities.start_measure_time()
        evaluator = evaluators_handling.Evaluator_(
            maker, self.input_name, self.config_path_short, self.supported_evaluators
        )
        maker.current_evaluator_id = evaluator_id
        await evaluator.init_evaluator(maker, ctx, evaluator_id)
        if evaluator.enabled:
            self.evaluators[evaluator_id] = evaluator
            self.signals[evaluator_id] = await evaluator.evaluate_and_get_data(
                maker, ctx
            )
            maker.evaluators[evaluator.config_path] = evaluator
            utilities.end_measure_time(
                sm_time,
                f" strategy maker - calculating evaluator {evaluator_id + 1} "
                f"{evaluator.name} {evaluator.class_name}",
                min_duration=9,
            )

    async def execute_managed_order(self, ctx, maker):
        if self.trading_side in (
            matrix_enums.TradingSidesNames.LONG,
            matrix_enums.TradingSidesNames.SHORT,
        ):
            await activate_managed_order.managed_order(
                maker,
                trading_side=self.trading_side,
                orders_settings=self.order_settings,
            )
        elif self.trading_side == matrix_enums.TradingSidesNames.LONG_EXIT:
            await self.exit_long_trade(ctx)

        elif self.trading_side == matrix_enums.TradingSidesNames.SHORT_EXIT:
            await self.exit_short_trade(ctx)

    @staticmethod
    async def exit_short_trade(ctx: context_management.Context):
        await market_order.market(ctx, target_position=0, reduce_only=True)
        await cancelling.cancel_orders(
            ctx,
            symbol=ctx.symbol,
            side=enums.TradeOrderSide.BUY.value,
            tag=f"sl{matrix_constants.TAG_SEPERATOR}",
        )
        await cancelling.cancel_orders(
            ctx,
            symbol=ctx.symbol,
            side=enums.TradeOrderSide.SELL.value,
            tag=f"tp{matrix_constants.TAG_SEPERATOR}",
        )
        await cancelling.cancel_orders(
            ctx,
            symbol=ctx.symbol,
            side=enums.TradeOrderSide.SELL.value,
            tag=f"e{matrix_constants.TAG_SEPERATOR}",
        )

    @staticmethod
    async def exit_long_trade(ctx: context_management.Context):
        await market_order.market(ctx, target_position=0, reduce_only=True)
        await cancelling.cancel_orders(
            ctx,
            symbol=ctx.symbol,
            side=enums.TradeOrderSide.SELL.value,
            tag=f"sl{matrix_constants.TAG_SEPERATOR}",
        )
        await cancelling.cancel_orders(
            ctx,
            symbol=ctx.symbol,
            side=enums.TradeOrderSide.BUY.value,
            tag=f"tp{matrix_constants.TAG_SEPERATOR}",
        )
        await cancelling.cancel_orders(
            ctx,
            symbol=ctx.symbol,
            side=enums.TradeOrderSide.BUY.value,
            tag=f"e{matrix_constants.TAG_SEPERATOR}",
        )

    async def set_managed_order_settings(self, ctx, maker):
        if self.trading_side in (
            matrix_enums.TradingSidesNames.LONG,
            matrix_enums.TradingSidesNames.SHORT,
        ):
            await basic_keywords.user_input(
                ctx,
                self.managed_order_root_name,
                "object",
                title=f"Strategy {self.strategy_id+1} Order Settings",
                def_val=None,
                editor_options={"grid_columns": 12, "antIcon": "ShoppingCartOutlined"},
                other_schema_values={"display_as_tab": True}
                # path=self.managed_order_root_path,
            )
            self.order_settings = await activate_managed_order.activate_managed_orders(
                maker,
                parent_input_name=self.managed_order_root_name,
                name_prefix=f"s{self.strategy_id + 1}",
                order_tag_prefix=f"Strategy {self.strategy_id+1}",
                enable_trailing_stop_settings=True,
            )

    async def handle_order_daemons(self, ctx, maker):
        if self.order_settings:
            for order_group_settings in self.order_settings.order_groups.values():
                if (
                    order_group_settings.stop_loss.sl_trail_type
                    != sl_settings.ManagedOrderSettingsSLTrailTypes.DONT_TRAIL_DESCRIPTION
                ):
                    try:
                        await trail_stop_losses.trail_stop_losses_for_this_candle(
                            maker,
                            order_group_settings=order_group_settings,
                            order_settings=self.order_settings,
                        )
                    except Exception as error:
                        raise RuntimeError(
                            "Managed Order trailing Stop: There is probably an "
                            "issue in your Managed Order "
                            "configuration. Check the settings: " + str(error)
                        ) from error
                if (
                    order_group_settings.entry.enable_expired_limit_cancel
                    and order_group_settings.entry.entry_type
                    in entry_types.ManagedOrderSettingsEntryTypes.LIMIT_ENTRY_TYPES
                ):
                    await expired_orders_cancelling.cancel_expired_orders_for_this_candle(
                        ctx,
                        limit_max_age_in_bars=order_group_settings.entry.limit_max_age_in_bars,
                        tag=f"e{matrix_constants.TAG_SEPERATOR}{order_group_settings.order_manager_group_id}",
                    )
