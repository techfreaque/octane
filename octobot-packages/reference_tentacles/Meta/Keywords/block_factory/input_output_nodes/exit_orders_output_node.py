from tentacles.Meta.Keywords.block_factory.input_output_nodes.abstract_node import (
    OutputNode,
)
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums


class StopLossOutputNode(OutputNode):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.YELLOW
    NAME: str = "stop_loss_output"
    TITLE: str = "Stop Loss Output Node"


class TakeProfitOutputNode(OutputNode):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.RED
    NAME: str = "take_profit_output"
    TITLE: str = "Take Profit Output Node"
