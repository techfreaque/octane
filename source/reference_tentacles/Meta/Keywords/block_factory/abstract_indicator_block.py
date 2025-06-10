from __future__ import annotations
import typing
import tentacles.Meta.Keywords.block_factory as _block_factory
import octobot_tentacles_manager.constants as constants
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums


class IndicatorBlock(_block_factory.AbstractBlock):
    PACKAGES_PATH: str = constants.TENTACLES_STRATEGY_BLOCKS_INDICATORS_PATH
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.ORANGE

    indicator_id: int

    def __init__(
        self,
        trading_mode,
        node_config: dict,
        inputs: dict,
        block_factory: _block_factory.BlockFactory,
    ) -> None:
        self.indicator_id = block_factory.next_indicator_id
        block_factory.next_indicator_id += 1
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
            inputs=inputs, node=node, title_suffix=f" {self.indicator_id}"
        )
