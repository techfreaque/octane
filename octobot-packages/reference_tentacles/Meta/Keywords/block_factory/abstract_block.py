# prevent circular import error
from __future__ import annotations
import tentacles.Meta.Keywords.block_factory as _block_factory

import typing

import octobot_commons.time_frame_manager as time_frame_manager
import octobot_commons.configuration.user_inputs as user_inputs
import octobot_commons.enums as enums
import octobot_trading.api.symbol_data as symbol_data
import tentacles.Meta.Keywords.scripting_library.data.writing.plotting as plotting

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.plottings.plots as plots
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.write_evaluator_cache as write_evaluator_cache
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.input_output_nodes.abstract_node as abstract_node
import tentacles.Meta.Keywords.block_factory.input_output_nodes.data_input_nodes as data_input_nodes
import tentacles.Meta.Keywords.block_factory.input_output_nodes.data_output_node as data_output_node
import tentacles.Meta.Keywords.block_factory.input_output_nodes.entry_order_filled_output_node as entry_order_filled_output_node
import tentacles.Meta.Keywords.block_factory.input_output_nodes.entry_orders_input_node as entry_orders_input_node
import tentacles.Meta.Keywords.block_factory.input_output_nodes.evaluator_signals_input_node as evaluator_signals_input_node
import tentacles.Meta.Keywords.block_factory.input_output_nodes.evaluator_signals_output_node as evaluator_signals_output_node
import tentacles.Meta.Keywords.block_factory.input_output_nodes.exit_orders_output_node as exit_orders_output_node
import tentacles.Meta.Keywords.block_factory.input_output_nodes.strategy_start_output_node as strategy_start_output_node


