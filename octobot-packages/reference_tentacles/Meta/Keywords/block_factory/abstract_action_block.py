from __future__ import annotations
import typing
import tentacles.Meta.Keywords.block_factory as _block_factory
import octobot_tentacles_manager.constants as constants
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
from tentacles.Meta.Keywords.block_factory.input_output_nodes import data_input_nodes, data_output_node, evaluator_signals_output_node


class ActionBlock(_block_factory.AbstractBlock):
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

    async def execute_cron_jobs(
        self,
        block_factory,
        triggering_block: typing.Optional[_block_factory.AbstractBlock] = None,
    ):
        """
        Define a cron job that should run on all candles
        in backtesting only on candles with signals or open orders
        """

    async def init_block_data_from_factory(
        self, block_factory, triggering_block: typing.Optional[_block_factory.AbstractBlock] = None
    ):
        self.block_factory = block_factory
        self.triggering_block = triggering_block
        self.next_indicator_output_generator: typing.Iterator[
            data_output_node.IndicatorDataOutputNode
        ] = self._get_next_indicator_output_node()
        self.next_indicator_input_generator: typing.Iterator[
            typing.Union[
                data_input_nodes.SingleIndicatorDataInputNode,
                data_input_nodes.MultiIndicatorDataInputNode,
            ]
        ] = self._get_next_indicator_input_node()
        self.next_evaluator_output_generator: typing.Iterator[
            evaluator_signals_output_node.EvaluatorSignalsOutputNode
        ] = self._get_next_evaluator_output_node()
        await self.init_block_data()

    async def init_block_data(
        self,
    ) -> None:
        """
        Define a actions that should run on every candle in live before execute block gets triggered
        in backtesting this will only be called once
        """
