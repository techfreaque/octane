# prevent circular import error
from __future__ import annotations
import tentacles.Meta.Keywords.block_factory as _block_factory

from copy import deepcopy
import typing
import octobot_commons.enums as enums
import octobot_tentacles_manager.constants as constants

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords import matrix_enums
import tentacles.Meta.Keywords.block_factory.abstract_action_block as abstract_action_block
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums


class StrategyBlock(_block_factory.AbstractBlock):
    PACKAGES_PATH: str = constants.TENTACLES_STRATEGY_BLOCKS_STRATEGY_PATH
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.PURPLE
    TRIGGER_SOURCES: typing.Tuple[str] = (
        enums.ActivationTopics.FULL_CANDLES.value,
        enums.ActivationTopics.IN_CONSTRUCTION_CANDLES.value,
        matrix_enums.TradingModeCommands.TRADING_VIEW_CALLBACK,
    )
    strategy_id: int

    def __init__(
        self,
        trading_mode,
        node_config: dict,
        inputs: dict,
        block_factory: _block_factory.BlockFactory,
    ) -> None:
        self.strategy_id = block_factory.next_strategy_id
        block_factory.next_strategy_id += 1
        super().__init__(
            trading_mode=trading_mode,
            node_config=node_config,
            inputs=inputs,
            block_factory=block_factory,
        )

    def _init_node_config(
        self, inputs: dict, node: dict, title_suffix: typing.Optional[str] = None
    ) -> str:
        return super()._init_node_config(
            inputs=inputs, node=node, title_suffix=f" {self.strategy_id}"
        )

    async def execute_block_from_factory(
        self,
        block_factory: _block_factory.BlockFactory,
        triggering_block: typing.Optional[_block_factory.AbstractBlock] = None,
    ):
        if block_factory.ctx.trigger_source in self.TRIGGER_SOURCES:
            await super().execute_block_from_factory(
                block_factory=block_factory,
                triggering_block=triggering_block,
            )


class StrategySignals:
    def __init__(self, triggering_block: StrategyBlock):
        self.signals = []
        self.actions: typing.List[abstract_action_block.ActionBlock] = []
        self.signals_cache = None
        self.flow_name: str = (
            f"{triggering_block.TITLE_SHORT} {triggering_block.strategy_id}"
        )
        triggering_block.strategy_variations.append(self)

    def add_signals(self, signals, signals_title: typing.Optional[str] = None):
        if signals_title:
            self.flow_name += f" -> {signals_title}"
        self.signals.append(signals)

    def add_action(self, action: abstract_action_block.ActionBlock):
        self.actions.append(action)

    def write_strategy_cache(self, signals_cache):
        self.signals_cache = signals_cache

    def create_new_variation(self, triggering_block: StrategyBlock) -> StrategySignals:
        new_variation: StrategySignals = deepcopy(self)
        triggering_block.strategy_variations.append(new_variation)
        return new_variation
