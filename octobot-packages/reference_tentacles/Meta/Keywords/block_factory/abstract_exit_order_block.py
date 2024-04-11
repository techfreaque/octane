from __future__ import annotations
import tentacles.Meta.Keywords.block_factory as _block_factory
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_action_block as abstract_action_block


class ExitOrderBlock(abstract_action_block.ActionBlock):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.RED

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


class ExitSignalsOrderBlock(abstract_action_block.ActionBlock):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.CYAN