class AbstractBlock:
    NAME: str = "overrride_NAME_with_your_name"
    TITLE: str = "Overrride TILE with your name"
    TITLE_SHORT: str = "Overrride TILE_SHORT with your name"
    DESCRIPTION: str = ""
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.ORANGE

    output_nodes: typing.Dict[str, abstract_node.OutputNode]
    input_nodes: typing.Dict[str, abstract_node.OutputNode]

    def init_block_settings(self) -> None:
        """
        override with your block settings here
        """

    async def execute_block(
        self,
    ) -> None:
        """
        override with your block execution code here
        """

    # usefuly methods starting here

    async def get_candles(
        self,
        source_name: str = matrix_enums.PriceDataSources.CLOSE.value,
        time_frame: str = None,
        symbol: str = None,
        block_factory: typing.Optional[_block_factory.BlockFactory] = None,
    ):
        return await self.block_factory.get_candles(
            source_name=source_name,
            time_frame=time_frame or self.custom_time_frame,
            symbol=symbol,
            block_factory=block_factory,
        )

    def user_input(
        self,
        name: str,
        input_type: str,
        def_val,
        min_val=None,
        max_val=None,
        title: str = None,
        options: list = None,
        show_in_summary=True,
        show_in_optimizer=True,
        item_title: str = None,
        order=None,
        parent_input_name=None,
        grid_columns: int = 12,
        description: str = None,
        other_schema_values: dict = {},
        editor_options: dict = {},
        value=None,
        read_only: bool = False,
        is_nested_config=None,
        nested_tentacle=None,
        path=None,
        array_indexes=None,
        return_value_only: bool = True,
        update_parent_value: bool = True,
    ):
        _editor_options = {**editor_options}
        if grid_columns:
            _editor_options[enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value] = (
                grid_columns
            )

        _other_schema_values = {**other_schema_values}
        if description:
            _other_schema_values[
                enums.UserInputOtherSchemaValuesTypes.DESCRIPTION.value
            ] = description
        return self.UI.user_input(
            name=f"{name}_{self.node_parent_input}".replace(" ", "_"),
            input_type=enums.UserInputTypes(input_type),
            def_val=def_val,
            registered_inputs=self.inputs,
            parent_input_name=parent_input_name or self.node_parent_input,
            value=value,
            min_val=min_val,
            max_val=max_val,
            options=options,
            title=title or name,
            item_title=item_title,
            editor_options=_editor_options,
            other_schema_values=_other_schema_values,
            read_only=read_only,
            is_nested_config=is_nested_config,
            nested_tentacle=nested_tentacle,
            show_in_summary=show_in_summary,
            show_in_optimizer=show_in_optimizer,
            path=path,
            order=order,
            array_indexes=array_indexes,
            return_value_only=return_value_only,
            update_parent_value=update_parent_value,
        )

    def activate_single_input_data_node(
        self,
        data_source_name="Data Source",
        def_val="ema",
        enable_oscillators=True,
        enable_price_indicators=True,
        enable_price_data=True,
        enable_volume=True,
        enable_static_value=True,
        enable_force_def_val=False,
        enable_multi_data_indicators=False,
        parent_input_name: str = None,
    ):
        # TODO handle def_val and other parameters
        self.register_block_input_node(
            input_node_class=data_input_nodes.SingleIndicatorDataInputNode,
            node_id=self.block_id,
            inputs=self.inputs,
            input_node_title=data_source_name,
            input_node_id=self.last_io_node_id,
            input_node_is_connectable=1,
            input_node_side=block_factory_enums.InOutputNodeSides.TOP,
        )
        return def_val

    def register_take_profit_orders_input(
        self,
    ):
        self.register_block_input_node(
            input_node_class=entry_orders_input_node.EntryOrderTakeProfitInputNode,
            node_id=self.block_id,
            inputs=self.inputs,
            input_node_title="Take Profits Input",
            input_node_id=self.last_io_node_id,
            input_node_side=block_factory_enums.InOutputNodeSides.TOP,
        )
        # TODO
        take_profit_nodes = [AbstractBlock]
        return take_profit_nodes

    def register_stop_orders_input(
        self,
    ):
        self.register_block_input_node(
            input_node_class=entry_orders_input_node.EntryOrderStopLossInputNode,
            node_id=self.block_id,
            inputs=self.inputs,
            input_node_title="Stop Losses Input",
            input_node_id=self.last_io_node_id,
            input_node_side=block_factory_enums.InOutputNodeSides.BOTTOM,
        )
        # TODO
        stop_loss_nodes = [AbstractBlock]
        return stop_loss_nodes

    def register_stop_orders_output(
        self,
    ):
        self.register_block_output_node(
            output_node_class=exit_orders_output_node.StopLossOutputNode,
            node_id=self.block_id,
            inputs=self.inputs,
            output_node_title="Stop Loss Output",
            output_node_id=self.last_io_node_id,
            output_node_side=block_factory_enums.InOutputNodeSides.TOP,
        )
        # TODO
        stop_loss_nodes = [AbstractBlock]
        return stop_loss_nodes

    def register_take_profit_output(
        self,
    ):
        self.register_block_output_node(
            output_node_class=exit_orders_output_node.TakeProfitOutputNode,
            node_id=self.block_id,
            inputs=self.inputs,
            output_node_title="Take Profit Output",
            output_node_id=self.last_io_node_id,
            output_node_side=block_factory_enums.InOutputNodeSides.BOTTOM,
        )
        # TODO
        stop_loss_nodes = [AbstractBlock]
        return stop_loss_nodes

    def register_order_filled_output(
        self,
    ):
        self.register_block_output_node(
            output_node_class=entry_order_filled_output_node.EntryOrderFilledOutputNode,
            node_id=self.block_id,
            inputs=self.inputs,
            output_node_title="Order Filled Output",
            output_node_id=self.last_io_node_id,
            output_node_side=block_factory_enums.InOutputNodeSides.RIGHT,
        )
        # TODO
        stop_loss_nodes = [AbstractBlock]
        return stop_loss_nodes

    def activate_multiple_input_data_nodes(
        self,
        data_source_name: str = "Data Source",
        def_val: list = ["ema"],
        indicator_group_id: int = 1,
        enable_oscillators: bool = True,
        enable_price_indicators: bool = True,
        enable_price_data: bool = True,
        enable_volume: bool = True,
        enable_static_value: bool = True,
        min_indicators: int = 1,
        # enable_force_def_val: bool = False,
    ) -> typing.Tuple[list, list]:
        # TODO handle def_val and other parameters
        self.register_block_input_node(
            input_node_class=data_input_nodes.MultiIndicatorDataInputNode,
            node_id=self.block_id,
            inputs=self.inputs,
            input_node_title=data_source_name,
            input_node_id=self.last_io_node_id,
            input_node_side=block_factory_enums.InOutputNodeSides.TOP,
        )
        return ["EMA"], [11]

    async def get_input_node_data(
        self, get_additional_node_data: bool = False
    ) -> tuple:
        node = next(self.next_indicator_input_generator)
        if isinstance(node, data_input_nodes.SingleIndicatorDataInputNode):
            for handle in node.connected_handle_instances.values():
                handle: abstract_node.InputOutputNode
                try:
                    await handle.origin_block_instance.execute_block_from_factory(
                        block_factory=self.block_factory,
                        triggering_block=self,
                    )
                    if get_additional_node_data:
                        return (
                            handle.data,
                            handle.data_display_conditions,
                            handle.additional_payload_data,
                            handle.chart_location,
                            handle.data_title,
                        )
                    return handle.data, handle.chart_location, handle.data_title
                except Exception as error:
                    if hasattr(handle.origin_block_instance, "indicator_id"):
                        _block_id = handle.origin_block_instance.indicator_id
                    else:
                        _block_id = ""
                    self.block_factory.ctx.logger.exception(
                        error,
                        True,
                        f"Failed to get input node data for {self.NAME} {_block_id} ({self.block_factory.ctx.symbol} / {self.block_factory.ctx.time_frame})",
                    )
        if get_additional_node_data:
            return [], None, None, None, None
        return [], None, None

    async def get_multi_input_node_data(
        self,
        get_additional_node_data: bool = False,
        symbols: typing.Optional[
            typing.Union[typing.List[str], typing.Set[str]]
        ] = None,
        time_frames: typing.Optional[
            typing.Union[typing.List[str], typing.Set[str]]
        ] = None,
    ) -> typing.List[typing.Tuple[typing.Any, str, str]]:
        node = next(self.next_indicator_input_generator)
        data: typing.Dict[typing.List[typing.Tuple[typing.Any, str, str]]] = {}
        if isinstance(node, data_input_nodes.MultiIndicatorDataInputNode):
            original_time_frame = f"{self.block_factory.ctx.time_frame}"
            original_symbol = f"{self.block_factory.ctx.symbol}"
            for time_frame in time_frames or (self.block_factory.ctx.time_frame,):
                for symbol in symbols or (self.block_factory.ctx.symbol,):
                    key = f"{symbol}-{time_frame}"
                    self.block_factory.ctx.time_frame = time_frame
                    self.block_factory.ctx.symbol = symbol
                    data[key] = []
                    for handle in node.connected_handle_instances.values():
                        handle: abstract_node.InputOutputNode
                        try:
                            await handle.origin_block_instance.execute_block_from_factory(
                                block_factory=self.block_factory,
                                triggering_block=self,
                            )
                            if get_additional_node_data:
                                data[key].append(
                                    (
                                        handle.data,
                                        handle.data_display_conditions,
                                        handle.additional_payload_data,
                                        handle.chart_location,
                                        handle.data_title,
                                    )
                                )
                            else:
                                data[key].append(
                                    (
                                        handle.data,
                                        handle.chart_location,
                                        handle.data_title,
                                    )
                                )
                        except Exception as error:
                            if hasattr(handle.origin_block_instance, "indicator_id"):
                                _block_id = handle.origin_block_instance.indicator_id
                            else:
                                _block_id = ""
                            self.block_factory.ctx.logger.exception(
                                error,
                                True,
                                f"Failed to get input node data for {self.NAME} {_block_id} ({self.block_factory.ctx.symbol} / {self.block_factory.ctx.time_frame})",
                            )
                            if get_additional_node_data:
                                data[key].append(([], None, None, None, None))
                            else:
                                data[key].append(([], None, None))
            self.block_factory.ctx.time_frame = original_time_frame
            self.block_factory.ctx.symbol = original_symbol
        if symbols is None and data is not None:
            return data[
                f"{self.block_factory.ctx.symbol}-{self.block_factory.ctx.time_frame}"
            ]
        return data

    def activate_evaluator_signals_input_node(
        self,
    ) -> None:
        self.register_block_input_node(
            input_node_class=evaluator_signals_input_node.EvaluatorSignalsInputNode,
            node_id=self.block_id,
            inputs=self.inputs,
            input_node_title="Evaluator signals Input",
            input_node_id=self.last_io_node_id,
            input_node_side=block_factory_enums.InOutputNodeSides.LEFT,
        )

    def user_select_color(
        self,
        title: str = "Select the plot color",
        default_color=block_factory_enums.Colors.BLUE,
        name: typing.Optional[str] = None,
        parent_input_name: typing.Optional[str] = None,
    ):
        return block_factory_enums.Colors(
            self.user_input(
                name if name else title.replace(" ", "_"),
                enums.UserInputTypes.OPTIONS.value,
                def_val=block_factory_enums.Colors(default_color).value,
                title=title,
                options=[color.value for color in block_factory_enums.Colors],
                show_in_summary=False,
                show_in_optimizer=False,
                parent_input_name=parent_input_name,
            )
        )

    def user_select_chart_location(
        self,
        title: str = "Select chart location",
        name: typing.Optional[str] = None,
        default_chart_location: str = enums.PlotCharts.MAIN_CHART.value,
        parent_input_name: typing.Optional[str] = None,
    ):
        return self.user_input(
            name if name else title.replace(" ", "_"),
            enums.UserInputTypes.OPTIONS.value,
            def_val=enums.PlotCharts(default_chart_location).value,
            title=title,
            options=[
                chart.value
                for chart in (
                    enums.PlotCharts.MAIN_CHART,
                    enums.PlotCharts.SUB_CHART,
                )
            ],
            show_in_summary=False,
            show_in_optimizer=False,
            parent_input_name=parent_input_name,
        )

    def user_select_candle_source_name(
        self,
        name="Select Candle Source",
        def_val=matrix_enums.PriceDataSources.CLOSE.value,
        enable_volume=False,
        show_in_summary=False,
        show_in_optimizer=False,
        order=None,
        grid_columns=12,
    ):
        available_data_src = [
            matrix_enums.PriceDataSources.OPEN.value,
            matrix_enums.PriceDataSources.HIGH.value,
            matrix_enums.PriceDataSources.LOW.value,
            matrix_enums.PriceDataSources.CLOSE.value,
            matrix_enums.PriceDataSources.HL2.value,
            matrix_enums.PriceDataSources.HLC3.value,
            matrix_enums.PriceDataSources.OHLC4.value,
            matrix_enums.PriceDataSources.HEIKIN_ASHI_OPEN.value,
            matrix_enums.PriceDataSources.HEIKIN_ASHI_HIGH.value,
            matrix_enums.PriceDataSources.HEIKIN_ASHI_LOW.value,
            matrix_enums.PriceDataSources.HEIKIN_ASHI_CLOSE.value,
        ]
        if enable_volume:
            available_data_src.append(matrix_enums.PriceDataSources.VOLUME.value)
        source_name = self.user_input(
            name=name,
            input_type=enums.UserInputTypes.OPTIONS.value,
            def_val=def_val,
            options=available_data_src,
            show_in_summary=show_in_summary,
            show_in_optimizer=show_in_optimizer,
            order=order,
            grid_columns=grid_columns,
        )
        return source_name

    def get_available_time_frames(self) -> list:
        if self._available_time_frames is None:
            if not hasattr(self.trading_mode.exchange_manager, "exchange_config"):
                return []
            self._available_time_frames = [
                tf.value
                for tf in time_frame_manager.sort_time_frames(
                    self.trading_mode.exchange_manager.exchange_config.get_relevant_time_frames()
                )
            ]
        return self._available_time_frames

    def user_select_data_source_time_frame(self) -> typing.Optional[list]:
        available_timeframes: list = self.get_available_time_frames()
        if len(available_timeframes) > 1:
            available_timeframes.insert(0, matrix_enums.CURRENT_TIME_FRAME)
            time_frame = self.user_input(
                "data_time_frame",
                "options",
                def_val=matrix_enums.CURRENT_TIME_FRAME,
                title="Data source time frame",
                options=available_timeframes,
            )
            if time_frame != matrix_enums.CURRENT_TIME_FRAME:
                self.custom_time_frame = time_frame
                return time_frame
        self.custom_time_frame = None
        return None

    def user_select_trigger_time_frames(self) -> list:
        available_time_frames: list = self.get_available_time_frames()
        return self.user_input(
            "trigger_time_frames",
            input_type=enums.UserInputTypes.MULTIPLE_OPTIONS.value,
            def_val=available_time_frames,
            title="Trigger time frames",
            options=available_time_frames,
        )

    def user_select_trigger_time_frame(
        self, title: str = "Trigger time frame", name: str = "trigger_time_frame"
    ) -> str:
        available_time_frames: list = self.get_available_time_frames()
        return self.user_input(
            name,
            input_type=enums.UserInputTypes.OPTIONS.value,
            def_val=available_time_frames,
            title=title,
            options=available_time_frames,
        )

    def get_available_pairs(self) -> list:
        if self._available_pairs is None:
            self._available_pairs = symbol_data.get_config_symbols(
                self.trading_mode.exchange_manager.config, True
            )
        return self._available_pairs

    def user_select_trigger_pairs(self) -> list:
        all_pairs = self.get_available_pairs()
        return self.user_input(
            "trigger_pairs",
            input_type=enums.UserInputTypes.MULTIPLE_OPTIONS,
            title="Trigger pairs",
            def_val=all_pairs,
            options=all_pairs,
        )

    def register_data_output(
        self,
        title: str,
        plot_switch_text: str,
        plot_color_title: str,
        output_node_class: abstract_node.OutputNode,
        output_node_side: block_factory_enums.InOutputNodeSides,
        default_plot_color: block_factory_enums.Colors = block_factory_enums.Colors.GREEN,
        chart_location_title: typing.Optional[str] = None,
        default_chart_location: typing.Optional[
            str
        ] = enums.PlotCharts.MAIN_CHART.value,
        parent_input_name: typing.Optional[str] = None,
    ):
        plot_data: bool = self.user_input(
            name=f"plot_{self.NAME}_{self.last_io_node_id}",
            title=plot_switch_text,
            input_type=enums.UserInputTypes.BOOLEAN.value,
            def_val=True,
            show_in_summary=False,
            show_in_optimizer=False,
            parent_input_name=parent_input_name,
        )
        chart_location: str = None
        plot_color: str = None
        if plot_data:
            plot_color = self.user_select_color(
                default_color=default_plot_color,
                title=plot_color_title,
                parent_input_name=parent_input_name,
            )
            if chart_location_title:
                chart_location = self.user_select_chart_location(
                    default_chart_location=default_chart_location,
                    title=chart_location_title,
                    name=f"chart_{self.NAME}_{self.last_io_node_id}",
                    parent_input_name=parent_input_name,
                )
        else:
            chart_location = default_chart_location
        self.register_block_output_node(
            output_node_class=output_node_class,
            node_id=self.block_id,
            inputs=self.inputs,
            output_node_title=title,
            output_node_id=self.last_io_node_id,
            output_node_side=output_node_side,
            output_node_plot_enabled=plot_data,
            output_node_plot_color=plot_color,
            output_node_chart_location=chart_location,
        )

    # strategies methods
    def register_strategy_start_output_node(
        self, title: str, output_node_plot_enabled: bool
    ):
        self.register_block_output_node(
            output_node_class=strategy_start_output_node.StrategyStartOutputNode,
            node_id=self.block_id,
            inputs=self.inputs,
            output_node_title=title,
            output_node_id=self.last_io_node_id,
            output_node_side=block_factory_enums.InOutputNodeSides.RIGHT,
            output_node_plot_enabled=output_node_plot_enabled,
        )

    async def get_strategy_signals(self):
        for node in self.output_nodes.values():
            for handle in node.connected_handle_instances.values():
                handle: abstract_node.InputOutputNode
                if isinstance(
                    handle.origin_block_instance,
                    _block_factory.EvaluatorBlock,
                ):
                    await handle.origin_block_instance.execute_block_from_factory(
                        block_factory=self.block_factory, triggering_block=self
                    )
                elif isinstance(
                    handle.origin_block_instance,
                    _block_factory.ActionBlock,
                ):
                    # directly connected action blocks
                    new_strategy_signals_variation: _block_factory.StrategySignals = (
                        _block_factory.StrategySignals(triggering_block=self)
                    )
                    new_strategy_signals_variation.add_signals(signals=True)
                    new_strategy_signals_variation.add_action(
                        handle.origin_block_instance
                    )

    # indicators methods
    def register_indicator_data_output(
        self,
        title: str,
        plot_switch_text: str,
        plot_color_switch_title: str,
        chart_location_title: typing.Optional[str] = None,
        default_plot_color: block_factory_enums.Colors = block_factory_enums.Colors.CYAN,
        default_chart_location: typing.Optional[
            str
        ] = enums.PlotCharts.MAIN_CHART.value,
    ):
        self.register_data_output(
            title,
            plot_switch_text=plot_switch_text,
            output_node_class=data_output_node.IndicatorDataOutputNode,
            output_node_side=block_factory_enums.InOutputNodeSides.BOTTOM,
            plot_color_title=plot_color_switch_title,
            default_plot_color=default_plot_color,
            default_chart_location=default_chart_location,
            chart_location_title=chart_location_title,
        )

    async def store_indicator_data(
        self,
        title: str,
        data,
        data_display_conditions=None,
        own_yaxis: bool = False,
        kind="scattergl",
        mode="lines",
        line_shape="linear",
        enable_rounding_plots: bool = False,
        filter_nan_for_plots: bool = False,
        chart_location: typing.Optional[str] = None,
        additional_payload_data=None,
    ):
        if data is None or not len(data):
            self.block_factory.ctx.logger.error(
                f"Data Source: {title} data is empty" " check Candles history size. "
            )
        node = next(self.next_indicator_output_generator)
        source_timeframe = self.custom_time_frame or self.block_factory.ctx.time_frame
        normalized_data = await utilities.normalize_any_time_frame_to_this_time_frame(
            self.block_factory,
            data=data,
            source_time_frame=source_timeframe,
            target_time_frame=self.block_factory.ctx.time_frame,
        )
        if node:
            if node.plot_enabled:
                await self.plot_and_store_indicator_data(
                    title=title,
                    data=normalized_data,
                    data_display_conditions=data_display_conditions,
                    own_yaxis=own_yaxis,
                    kind=kind,
                    mode=mode,
                    line_shape=line_shape,
                    enable_rounding_plots=enable_rounding_plots,
                    filter_nan_for_plots=filter_nan_for_plots,
                    color=node.plot_color.value if node.plot_color else None,
                    chart_location=chart_location or node.chart_location,
                )
            await node.store_data(
                title=title,
                data=normalized_data,
                data_display_conditions=data_display_conditions,
                chart_location=chart_location,
                additional_payload_data=additional_payload_data,
            )
            return
        raise RuntimeError(f"Falied to save data for {title}")

    async def plot_and_store_indicator_data(
        self,
        title: str,
        data,
        data_display_conditions=None,
        own_yaxis: bool = False,
        kind="scattergl",
        mode="lines",
        line_shape="linear",
        color: str = "blue",
        size: typing.Optional[int] = None,
        enable_rounding_plots: bool = False,
        filter_nan_for_plots: bool = False,
        chart_location: typing.Optional[str] = None,
        timeframe: typing.Optional[str] = None,
    ):
        if data is not None and len(data):
            source_timeframe = (
                timeframe or self.custom_time_frame or self.block_factory.ctx.time_frame
            )
            value_key: str = self._get_next_cache_value_key()
            if data_display_conditions is not None:
                time_data = await self.get_candles(
                    matrix_enums.PriceDataSources.TIME.value
                )
                (
                    cutted_data_display_conditions,
                    cutted_data,
                    cutted_time_data,
                ) = utilities.cut_data_to_same_len(
                    (data_display_conditions, data, time_data)
                )
                await plots.plot_conditional(
                    self.block_factory.ctx,
                    value_key=value_key,
                    chart_location=chart_location,
                    title=title,
                    signals=cutted_data_display_conditions,
                    values=cutted_data,
                    times=cutted_time_data,
                    size=size,
                )
            else:
                await write_evaluator_cache.store_indicator_history(
                    self.block_factory,
                    data,
                    value_key=value_key,
                    enable_rounding=enable_rounding_plots,
                    filter_nan_for_plots=filter_nan_for_plots,
                )
                await plotting.plot(
                    self.block_factory.ctx,
                    f"{title} {self.block_factory.ctx.symbol} {source_timeframe}",
                    cache_value=value_key,
                    chart=chart_location,
                    color=color,
                    own_yaxis=own_yaxis,
                    kind=kind,
                    mode=mode,
                    line_shape=line_shape,
                    size=size,
                )

    # evaluators methods
    def register_evaluator_data_output(
        self,
        title: str,
        plot_switch_text: str,
        plot_color_switch_title: str,
        chart_location_title: typing.Optional[str] = None,
        default_plot_color: block_factory_enums.Colors = block_factory_enums.Colors.GREEN,
        default_chart_location: typing.Optional[str] = None,
        parent_input_name: typing.Optional[str] = None,
    ):
        self.register_data_output(
            title,
            plot_switch_text=plot_switch_text,
            output_node_class=evaluator_signals_output_node.EvaluatorSignalsOutputNode,
            output_node_side=block_factory_enums.InOutputNodeSides.RIGHT,
            plot_color_title=plot_color_switch_title,
            default_plot_color=default_plot_color,
            default_chart_location=default_chart_location,
            chart_location_title=chart_location_title,
            parent_input_name=parent_input_name,
        )

    async def store_evaluator_signals(
        self,
        title: str,
        signals,
        signal_values,
        chart_location: str,
        mode: str = "markers",
        kind: str = "scattergl",
        line_shape=None,
        size: int = 10,
        own_yaxis: bool = False,
        reset_cache_before_writing: bool = True,
        allow_signal_extension: bool = False,
    ):
        if signals is None:
            self.block_factory.ctx.logger.error(
                f"Data Source: {title} data is empty" " check Candles history size. "
            )
        node = next(self.next_evaluator_output_generator)
        if node:
            source_timeframe = self.get_block_time_frame()
            # if allow_signal_extension:
            #     evaluator.signal_valid_for = await user_inputs2.user_input2(
            #         maker, evaluator, "extend signal X candles", "int", 0
            #     )
            #     if evaluator.signal_valid_for != 0:
            #         signals = []
            #         for index, signal in enumerate(evaluator.signals):
            #             if signal == 1:
            #                 signals.append(signal)
            #             else:
            #                 try:
            #                     if (
            #                         max(
            #                             evaluator.signals[
            #                                 index - evaluator.signal_valid_for : index
            #                             ]
            #                         )
            #                         == 1
            #                     ):
            #                         signals.append(1)
            #                     else:
            #                         signals.append(0)
            #                 except Exception:
            #                     signals.append(0)
            #         evaluator.signals = signals

            if node.plot_enabled:
                await self.plot_and_store_signals(
                    signal_values=signal_values,
                    signals=signals,
                    reset_cache_before_writing=reset_cache_before_writing,
                    title=title,
                    source_timeframe=source_timeframe,
                    chart_location=chart_location or node.chart_location,
                    plot_color=node.plot_color.value if node.plot_color else None,
                    kind=kind,
                    size=size,
                    mode=mode,
                    line_shape=line_shape,
                    own_yaxis=own_yaxis,
                )
            await node.store_data(
                title=title, data=signals, chart_location=chart_location
            )
            return
        raise RuntimeError(f"Falied to save data for {title}")

    def get_block_time_frame(
        self,
    ) -> str:
        return self.custom_time_frame or self.block_factory.ctx.time_frame

    async def plot_and_store_signals(
        self,
        title: str,
        signals,
        signal_values,
        chart_location: str,
        source_timeframe: typing.Optional[str] = None,
        mode: str = "markers",
        kind: str = "scattergl",
        plot_color: typing.Optional[str] = None,
        line_shape: typing.Optional[str] = None,
        size: int = 10,
        own_yaxis: bool = False,
        reset_cache_before_writing: bool = True,
        should_keep_values: bool = False,
    ):
        _source_timeframe = source_timeframe or self.get_block_time_frame()
        value_key = self._get_next_cache_value_key()
        times = await self.get_candles(matrix_enums.PriceDataSources.TIME.value)
        (
            cutted_times,
            cutted_signal_values,
            cutted_signals,
        ) = utilities.cut_data_to_same_len((times, signal_values, signals))
        values_with_signals = []
        signal_timestamps = []
        for index, signal in enumerate(cutted_signals):
            if signal:
                values_with_signals.append(cutted_signal_values[index])
                signal_timestamps.append(cutted_times[index])
        if reset_cache_before_writing:
            await self.block_factory.ctx.reset_cached_values([value_key])
        if not should_keep_values:
            await self.block_factory.ctx.set_cached_values(
                values=values_with_signals,
                cache_keys=signal_timestamps,
                value_key=value_key,
            )
        await plotting.plot(
            self.block_factory.ctx,
            f"{title} {self.block_factory.ctx.symbol} {_source_timeframe}",
            cache_value=None if should_keep_values else value_key,
            x=signal_timestamps if should_keep_values else None,
            y=values_with_signals if should_keep_values else None,
            chart=chart_location,
            color=plot_color,
            own_yaxis=own_yaxis,
            kind=kind,
            size=size,
            mode=mode,
            line_shape=line_shape,
        )

    # internal methods

    def _get_next_indicator_output_node(
        self,
    ) -> typing.Iterator[data_output_node.IndicatorDataOutputNode]:
        for node in self.output_nodes.values():
            if isinstance(node, data_output_node.IndicatorDataOutputNode):
                yield node

    def _get_next_indicator_input_node(
        self,
    ) -> typing.Iterator[data_output_node.IndicatorDataOutputNode]:
        for node in self.input_nodes.values():
            if isinstance(
                node,
                (
                    data_input_nodes.SingleIndicatorDataInputNode,
                    data_input_nodes.MultiIndicatorDataInputNode,
                ),
            ):
                yield node

    def _get_next_evaluator_output_node(
        self,
    ) -> typing.Iterator[evaluator_signals_output_node.EvaluatorSignalsOutputNode]:
        for node in self.output_nodes.values():
            if isinstance(
                node, evaluator_signals_output_node.EvaluatorSignalsOutputNode
            ):
                yield node

    def _get_next_cache_value_key(self) -> str:
        value_key: str = (
            f"{self.block_factory.last_run_plot_id}"
            if self.block_factory.ctx.exchange_manager.is_backtesting
            else (
                f"lr{self.block_factory.last_run_plot_id}"
                if self.block_factory.live_recording_mode
                else f"l{self.block_factory.last_run_plot_id}"
            )
        )
        self.block_factory.last_run_plot_id += 1
        return value_key

    def __init__(
        self,
        trading_mode,
        node_config: dict,
        inputs: dict,
        block_factory: _block_factory.BlockFactory,
    ) -> None:
        self.trading_mode = trading_mode
        self.UI: user_inputs.UserInputFactory = trading_mode.UI
        self.block_id = node_config["id"]
        self.inputs: dict = inputs
        self.block_factory: _block_factory.BlockFactory = block_factory
        self.triggering_block: typing.Optional[AbstractBlock] = None
        self.plot = True
        self.last_io_node_id: int = 0
        self.custom_time_frame: str = None
        self.output_nodes: typing.Dict[str, abstract_node.OutputNode] = {}
        self.input_nodes: typing.Dict[str, abstract_node.OutputNode] = {}
        self._available_time_frames: list = None
        self._available_pairs: list = None
        self.next_indicator_output_generator: typing.Iterator[
            data_output_node.IndicatorDataOutputNode
        ] = None
        self.next_indicator_input_generator: typing.Iterator[
            typing.Union[
                data_input_nodes.SingleIndicatorDataInputNode,
                data_input_nodes.MultiIndicatorDataInputNode,
            ]
        ] = None
        self.next_evaluator_output_generator: typing.Iterator[
            evaluator_signals_output_node.EvaluatorSignalsOutputNode
        ] = None
        self.UI.user_input(
            self.block_id,
            enums.UserInputTypes.OBJECT,
            None,
            inputs,
            title=(
                f"{node_config['data']['title']} "
                f"({node_config['data']['nodeType']})"
            ),
            parent_input_name=block_factory_enums.CURRENT_NODES_NAME,
        )
        self.block_factory.init_hidden_node_setings(inputs, self.block_id)
        self.node_parent_input: str = self._init_node_config(
            inputs=inputs,
            node=node_config,
        )
        self.node_in_output_parent_input: str = self._init_node_in_output(
            inputs=inputs,
        )

    def register_block_output_node(
        self,
        node_id: str,
        inputs: dict,
        output_node_title: int,
        output_node_id: int,
        output_node_class: abstract_node.InputNode,
        output_node_side: block_factory_enums.InOutputNodeSides,
        output_node_is_connectable: typing.Union[bool, int] = True,
        output_node_plot_enabled: bool = False,
        output_node_plot_color: block_factory_enums.Colors = block_factory_enums.Colors.YELLOW,
        output_node_chart_location: typing.Optional[str] = None,
    ) -> None:
        io_node_instance: abstract_node.OutputNode = output_node_class(
            ui=self.UI,
            inputs=inputs,
            title=output_node_title,
            side=output_node_side,
            node_id=node_id,
            plot_enabled=output_node_plot_enabled,
            io_node_id=output_node_id,
            is_connectable=output_node_is_connectable,
            node_config_parent=self.node_in_output_parent_input,
            plot_color=output_node_plot_color,
            output_node_chart_location=output_node_chart_location,
            origin_block_instance=self,
        )
        self.output_nodes[io_node_instance.full_io_id] = io_node_instance
        self.last_io_node_id += 1

    def register_block_input_node(
        self,
        node_id: str,
        inputs: dict,
        input_node_title: int,
        input_node_id: int,
        input_node_class: abstract_node.InputNode,
        input_node_side: block_factory_enums.InOutputNodeSides,
        input_node_is_connectable: typing.Union[bool, int] = True,
    ) -> None:
        io_node_instance: abstract_node.InputNode = input_node_class(
            ui=self.UI,
            inputs=inputs,
            title=input_node_title,
            side=input_node_side,
            node_id=node_id,
            io_node_id=input_node_id,
            is_connectable=input_node_is_connectable,
            node_config_parent=self.node_in_output_parent_input,
            origin_block_instance=self,
        )
        self.input_nodes[io_node_instance.full_io_id] = io_node_instance
        self.last_io_node_id += 1

    def _init_node_in_output(self, inputs: dict) -> str:
        current_nodes_in_output_name: str = f"nodes_io_{self.block_id}"
        self.UI.user_input(
            current_nodes_in_output_name,
            enums.UserInputTypes.OBJECT,
            None,
            inputs,
            parent_input_name=self.block_id,
            show_in_optimizer=False,
            show_in_summary=False,
        )
        return current_nodes_in_output_name

    def _init_node_config(
        self, inputs: dict, node: dict, title_suffix: typing.Optional[str] = None
    ) -> str:
        current_node_config_name = f"config_{self.block_id}"
        self.UI.user_input(
            current_node_config_name,
            enums.UserInputTypes.OBJECT,
            None,
            inputs,
            parent_input_name=self.block_id,
            title=(
                f"{node['data']['title']}{title_suffix or ''} "
                f"({node['data']['nodeType']})"
            ),
            editor_options={
                enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: True,
                "color": self.COLOR.value,
            },
            other_schema_values={
                enums.UserInputOtherSchemaValuesTypes.DESCRIPTION.value: self.DESCRIPTION,
            },
        )

        return current_node_config_name

    async def execute_block_from_factory(
        self, block_factory, triggering_block: typing.Optional[AbstractBlock] = None
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
        await self.execute_block()
