import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
from tentacles.Meta.Keywords.block_factory.input_output_nodes.abstract_node import OutputNode


class IndicatorDataOutputNode(OutputNode):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.ORANGE
    NAME: str = "indicator_data_output"
    TITLE: str = "Indicator Data Output Node"
