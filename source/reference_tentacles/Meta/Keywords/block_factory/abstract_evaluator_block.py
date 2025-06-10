from __future__ import annotations
import tentacles.Meta.Keywords.block_factory as _block_factory
import typing

import octobot_tentacles_manager.constants as constants
import tentacles.Meta.Keywords.block_factory.abstract_action_block as abstract_action_block
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_strategy_block as abstract_strategy_block
from tentacles.Meta.Keywords.block_factory.input_output_nodes.evaluator_signals_input_node import (
    EvaluatorSignalsInputNode,
)


class EvaluatorBlock(_block_factory.AbstractBlock):
    PACKAGES_PATH: str = constants.TENTACLES_STRATEGY_BLOCKS_EVALUATOR_PATH
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.GREEN

    def __init__(
        self,
        trading_mode,
        node_config: dict,
        inputs: dict,
        block_factory: _block_factory.BlockFactory,
    ) -> None:
        super().__init__(
            trading_mode=trading_mode,
            node_config=node_config,
            inputs=inputs,
            block_factory=block_factory,
        )
        self.activate_evaluator_signals_input_node()

    async def execute_block_from_factory(
        self,
        block_factory,
        triggering_block: typing.Optional[abstract_strategy_block.StrategyBlock] = None,
        strategy_signals: typing.Optional[
            abstract_strategy_block.StrategySignals
        ] = None,
    ):
        await super().execute_block_from_factory(
            block_factory=block_factory,
            triggering_block=triggering_block,
        )
        for node in self.output_nodes.values():
            new_strategy_signals_variation: abstract_strategy_block.StrategySignals = (
                strategy_signals.create_new_variation(triggering_block)
                if strategy_signals
                else abstract_strategy_block.StrategySignals(triggering_block)
            )
            new_strategy_signals_variation.add_signals(
                signals=node.data, signals_title=node.data_title
            )
            for handle in node.connected_handle_instances.values():
                handle: EvaluatorSignalsInputNode
                if isinstance(handle.origin_block_instance, EvaluatorBlock):
                    await handle.origin_block_instance.execute_block_from_factory(
                        block_factory=block_factory,
                        triggering_block=triggering_block,
                        strategy_signals=new_strategy_signals_variation,
                    )
                elif isinstance(
                    handle.origin_block_instance, abstract_action_block.ActionBlock
                ):
                    new_strategy_signals_variation.add_action(
                        handle.origin_block_instance
                    )
