# prevent circular import error
from __future__ import annotations
import tentacles.Meta.Keywords.block_factory as block_factory

import typing
import octobot_commons.configuration.user_inputs as user_inputs
import octobot_commons.enums as enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums


class InputOutputNode:
    NAME: str = "generic_node"
    TITLE: str = "Generic Node"
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.PURPLE

    def __init__(
        self,
        ui: user_inputs.UserInputFactory,
        inputs: dict,
        node_id: str,
        io_node_id: int,
        title: str,
        side: block_factory_enums.InOutputNodeSides,
        direction: block_factory_enums.InputOutputNodeDirection,
        is_connectable: typing.Union[bool, int],
        node_config_parent: str,
        origin_block_instance: block_factory.AbstractBlock,
    ):
        self.io_node_id: int = io_node_id
        self.node_id: str = node_id
        self.title: str = title
        self.side: block_factory_enums.InOutputNodeSides = side
        self.direction: block_factory_enums.InputOutputNodeDirection = direction
        self.is_connectable: typing.Union[bool, int] = is_connectable
        self.full_io_id: str = f"{self.NAME}{self.io_node_id}"
        self.origin_block_instance: block_factory.AbstractBlock = origin_block_instance
        self.connected_handle_instances: typing.Dict[InputOutputNode] = {}

        # data attributes
        self.data_title: str = None
        self.data = None
        self.data_display_conditions = None
        self.additional_payload_data = None
        self.chart_location: str = None

        # use user_input to pass node schema to frontend
        ui.user_input(
            f"nodes_io_{self.io_node_id}_{self.node_id}",
            enums.UserInputTypes.OBJECT,
            None,
            inputs,
            parent_input_name=node_config_parent,
            editor_options={
                "side": self.side.value,
                "io_node_type": self.NAME,
                "io_node_id": self.io_node_id,
                "direction": self.direction.value,
                "title": self.title,
                "color": self.COLOR.value,
                "is_connectable": self.is_connectable,
            },
            show_in_summary=False,
            show_in_optimizer=False,
        )

    def register_connected_handle_instance(
        self, target_handle_instance: InputOutputNode
    ):
        self.connected_handle_instances[target_handle_instance.node_id]: typing.Dict[
            InputOutputNode
        ] = target_handle_instance

    async def store_data(
        self,
        title: str,
        data,
        chart_location: str = None,
        data_display_conditions=None,
        additional_payload_data=None,
    ):
        self.data_title: str = title
        self.data = data
        self.data_display_conditions = data_display_conditions
        self.additional_payload_data = additional_payload_data
        self.chart_location: str = self.chart_location or chart_location


class InputNode(InputOutputNode):
    NAME: str = "generic_output_node"
    TITLE: str = "Generic Input Node"
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.RED

    def __init__(
        self,
        ui: user_inputs.UserInputFactory,
        inputs: dict,
        node_id: str,
        io_node_id: int,
        title: str,
        side: block_factory_enums.InOutputNodeSides,
        is_connectable: typing.Union[bool, int],
        node_config_parent: str,
        origin_block_instance: block_factory.AbstractBlock,
    ):
        super().__init__(
            ui=ui,
            inputs=inputs,
            node_id=node_id,
            io_node_id=io_node_id,
            title=title,
            side=side,
            is_connectable=is_connectable,
            direction=block_factory_enums.InputOutputNodeDirection.IN,
            node_config_parent=node_config_parent,
            origin_block_instance=origin_block_instance,
        )


class OutputNode(InputOutputNode):
    NAME: str = "generic_output_node"
    TITLE: str = "Generic Output Node"
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.GREEN

    def __init__(
        self,
        ui: user_inputs.UserInputFactory,
        inputs: dict,
        node_id: str,
        io_node_id: int,
        title: str,
        side: block_factory_enums.InOutputNodeSides,
        is_connectable: typing.Union[bool, int],
        node_config_parent: str,
        plot_enabled: bool,
        plot_color: block_factory_enums.Colors,
        output_node_chart_location: str,
        origin_block_instance: block_factory.AbstractBlock,
    ):
        super().__init__(
            ui=ui,
            inputs=inputs,
            node_id=node_id,
            io_node_id=io_node_id,
            title=title,
            side=side,
            is_connectable=is_connectable,
            direction=block_factory_enums.InputOutputNodeDirection.OUT,
            node_config_parent=node_config_parent,
            origin_block_instance=origin_block_instance,
        )
        self.plot_enabled: bool = plot_enabled
        self.plot_color: block_factory_enums.Colors = plot_color
        self.chart_location = output_node_chart_location
