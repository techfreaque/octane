from __future__ import annotations
import tentacles.Meta.Keywords.block_factory as _block_factory
import octobot_tentacles_manager.constants as constants
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_block as abstract_block


class ActionBlock(abstract_block.AbstractBlock):
    PACKAGES_PATH: str = constants.TENTACLES_STRATEGY_BLOCKS_ACTION_PATH
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.CYAN

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
