from tentacles.Meta.Keywords.block_factory.input_output_nodes.abstract_node import (
    OutputNode,
)
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums


class EntryOrderFilledOutputNode(OutputNode):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.LIME
    NAME: str = "entry_order_filled_output"
    TITLE: str = "Entry Order Filled Output Node"
