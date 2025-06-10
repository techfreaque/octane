import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
from tentacles.Meta.Keywords.block_factory.input_output_nodes.abstract_node import (
    OutputNode,
)


class StrategyStartOutputNode(OutputNode):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.GREEN
    NAME: str = "strategy_start_output"
    TITLE: str = "Strategy Start Node"
