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

import octobot_commons.enums as common_enums
import octobot_commons.errors as commons_errors
from octobot_trading.api import symbol_data
import octobot_trading.modes.script_keywords.basic_keywords.user_inputs as user_inputs
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    TradingModeCommands,
)
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.orders.managed_order_pro.activate_managed_order as activate_managed_order
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.enums as maker_enums
import tentacles.Meta.Keywords.basic_tentacles.basic_modes.mode_base.abstract_producer_base as abstract_producer_base
import tentacles.Meta.Keywords.basic_tentacles.basic_modes.mode_base.producer_base as producer_base


class SemiAutoTradingModeMaking(
    abstract_producer_base.AbstractBaseModeProducer,
    producer_base.MatrixProducerBase,
):
    strategy_mode: str = maker_enums.StrategyModes.SEMI_AUTOMATED_TRADING
    should_execute_semi_auto: bool = False
    pairs_to_execute: list = None
    all_pairs: list = None
    enable_settings_for_all: bool = None
    action: str = None
    managend_orders_settings: dict = {}
    trading_sides: dict = {}
    plot_order_preview: dict = {}
    plot_order_preview_for_all: bool = False
    trading_side_for_all: str = None
    managend_orders_settings_for_all = None
    pair_settings_name: str = None

    def __init__(self, channel, config, trading_mode, exchange_manager):
        abstract_producer_base.AbstractBaseModeProducer.__init__(
            self, channel, config, trading_mode, exchange_manager
        )
        producer_base.MatrixProducerBase.__init__(
            self, channel, config, trading_mode, exchange_manager
        )

    async def make_semi_auto_strategy(self):
        try:
            await self.initialize_base_settings()
        except commons_errors.ExecutionAborted:
            return
        if self.enable_settings_for_all:
            all_pairs_settings_name: str = "all_pairs_settings"
            await user_inputs.user_input(
                self.ctx,
                all_pairs_settings_name,
                common_enums.UserInputTypes.OBJECT,
                title="Order settings for all pairs",
                def_val=None,
                show_in_summary=True,
                show_in_optimizer=False,
            )
            self.trading_side_for_all: str = await user_inputs.user_input(
                self.ctx,
                "trading_side",
                common_enums.UserInputTypes.OPTIONS,
                title="Trading side",
                def_val="long",
                options=["long", "short"],
                show_in_summary=True,
                show_in_optimizer=False,
                parent_input_name=all_pairs_settings_name,
            )
            self.plot_order_preview_for_all: str = await user_inputs.user_input(
                self.ctx,
                "plot_order_preview",
                common_enums.UserInputTypes.BOOLEAN,
                title="Plot orders preview",
                def_val=False,
                show_in_summary=True,
                show_in_optimizer=False,
                parent_input_name=all_pairs_settings_name,
            )
            self.managend_orders_settings_for_all = (
                await activate_managed_order.activate_managed_orders(
                    self,
                    parent_input_name=all_pairs_settings_name,
                    name_prefix="all",
                    order_tag_prefix="Managed order all",
                )
            )
        managed_order_id = 100
        if self.pairs_to_execute:
            for pair in self.pairs_to_execute:
                managed_order_id += 1
                await self.initialize_pair_settings(pair, managed_order_id)
                if (
                    self.action == TradingModeCommands.EXECUTE
                    and pair in self.managend_orders_settings
                    and self.ctx.time_frame in self.trigger_time_frames
                    and self.ctx.symbol == pair
                ):
                    self.ctx.enable_trading = True
                    try:
                        await activate_managed_order.managed_order(
                            self,
                            trading_side=self.trading_sides[pair],
                            orders_settings=self.managend_orders_settings[pair],
                        )
                    except Exception as error:
                        self.ctx.logger.exception(
                            error, True, f"Failed to execute orders for {pair}"
                        )
                elif (
                    self.action != TradingModeCommands.INIT_CALL
                    and pair in self.managend_orders_settings
                    and self.plot_order_preview.get(pair)
                    and self.ctx.time_frame in self.trigger_time_frames
                    and self.ctx.symbol == pair
                ):
                    self.ctx.enable_trading = False
                    await activate_managed_order.managed_order_preview(
                        self,
                        trading_side=self.trading_sides[pair],
                        orders_settings=self.managend_orders_settings[pair],
                    )

    async def initialize_pair_settings(self, pair, managed_order_id):
        self.pair_settings_name: str = f"{pair} settings"
        await user_inputs.user_input(
            self.ctx,
            self.pair_settings_name,
            common_enums.UserInputTypes.OBJECT,
            title=f"{pair} settings",
            def_val=None,
            show_in_summary=True,
            show_in_optimizer=False,
            editor_options={
                "grid_columns": 12,
            },
        )
        enabled = await user_inputs.user_input(
            self.ctx,
            f"{pair}_custom_settings_enabled",
            common_enums.UserInputTypes.BOOLEAN,
            title=f"Enable custom {pair} order settings",
            def_val=False,
            show_in_summary=True,
            show_in_optimizer=False,
            parent_input_name=self.pair_settings_name,
        )
        if enabled:
            self.plot_order_preview[pair]: str = await user_inputs.user_input(
                self.ctx,
                f"{pair}_plot_order_preview",
                common_enums.UserInputTypes.BOOLEAN,
                title="Plot orders preview",
                def_val=False,
                show_in_summary=True,
                show_in_optimizer=False,
                parent_input_name=self.pair_settings_name,
            )
            self.trading_sides[pair] = await user_inputs.user_input(
                self.ctx,
                f"{pair}_custom_trading_side",
                common_enums.UserInputTypes.OPTIONS,
                title=f"Trading side for {pair}",
                def_val="long",
                options=["long", "short"],
                show_in_summary=True,
                show_in_optimizer=False,
                parent_input_name=self.pair_settings_name,
            )
            self.managend_orders_settings[
                pair
            ] = await activate_managed_order.activate_managed_orders(
                self,
                parent_input_name=self.pair_settings_name,
                order_tag_prefix=f"Managed order {pair}",
                name_prefix=pair.replace("/", "").replace(":", ""),
            )
            if (
                self.trading_mode.enable_real_time_strategy
                and self.trading_mode.real_time_strategy_data
            ):
                await self.trading_mode.real_time_strategy_data.create_real_time_strategy(
                    self,
                    [pair],
                    parent_user_input_name=self.pair_settings_name,
                    input_suffix=pair,
                    title_name=pair,
                )
        elif self.enable_settings_for_all:
            self.managend_orders_settings[pair] = self.managend_orders_settings_for_all
            self.trading_sides[pair] = self.trading_side_for_all
            self.plot_order_preview[pair] = self.plot_order_preview_for_all

    async def initialize_base_settings(self):
        await self.handle_trigger_time_frame()
        self.all_pairs = symbol_data.get_config_symbols(
            self.ctx.exchange_manager.config, True
        )
        self.pairs_to_execute = await user_inputs.user_input(
            self.ctx,
            "pairs_to_trade",
            common_enums.UserInputTypes.MULTIPLE_OPTIONS,
            title="Pairs to execute trades on",
            def_val=self.all_pairs or [],
            options=self.all_pairs or [],
            show_in_summary=True,
            show_in_optimizer=False,
        )
        self.enable_settings_for_all: bool = await user_inputs.user_input(
            self.ctx,
            "enable_settings_for_all",
            common_enums.UserInputTypes.BOOLEAN,
            title="Enable order settings for all pairs",
            def_val=False,
            show_in_summary=False,
            show_in_optimizer=False,
        )
