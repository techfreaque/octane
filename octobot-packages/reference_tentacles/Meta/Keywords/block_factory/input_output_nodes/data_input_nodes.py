from tentacles.Meta.Keywords.block_factory.input_output_nodes.abstract_node import (
    InputNode,
)
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums


class SingleIndicatorDataInputNode(InputNode):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.ORANGE
    NAME: str = "single_indicator_data_input"
    TITLE: str = "Single Indicator Data Input Node"


class MultiIndicatorDataInputNode(InputNode):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.ORANGE
    NAME: str = "multi_indicator_data_input"
    TITLE: str = "Multi Indicator Data Input Node"
