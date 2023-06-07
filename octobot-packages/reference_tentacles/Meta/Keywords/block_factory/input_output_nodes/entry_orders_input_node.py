from tentacles.Meta.Keywords.block_factory.input_output_nodes.abstract_node import (
    InputNode,
)
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums


class EntryOrderStopLossInputNode(InputNode):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.YELLOW
    NAME: str = "entry_order_stop_loss_input"
    TITLE: str = "Entry Order Stop Loss Input Node"


class EntryOrderTakeProfitInputNode(InputNode):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.RED
    NAME: str = "entry_order_take_profit_input"
    TITLE: str = "Entry Order Take Profit Input Node"
