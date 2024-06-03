from __future__ import annotations
from imp import reload
import importlib
import sys

from octobot_commons.constants import CONFIG_ACTIVATION_TOPICS
import tentacles.Meta.Keywords.block_factory as _block_factory
from types import ModuleType
import typing

from octobot_commons import os_util, time_frame_manager
import octobot_backtesting.api as backtesting_api
from octobot_trading.api import symbol_data
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords import matrix_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data import (
    public_exchange_data,
)
import octobot_commons.configuration.user_inputs as user_inputs
import octobot_commons.enums as commons_enums
import octobot_commons.logging as logging
from octobot_tentacles_manager import constants
from octobot_trading.modes.script_keywords import context_management

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools import (
    utilities,
)
from tentacles.Meta.Keywords.block_factory.abstract_action_block import ActionBlock
import tentacles.Meta.Keywords.block_factory.abstract_strategy_block as abstract_strategy_block
import tentacles.Meta.Keywords.block_factory.abstract_evaluator_block as abstract_evaluator_block
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.backtesting import (
    skip_runs,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.trade_analysis.order_plotting import (
    plot_orders,
)


STRATEGY_BLOCKS_DEV_MODE = os_util.parse_boolean_environment_var(
    "STRATEGY_BLOCKS_DEV_MODE", "False"
)


def get_block_type_modules():
    import tentacles.StrategyBlocks.IndicatorBlock as _IndicatorBlock
    import tentacles.StrategyBlocks.EvaluatorBlock as _EvaluatorBlock
    import tentacles.StrategyBlocks.StrategyBlock as _StrategyBlock
    import tentacles.StrategyBlocks.ActionBlock as _ActionBlock

    reload(_IndicatorBlock)
    reload(_EvaluatorBlock)
    reload(_StrategyBlock)
    reload(_ActionBlock)
    import tentacles.StrategyBlocks.IndicatorBlock as _IndicatorBlock
    import tentacles.StrategyBlocks.EvaluatorBlock as _EvaluatorBlock
    import tentacles.StrategyBlocks.StrategyBlock as _StrategyBlock
    import tentacles.StrategyBlocks.ActionBlock as _ActionBlock

    return (
        (
            abstract_strategy_block.StrategyBlock.PACKAGES_PATH,
            _StrategyBlock,
        ),
        (ActionBlock.PACKAGES_PATH, _ActionBlock),
        (abstract_indicator_block.IndicatorBlock.PACKAGES_PATH, _IndicatorBlock),
        (abstract_evaluator_block.EvaluatorBlock.PACKAGES_PATH, _EvaluatorBlock),
    )


class BlockFactory:
    installed_blocks: typing.Dict[str, typing.List[_block_factory.AbstractBlock]] = {}
    installed_blocks_info: typing.Dict[str, typing.Dict[str, str]] = {}

    logger = logging.get_logger("BlockFactory")
    enable_ping_pong: bool

    def __init__(self, trading_mode) -> None:
        self.ctx: context_management.Context = None
        self.execution_action: typing.Optional[str] = None
        self.execution_action_data: typing.Optional[dict] = None
        self.candles: typing.Dict[
            str, typing.Dict[str, typing.Dict[str, typing.Any]]
        ] = {}
        self.current_edges: list = []
        self.current_nodes: list = []
        self.current_nodes_instances_by_type: typing.Dict[
            str, typing.Dict[str, _block_factory.AbstractBlock]
        ] = {}
        self.current_nodes_instances_by_id: typing.Dict[
            str, _block_factory.AbstractBlock
        ] = {}
        self.last_run_plot_id: int = 0
        self.next_strategy_id: int = 1
        self.next_indicator_id: int = 1
        self.UI: user_inputs.UserInputFactory = trading_mode.UI
        self.trading_mode = trading_mode
        self.whitelist_timestamps: list = []
        self._available_time_frames = None
        self._available_pairs = None

        # TODO
        self.plot_orders: bool = False
        self.live_recording_mode: bool = False
        self.whitelist_mode: bool = True

    def init_building_blocks(self) -> None:
        self.init_installed_blocks_by_type()

    def soft_refresh_block_factory(self, trading_mode, inputs: dict) -> None:
        self.trading_mode = trading_mode
        if not self.check_if_exchange_enabled(trading_mode):
            return

        self._available_time_frames = None
        self._available_pairs = None
        self.current_nodes_instances_by_type = {}
        self.current_nodes_instances_by_id = {}
        self.next_strategy_id: int = 1
        self.next_indicator_id: int = 1
        self.init_building_blocks()

        self.init_edges(inputs=inputs)
        self.init_mode_config_node(inputs=inputs)
        self.init_nodes(inputs=inputs)
        # remove so it wont be use in execution mode
        self.trading_mode = None

    @staticmethod
    def check_if_exchange_enabled(trading_mode) -> bool:
        try:
            trading_mode.exchange_manager.config
            return True
        except AttributeError:
            trading_mode.logger.error("Exchange is not enabled or initialized yet")
            return False

    async def run_block_factory(
        self,
        ctx: context_management.Context,
        trading_mode_producer,
        action: typing.Optional[str] = None,
        action_data: typing.Optional[dict] = None,
    ) -> None:
        self.ctx: context_management.Context = ctx
        self.execution_action: typing.Optional[str] = action
        self.execution_action_data: typing.Optional[dict] = action_data
        if not self.check_if_exchange_enabled(ctx):
            return
        self.connect_blocks()
        self.last_run_plot_id: int = 0

        for block_id, block in self.current_nodes_instances_by_type.get(
            constants.TENTACLES_STRATEGY_BLOCKS_STRATEGY_PATH, {}
        ).items():
            try:
                await block.execute_block_from_factory(block_factory=self)
            except Exception as error:
                if hasattr(block, "indicator_id"):
                    _block_id = block.indicator_id
                elif hasattr(block, "strategy_id"):
                    _block_id = block.strategy_id
                else:
                    _block_id = block_id
                self.logger.exception(
                    error,
                    True,
                    f"Failed to run strategy block {block.TITLE} ({_block_id})",
                )
        if self.plot_orders:
            await plot_orders(ctx)
        if ctx.exchange_manager.is_backtesting:
            if not trading_mode_producer.trading_mode.get_initialized_trading_pair_by_bot_id(
                ctx.symbol, ctx.time_frame
            ):
                trading_mode_producer.trading_mode.set_initialized_trading_pair_by_bot_id(
                    ctx.symbol, ctx.time_frame, initialized=True
                )
                first_timestamps_from_pairs = []
                if not backtesting_api.get_backtesting_timestamp_whitelist(
                    ctx.exchange_manager.exchange.backtesting
                ):
                    first_timestamps_from_pairs = [
                        (
                            await self.get_candles(
                                source_name=matrix_enums.PriceDataSources.TIME.value,
                                symbol=symbol,
                                time_frame=time_frame,
                            )
                        )[0]
                        for symbol in self.get_available_pairs()
                        for time_frame in self.get_available_time_frames()
                    ]
                if self.whitelist_mode:
                    self.handle_backtesting_timestamp_whitelist(
                        list(
                            set(self.whitelist_timestamps + first_timestamps_from_pairs)
                        )
                    )

    async def get_candles(
        self,
        source_name: str = matrix_enums.PriceDataSources.CLOSE.value,
        time_frame: str = None,
        symbol: str = None,
        block_factory: typing.Optional[_block_factory.BlockFactory] = None,
    ):
        symbol = symbol or self.ctx.symbol
        time_frame = time_frame or self.ctx.time_frame
        used_block_factory = block_factory or self
        try:
            if self.ctx.exchange_manager.is_backtesting:
                return used_block_factory.candles[symbol][time_frame][source_name]
        except KeyError:
            pass
        starting_time = self.start_measure_time()
        if symbol not in used_block_factory.candles:
            used_block_factory.candles[symbol] = {}
        if time_frame not in used_block_factory.candles[symbol]:
            used_block_factory.candles[symbol][time_frame] = {}
        used_block_factory.candles[symbol][time_frame][source_name] = (
            await public_exchange_data.get_candles_from_name(
                used_block_factory,
                source_name=source_name,
                time_frame=time_frame,
                symbol=symbol,
                max_history=True,
            )
        )
        self.end_measure_time(
            starting_time,
            f"loading candle: {source_name}, {symbol}, {time_frame}",
            min_duration=1,
        )
        return used_block_factory.candles[symbol][time_frame][source_name]

    def get_available_time_frames(self) -> list:
        if self._available_time_frames is None:
            self._available_time_frames = [
                tf.value
                for tf in time_frame_manager.sort_time_frames(
                    self.ctx.exchange_manager.exchange_config.get_relevant_time_frames()
                )
            ]
        return self._available_time_frames

    def get_available_pairs(self) -> list:
        if self._available_pairs is None:
            self._available_pairs = symbol_data.get_config_symbols(
                self.ctx.exchange_manager.config, True
            )
        return self._available_pairs

    def handle_backtesting_timestamp_whitelist(self, any_trading_timestamps):
        final_whitelist: list = []
        time_frame_sec = (
            commons_enums.TimeFramesMinutes[
                commons_enums.TimeFrames(self.ctx.time_frame)
            ]
            * 60
        )
        for timestamp in any_trading_timestamps:
            final_whitelist.append(timestamp - time_frame_sec)
            final_whitelist.append(timestamp)
        # if self.whitelist_mode and len(self.trigger_time_frames) == 1:
        skip_runs.register_backtesting_timestamp_whitelist(self.ctx, final_whitelist)

    @staticmethod
    def start_measure_time(message: typing.Optional[str] = None) -> float:
        return utilities.start_measure_time(
            message=None if message is None else f" strategy flow builder - {message}"
        )

    @staticmethod
    def end_measure_time(
        m_time: typing.Union[int, float],
        message: str,
        min_duration: typing.Optional[typing.Union[int, float]] = None,
    ):
        utilities.end_measure_time(
            m_time=m_time,
            message=None if message is None else f" strategy flow builder - {message}",
            min_duration=min_duration,
        )

    def connect_blocks(self) -> None:
        if self.current_edges is not None:
            for edge in self.current_edges:
                try:
                    source_instance: _block_factory.AbstractBlock = (
                        self.current_nodes_instances_by_id.get(edge["source"])
                    )
                    target_instance: _block_factory.AbstractBlock = (
                        self.current_nodes_instances_by_id.get(edge["target"])
                    )
                    if source_instance and target_instance:
                        source_handle_id = edge["sourceHandle"]
                        source_handle = source_instance.output_nodes[source_handle_id]
                        target_handle_id = edge["targetHandle"]
                        target_handle = target_instance.input_nodes[target_handle_id]
                        source_handle.register_connected_handle_instance(target_handle)
                        target_handle.register_connected_handle_instance(source_handle)
                except Exception as error:
                    if hasattr(source_instance, "indicator_id"):
                        source_block_id = source_instance.indicator_id
                    elif hasattr(source_instance, "strategy_id"):
                        source_block_id = source_instance.strategy_id
                    else:
                        source_block_id = ""
                    if hasattr(target_instance, "indicator_id"):
                        target_block_id = target_instance.indicator_id
                    elif hasattr(target_instance, "strategy_id"):
                        target_block_id = target_instance.strategy_id
                    else:
                        target_block_id = ""
                    self.logger.exception(
                        error,
                        True,
                        f"Failed to connect block {f'{source_instance.NAME} {source_block_id}' if source_instance else 'None'}"
                        f" with {f'{target_instance.NAME} {target_block_id}' if target_instance else 'None'}",
                    )

    def init_nodes(self, inputs: dict) -> None:
        self.current_nodes = self.UI.user_input(
            block_factory_enums.CURRENT_NODES_NAME,
            commons_enums.UserInputTypes.OBJECT,
            self.trading_mode.trading_config.get(
                block_factory_enums.CURRENT_NODES_NAME, None
            ),
            inputs,
        )
        if self.current_nodes:
            for node_id in tuple(self.current_nodes.keys()):
                try:
                    if not node_id == block_factory_enums.MODE_CONFIG_NAME:
                        self.create_node(self.current_nodes[node_id], inputs)
                except Exception as error:
                    self.logger.exception(
                        error,
                        True,
                        f"Failed to initialize node - error: {error}",
                    )

    def init_mode_config_node(self, inputs: dict) -> None:
        self.UI.user_input(
            block_factory_enums.MODE_CONFIG_NAME,
            commons_enums.UserInputTypes.OBJECT,
            None,
            inputs,
            title="Strategy Flow Mode Configuration",
            parent_input_name=block_factory_enums.CURRENT_NODES_NAME,
        )
        self.init_hidden_node_setings(inputs, block_factory_enums.MODE_CONFIG_NAME)
        self.UI.user_input(
            block_factory_enums.CURRENT_NODE_CONFIG_NAME,
            commons_enums.UserInputTypes.OBJECT,
            None,
            inputs,
            parent_input_name=block_factory_enums.MODE_CONFIG_NAME,
            title="Strategy Flow Mode Configuration",
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: True,
                "color": block_factory_enums.Colors.RED.value,
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
            other_schema_values={
                commons_enums.UserInputOtherSchemaValuesTypes.DESCRIPTION.value: (
                    "The settings in this block are applied to all other blocks"
                ),
            },
        )
        activation_topic_values = [
            commons_enums.ActivationTopics.FULL_CANDLES.value,
            commons_enums.ActivationTopics.IN_CONSTRUCTION_CANDLES.value,
        ]
        self.UI.user_input(
            CONFIG_ACTIVATION_TOPICS.replace(" ", "_"),
            commons_enums.UserInputTypes.MULTIPLE_OPTIONS,
            [activation_topic_values[0]],
            inputs,
            options=activation_topic_values,
            parent_input_name=block_factory_enums.CURRENT_NODE_CONFIG_NAME,
            title="Strategy Triggers",
            show_in_summary=False,
            show_in_optimizer=False,
            other_schema_values={
                commons_enums.UserInputOtherSchemaValuesTypes.DESCRIPTION.value: (
                    "Requires a restart to be applied"
                ),
            },
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
        )
        self.plot_orders = self.UI.user_input(
            "plot_orders",
            commons_enums.UserInputTypes.BOOLEAN,
            False,
            inputs,
            parent_input_name=block_factory_enums.CURRENT_NODE_CONFIG_NAME,
            title="Plot Orders",
            show_in_summary=False,
            other_schema_values={
                commons_enums.UserInputOtherSchemaValuesTypes.DESCRIPTION.value: (
                    "While plotting orders on the charts is very helpfull, "
                    "it will also slow down the backtesting speed quite a lot. "
                    "Enable in backtesting only if really required"
                ),
            },
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
        )
        self.live_recording_mode = self.UI.user_input(
            "live_recording_mode",
            commons_enums.UserInputTypes.BOOLEAN,
            False,
            inputs,
            parent_input_name=block_factory_enums.CURRENT_NODE_CONFIG_NAME,
            title="Live plot recording mode",
            show_in_optimizer=False,
            show_in_summary=False,
            other_schema_values={
                commons_enums.UserInputOtherSchemaValuesTypes.DESCRIPTION.value: (
                    "If enable, the charting data will get created candle by candle "
                    "and past history will not get recreated. This will also improve "
                    "the live evaluation time as past signals dont need to be computed."
                    "If disabled, the visible chart history will get "
                    "recreated on every settings change."
                ),
            },
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
        )
        self.enable_ping_pong = self.UI.user_input(
            "enable_ping_pong",
            commons_enums.UserInputTypes.BOOLEAN,
            False,
            inputs,
            parent_input_name=block_factory_enums.CURRENT_NODE_CONFIG_NAME,
            title="Enable ping pong service (Restart required)",
            show_in_summary=False,
            show_in_optimizer=False,
            other_schema_values={
                commons_enums.UserInputOtherSchemaValuesTypes.DESCRIPTION.value: (
                    "Note that ping pong will slow down backtests by a lot, only use it when neccessary."
                    " If you enable this option, ping pong mode will be available in the all in one order block."
                ),
            },
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
        )
        self.enable_ping_pong = self.UI.user_input(
            "enable_ping_pong",
            commons_enums.UserInputTypes.INT,
            3000,
            inputs,
            parent_input_name=block_factory_enums.CURRENT_NODE_CONFIG_NAME,
            title="Available bars for live trading",
            show_in_summary=False,
            show_in_optimizer=False,
            other_schema_values={
                commons_enums.UserInputOtherSchemaValuesTypes.DESCRIPTION.value: (
                    "The amount of candles you will see on the live chart and "
                    "also what your strategy can use. "
                    "Some indicators might need a lot of data to be computed and some "
                    "less. The higher this value is the longer it will take to execute "
                    "your strategy in live trading."
                ),
            },
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
        )
        self.whitelist_mode = self.UI.user_input(
            "available_candles",
            commons_enums.UserInputTypes.INT,
            3000,
            inputs,
            parent_input_name=block_factory_enums.CURRENT_NODE_CONFIG_NAME,
            title="Available bars for live trading",
            show_in_summary=False,
            show_in_optimizer=False,
            other_schema_values={
                commons_enums.UserInputOtherSchemaValuesTypes.DESCRIPTION.value: (
                    "The amount of candles you will see on the live chart and "
                    "also what your strategy can use. "
                    "Some indicators might need a lot of data to be computed and some "
                    "less. The higher this value is the longer it will take to execute "
                    "your strategy in live trading."
                ),
            },
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
            },
        )

    def init_hidden_node_setings(self, inputs, parent_input_name):
        hidden_inputs = {
            "data": (commons_enums.UserInputTypes.OBJECT, None),
            "dragging": (commons_enums.UserInputTypes.BOOLEAN, None),
            "height": (commons_enums.UserInputTypes.FLOAT, None),
            "id": (commons_enums.UserInputTypes.TEXT, None),
            "position": (
                commons_enums.UserInputTypes.OBJECT,
                None,
            ),
            "positionAbsolute": (
                commons_enums.UserInputTypes.OBJECT,
                None,
            ),
            "selected": (commons_enums.UserInputTypes.BOOLEAN, None),
            "type": (commons_enums.UserInputTypes.TEXT, None),
            "width": (commons_enums.UserInputTypes.FLOAT, None),
        }
        for input_name, input_detail in hidden_inputs.items():
            self.UI.user_input(
                input_name,
                input_detail[0],
                input_detail[1],
                inputs,
                parent_input_name=parent_input_name,
                show_in_summary=False,
                show_in_optimizer=False,
            )

    def create_node(self, node: dict, inputs: dict) -> None:
        block_type_name: str = node["data"]["nodeType"]
        block_name: str = node["data"]["blockId"]
        block_instance: _block_factory.AbstractBlock = self.get_block_by_type_and_name(
            block_type_name, block_name
        )(
            trading_mode=self.trading_mode,
            node_config=node,
            inputs=inputs,
            block_factory=self,
        )
        block_instance.init_block_settings()

        if block_type_name not in self.current_nodes_instances_by_type:
            self.current_nodes_instances_by_type[block_type_name] = {}
        self.current_nodes_instances_by_type[block_type_name][
            block_instance.block_id
        ] = block_instance
        self.current_nodes_instances_by_id[block_instance.block_id] = block_instance

    def get_block_by_type_and_name(
        self, block_type_name: str, block_name: str
    ) -> _block_factory.AbstractBlock:
        return self.installed_blocks[block_type_name][block_name]

    def init_edges(self, inputs: dict) -> None:
        CURRENT_EDGES_NAME = "edges"
        self.current_edges = self.UI.user_input(
            CURRENT_EDGES_NAME,
            commons_enums.UserInputTypes.OBJECT_ARRAY,
            self.trading_mode.trading_config.get(CURRENT_EDGES_NAME, None),
            inputs,
            show_in_optimizer=False,
            show_in_summary=False,
        )
        self.UI.user_input(
            "source",
            commons_enums.UserInputTypes.TEXT,
            "",
            inputs,
            parent_input_name=CURRENT_EDGES_NAME,
            show_in_optimizer=False,
            show_in_summary=False,
        )
        self.UI.user_input(
            "target",
            commons_enums.UserInputTypes.TEXT,
            "",
            inputs,
            parent_input_name=CURRENT_EDGES_NAME,
            show_in_optimizer=False,
            show_in_summary=False,
        )
        self.UI.user_input(
            "sourceHandle",
            commons_enums.UserInputTypes.TEXT,
            "",
            inputs,
            parent_input_name=CURRENT_EDGES_NAME,
            show_in_optimizer=False,
            show_in_summary=False,
        )
        self.UI.user_input(
            "targetHandle",
            commons_enums.UserInputTypes.TEXT,
            "",
            inputs,
            parent_input_name=CURRENT_EDGES_NAME,
            show_in_optimizer=False,
            show_in_summary=False,
        )

    def init_installed_blocks_by_type(
        self,
    ) -> typing.Dict[str, typing.Dict[str, _block_factory.AbstractBlock]]:
        if self.installed_blocks == {} or STRATEGY_BLOCKS_DEV_MODE:
            (
                self.installed_blocks,
                self.installed_blocks_info,
            ) = self.get_installed_blocks_by_type()
        return self.installed_blocks

    @classmethod
    def get_installed_blocks_by_type(
        cls,
    ) -> typing.Dict[str, typing.Dict[str, _block_factory.AbstractBlock]]:
        installed_blocks: dict = {}
        installed_blocks_info: dict = {}
        for module_folder_name, module_folder in get_block_type_modules():
            (
                installed_blocks[module_folder_name],
                installed_blocks_info[module_folder_name],
            ) = cls._get_installed_block_modules(module_folder)
        return installed_blocks, installed_blocks_info

    @classmethod
    def _get_installed_block_modules(
        cls,
        modules_root: str,
    ) -> typing.Tuple[
        typing.Dict[str, _block_factory.AbstractBlock],
        typing.Dict[str, typing.Dict[str, str]],
    ]:
        available_block_modules: typing.Dict[str, _block_factory.AbstractBlock] = {}
        available_block_modules_info: dict = {}
        for moule_name, module in modules_root.__dict__.items():
            # TODO remove "abstract_" - its just a hack so we dont search in abstract modules
            if isinstance(module, ModuleType) and "abstract_" not in moule_name:
                for sub_module_name, sub_module in module.__dict__.items():
                    try:
                        if (
                            isinstance(sub_module, type)
                            and hasattr(sub_module, "init_block_settings")
                            and hasattr(sub_module, "execute_block")
                        ):
                            available_block_modules[sub_module.NAME] = sub_module
                            available_block_modules_info[sub_module.NAME] = {
                                "title": sub_module.TITLE,
                                "title_short": sub_module.TITLE_SHORT,
                                "description": sub_module.DESCRIPTION,
                                "color": sub_module.COLOR.value,
                            }
                    except Exception as error:
                        cls.logger.exception(
                            error,
                            True,
                            f"Failed to load Strategy Block from {sub_module_name}",
                        )
        return available_block_modules, available_block_modules_info


class ExchangeOfflineException(Exception):
    pass
