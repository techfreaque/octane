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
import async_channel.channels as channels
from octobot_commons.constants import CONFIG_ACTIVATION_TOPICS
from octobot_commons.enums import ActivationTopics, UserCommands
from octobot_commons.symbols import symbol_util
import octobot_services.api as services_api
from octobot_trading.modes import modes_util
import octobot_trading.enums as trading_enums
from octobot_trading.modes.script_keywords.context_management import Context
import octobot_trading.exchange_channel as exchanges_channel
import octobot_trading.personal_data as trading_personal_data
import async_channel.constants as channel_constants

from tentacles.Meta.Keywords.basic_tentacles.basic_modes.mode_base import (
    abstract_mode_base,
)
from tentacles.Meta.Keywords.basic_tentacles.basic_modes.mode_base.abstract_producer_base import (
    AbstractBaseModeProducer,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords import matrix_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.orders.managed_order_pro.daemons.ping_pong.simple_ping_pong import (
    play_ping_pong,
)
from tentacles.Meta.Keywords.block_factory import block_factory_enums
from tentacles.Meta.Keywords.block_factory.block_factory_worker import BlockFactory
from tentacles.Services.Services_feeds import trading_view_service_feed


class StrategyFlowMakerMode(abstract_mode_base.AbstractBaseMode):
    AVAILABLE_API_ACTIONS: list = []
    # tradingview
    TV_SERVICE_FEED_CLASS = trading_view_service_feed.TradingViewServiceFeed
    EXCHANGE_KEY = "EXCHANGE"
    SYMBOL_KEY = "SYMBOL"

    str_symbol: str
    merged_simple_symbol: str
    str_currency: str

    def __init__(self, config, exchange_manager):
        super().__init__(config, exchange_manager)
        self.producer = StrategyFlowMakerModeProducer
        self.block_factory: BlockFactory = BlockFactory(trading_mode=self)

    def get_mode_producer_classes(self) -> list:
        return [StrategyFlowMakerModeProducer]

    def init_user_inputs(self, inputs: dict) -> None:
        self.block_factory.soft_refresh_block_factory(inputs=inputs, trading_mode=self)

    @classmethod
    def get_supported_exchange_types(cls) -> list:
        """
        :return: The list of supported exchange types
        """
        return [trading_enums.ExchangeTypes.SPOT, trading_enums.ExchangeTypes.FUTURE]

    async def user_commands_callback(self, bot_id, subject, action, data) -> None:
        # do not call super as reload_config is called by reload_scripts already
        # on RELOAD_CONFIG command
        self.logger.debug(f"Received {action} command")
        if action == matrix_enums.TradingModeCommands.EXECUTE:
            await self._manual_trigger(data)
            self.logger.debug(
                f"Triggered trading mode from {action} command with data: {data}"
            )
        elif action == matrix_enums.TradingModeCommands.ACTIVATE_REALTIME_STRATEGY:
            self.activate_realtime_strategy()
            self.logger.info("Real time strategy activated")
        elif action == matrix_enums.TradingModeCommands.DISABLE_REALTIME_STRATEGY:
            self.disable_realtime_strategy()
            await self.reload_scripts()
            self.logger.info("Real time strategy disabled")
        elif action == UserCommands.RELOAD_CONFIG.value:
            # only reload config
            self.logger.debug("Reloaded configuration")
            await self.reload_config(self.exchange_manager.bot_id)
        elif action == UserCommands.RELOAD_SCRIPT.value:
            # reload config and script
            self.logger.debug("Reloaded configuration")
            await self.reload_scripts()
        elif action == UserCommands.CLEAR_PLOTTING_CACHE.value:
            await modes_util.clear_plotting_cache(self)
        elif action == UserCommands.CLEAR_SIMULATED_ORDERS_CACHE.value:
            await modes_util.clear_simulated_orders_cache(self)

    async def create_consumers(self) -> list:
        """
        Creates the instance of consumers listed in MODE_CONSUMER_CLASSES
        :return: the list of consumers created
        """
        consumers = await super().create_consumers()
        feed_consumer = []
        if not self.exchange_manager.is_backtesting:
            parsed_symbol = symbol_util.parse_symbol(self.symbol)
            self.str_symbol = str(parsed_symbol)
            self.str_currency = parsed_symbol.quote
            self.merged_simple_symbol = (
                parsed_symbol.merged_str_base_and_quote_only_symbol(market_separator="")
            )
            service_feed = services_api.get_service_feed(
                self.TV_SERVICE_FEED_CLASS, self.bot_id
            )
            if service_feed is not None:
                feed_consumer = [
                    await channels.get_chan(
                        service_feed.FEED_CHANNEL.get_name()
                    ).new_consumer(self._trading_view_signal_callback)
                ]
            else:
                self.logger.error(
                    "Impossible to find the Trading view service feed, "
                    "trading view signals tradingg is not available"
                )
        ping_pong_consumer: list = []
        if (
            (self.trading_config.get("nodes", {}) or {})
            .get("mode_node", {})
            .get("config_mode_node", {})
            .get("enable_ping_pong")
        ):
            ping_pong_consumer.append(
                await exchanges_channel.get_chan(
                    trading_personal_data.OrdersChannel.get_name(),
                    self.exchange_manager.id,
                ).new_consumer(
                    self._order_notification_callback,
                    symbol=(
                        self.symbol
                        if self.symbol
                        else channel_constants.CHANNEL_WILDCARD
                    ),
                )
            )
        return consumers + feed_consumer + ping_pong_consumer

    async def _order_notification_callback(
        self,
        exchange,
        exchange_id,
        cryptocurrency,
        symbol,
        order,
        update_type,
        is_from_bot,
    ):
        if (
            self.any_ping_pong_mode_active
            and order[trading_enums.ExchangeConstantsOrderColumns.STATUS.value]
            == trading_enums.OrderStatus.FILLED.value
            and is_from_bot
        ):
            await self.producers[0].order_filled_callback(order, symbol)

    async def _trading_view_signal_callback(self, data):
        parsed_data = {}
        signal_data = data.get("metadata", "")
        for line in signal_data.split(";"):
            if not line.strip():
                # ignore empty lines
                continue
            values = line.split("=")
            try:
                value = values[1].strip()
                # restore booleans
                lower_val = value.lower()
                if lower_val in ("true", "false"):
                    value = lower_val == "true"
                parsed_data[values[0].strip()] = value
            except IndexError:
                self.logger.error(
                    f'Invalid signal line in trading view signal, ignoring it. Line: "{line}"'
                )

        try:
            if parsed_data[
                self.EXCHANGE_KEY
            ].lower() in self.exchange_manager.exchange_name and (
                parsed_data[self.SYMBOL_KEY] == self.merged_simple_symbol
                or parsed_data[self.SYMBOL_KEY] == self.str_symbol
            ):
                # TODO use Lowest timeframe
                await self.producers[0].trading_view_signal_callback(
                    exchange=self.exchange_manager.exchange_name,
                    exchange_id=self.exchange_manager.id,
                    cryptocurrency=self.str_currency,
                    symbol=self.str_symbol,
                    parsed_data=parsed_data,
                    time_frame=None,
                )
        except KeyError as error:
            self.logger.error(
                f"Error when handling trading view signal: missing {error} required value. "
                f'Signal: "{signal_data}"'
            )


class StrategyFlowMakerModeProducer(AbstractBaseModeProducer):
    async def make_strategy(
        self,
        context: Context,
        action: typing.Optional[str] = None,
        action_data: typing.Optional[dict] = None,
    ):
        if action in (
            matrix_enums.TradingModeCommands.EXECUTE,
            matrix_enums.TradingModeCommands.OHLC_CALLBACK,
            matrix_enums.TradingModeCommands.KLINE_CALLBACK,
            matrix_enums.TradingModeCommands.SAVE,
            matrix_enums.TradingModeCommands.TRADING_VIEW_CALLBACK,
        ):
            context.enable_trading = action != matrix_enums.TradingModeCommands.SAVE
            block_factory: BlockFactory = self.trading_mode.block_factory
            await block_factory.run_block_factory(
                ctx=context,
                trading_mode_producer=self,
                action=action,
                action_data=action_data,
            )

    def get_channels_registration(self):
        registration_channels = []
        # Activate on evaluation cycle only by default
        def_value = [ActivationTopics.FULL_CANDLES.value]
        topics = (
            self.trading_mode.trading_config.get(
                block_factory_enums.CURRENT_NODES_NAME, {}
            )
            .get(block_factory_enums.MODE_CONFIG_NAME, {})
            .get(block_factory_enums.CURRENT_NODE_CONFIG_NAME, {})
            .get(
                CONFIG_ACTIVATION_TOPICS.replace(" ", "_"),
            )
            or def_value
        )
        for topic in topics:
            try:
                registration_channels.append(self.TOPIC_TO_CHANNEL_NAME[topic])
            except KeyError:
                self.logger.error(f"Unknown registration topic: {topic}")
        return registration_channels

    async def order_filled_callback(self, filled_order, symbol):
        """
        Called when an order is filled: create secondary orders if the filled order is an initial order
        :param filled_order:
        :return: None
        """
        await play_ping_pong(
            trading_mode=self,
            symbol=symbol,
            triggered_order=filled_order,
        )
