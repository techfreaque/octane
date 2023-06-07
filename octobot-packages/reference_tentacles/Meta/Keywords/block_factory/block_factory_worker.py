import importlib
from types import ModuleType
import typing

import octobot_commons.configuration.user_inputs as user_inputs
import octobot_commons.enums as commons_enums
from octobot_tentacles_manager import constants
from octobot_trading.modes.script_keywords import context_management
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools import (
    utilities,
)

from tentacles.Meta.Keywords.block_factory.abstract_action_block import ActionBlock
import tentacles.Meta.Keywords.block_factory.abstract_strategy_block as abstract_strategy_block
import tentacles.Meta.Keywords.block_factory.abstract_block as abstract_block
import tentacles.Meta.Keywords.block_factory.abstract_evaluator_block as abstract_evaluator_block
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums

import tentacles.StrategyBlocks.IndicatorBlock as _IndicatorBlock
import tentacles.StrategyBlocks.EvaluatorBlock as _EvaluatorBlock
import tentacles.StrategyBlocks.StrategyBlock as _StrategyBlock
import tentacles.StrategyBlocks.ActionBlock as _ActionBlock


BLOCK_TYPE_MODULES = (
    (
        abstract_strategy_block.StrategyBlock.PACKAGES_PATH,
        _StrategyBlock,
    ),
    (ActionBlock.PACKAGES_PATH, _ActionBlock),
    (abstract_indicator_block.IndicatorBlock.PACKAGES_PATH, _IndicatorBlock),
    (abstract_evaluator_block.EvaluatorBlock.PACKAGES_PATH, _EvaluatorBlock),
)


class BlockFactory:
    installed_blocks: typing.Dict[str, typing.List[abstract_block.AbstractBlock]] = {}
    installed_blocks_info: typing.Dict[str, typing.Dict[str, str]] = {}

    ENABLE_HOT_RELOAD = True

    def __init__(self, trading_mode) -> None:
        self.ctx: context_management.Context = None
        self.execution_action: typing.Optional[str] = None
        self.candles: typing.Dict[
            str, typing.Dict[str, typing.Dict[str, typing.Any]]
        ] = {}
        self.current_edges: list = []
        self.current_nodes: list = []
        self.current_nodes_instances_by_type: typing.Dict[
            str, typing.Dict[str, abstract_block.AbstractBlock]
        ] = {}
        self.current_nodes_instances_by_id: typing.Dict[
            str, abstract_block.AbstractBlock
        ] = {}
        self.last_run_plot_id: int = 0
        self.next_strategy_id: int = 1
        self.UI: user_inputs.UserInputFactory = trading_mode.UI
        self.trading_mode = trading_mode
        # TODO
        self.live_recording_mode: bool = False

    def init_building_blocks(self) -> None:
        self.init_installed_blocks_by_type()

    def soft_refresh_block_factory(self, trading_mode, inputs: dict) -> None:
        self.trading_mode = trading_mode
        self.current_nodes_instances_by_type = {}
        self.current_nodes_instances_by_id = {}
        self.next_strategy_id: int = 1
        self.init_edges(inputs=inputs)
        self.init_nodes(inputs=inputs)
        # remove so it wont be use in execution mode
        self.trading_mode = None

    async def run_block_factory(
        self,
        ctx: context_management.Context,
        trading_mode_producer,
        action: typing.Optional[str] = None,
    ) -> None:
        self.ctx: context_management.Context = ctx
        self.execution_action: typing.Optional[str] = action
        self.connect_blocks()
        self.last_run_plot_id: int = 0
        for block_id, block in self.current_nodes_instances_by_type.get(
            constants.TENTACLES_STRATEGY_BLOCKS_STRATEGY_PATH, {}
        ).items():
            try:
                await block.execute_block_from_factory(block_factory=self)
            except Exception as error:
                ctx.logger.exception(
                    error,
                    True,
                    f"Failed to run strategy block {block.TITLE} ({block_id})",
                )

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
        for edge in self.current_edges:
            try:
                source_instance: abstract_block.AbstractBlock = (
                    self.current_nodes_instances_by_id.get(edge["source"])
                )
                target_instance: abstract_block.AbstractBlock = (
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
                self.ctx.logger.exception(
                    error,
                    True,
                    f"Failed to connect block {source_instance.NAME if source_instance else 'None'}"
                    f" with {target_instance.NAME if target_instance else 'None'}",
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
                    self.create_node(self.current_nodes[node_id], inputs)
                except Exception as error:
                    self.trading_mode.logger.exception(
                        error,
                        True,
                        f"Failed to initialize node - error: {error}",
                    )

    def create_node(self, node: dict, inputs: dict) -> None:
        block_type_name: str = node["data"]["nodeType"]
        block_name: str = node["data"]["blockId"]
        block_instance: abstract_block.AbstractBlock = self.get_block_by_type_and_name(
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
    ) -> abstract_block.AbstractBlock:
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
    ) -> typing.Dict[str, typing.Dict[str, abstract_block.AbstractBlock]]:
        if self.installed_blocks == {}:
            for module_folder_name, module_folder in BLOCK_TYPE_MODULES:

                (
                    self.installed_blocks[module_folder_name],
                    self.installed_blocks_info[module_folder_name],
                ) = self._get_installed_block_modules(module_folder)
        return self.installed_blocks

    def _get_installed_block_modules(
        self,
        modules_root: str,
    ) -> typing.Tuple[
        typing.Dict[str, abstract_block.AbstractBlock],
        typing.Dict[str, typing.Dict[str, str]],
    ]:
        available_block_modules: typing.Dict[str, abstract_block.AbstractBlock] = {}
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
                        self.trading_mode.logger.exception(
                            error,
                            True,
                            f"Failed to load Strategy Block from {sub_module_name}",
                        )
        return available_block_modules, available_block_modules_info
