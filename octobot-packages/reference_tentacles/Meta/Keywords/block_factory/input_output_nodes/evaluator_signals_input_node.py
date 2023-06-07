import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
from tentacles.Meta.Keywords.block_factory.input_output_nodes.abstract_node import (
    InputNode,
)


class EvaluatorSignalsInputNode(InputNode):
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.GREEN
    NAME: str = "evaluator_signals_input"
    TITLE: str = "Evaluator Signals Input Node"
