import json
import flask
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    dev_mode_is_on,
    import_cross_origin_if_enabled,
)
import octobot_services.interfaces.util as interfaces_util
import tentacles.Services.Interfaces.web_interface.util as util
import tentacles.Services.Interfaces.web_interface.login as login


class OrdersCommands:
    CANCEL_ALL = "cancel_all"
    GET_ALL = "get_all"
    CANCEL_ORDER = "cancel_order"
    CANCEL_ORDERS = "cancel_orders"


class PositionsCommands:
    CLOSE_ALL = "close_all"
    GET_ALL = "get_all"
    CLOSE_POSITION = "close_position"


def register_cancel_orders_routes(plugin):
    route = "/orders/<command>"
    methods = ["POST", "GET"]
    if cross_origin := import_cross_origin_if_enabled():
        if dev_mode_is_on():

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            def orders_route(command):
                return _orders_route(command)

        else:

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            @login.login_required_when_activated
            def orders_route(command):
                return _orders_route(command)

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def orders_route(command):
            return _orders_route(command)

    def _orders_route(command):
        if flask.request.method == "GET":
            (
                real_open_orders,
                simulated_open_orders,
            ) = interfaces_util.get_all_open_orders()
            if command == OrdersCommands.CANCEL_ALL:
                orders_to_cancel = []
                if real_open_orders:
                    orders_to_cancel = [order.order_id for order in real_open_orders]
                elif simulated_open_orders:
                    orders_to_cancel = [
                        order.order_id for order in simulated_open_orders
                    ]
                removed_count = interfaces_util.cancel_orders(orders_to_cancel)
                result = f"{removed_count} orders cancelled"
                return flask.jsonify(result)
            if command == OrdersCommands.GET_ALL:
                return json.dumps(
                    {
                        "real_open_orders": real_open_orders,
                        "simulated_open_orders": simulated_open_orders,
                    }
                )
        elif flask.request.method == "POST":
            result = ""
            request_data = flask.request.get_json()
            if command == OrdersCommands.CANCEL_ORDER:
                if interfaces_util.cancel_orders([request_data]):
                    result = "Order cancelled"
                else:
                    return util.get_rest_reply(
                        "Impossible to cancel order: order not found.", 500
                    )
            elif command == OrdersCommands.CANCEL_ORDERS:
                removed_count = interfaces_util.cancel_orders(request_data)
                result = f"{removed_count} orders cancelled"
            return flask.jsonify(result)

    route = "/positions/<command>"
    methods = ["POST", "GET"]
    if cross_origin := import_cross_origin_if_enabled():
        if dev_mode_is_on():

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            def positions(command):
                return _positions(command)

        else:

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            @login.login_required_when_activated
            def positions(command):
                return _positions(command)

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def positions(command):
            return _positions(command)

    def _positions(command):
        if flask.request.method == "GET":
            real_positions, simulated_positions = interfaces_util.get_all_positions()
            if command == PositionsCommands.CLOSE_ALL:
                positions_to_close = [
                    {"symbol": position.symbol, "side": position.side.value}
                    for position in real_positions or simulated_positions
                ]
                if interfaces_util.close_positions(positions_to_close):
                    result = "Positions closed"
                else:
                    return util.get_rest_reply(
                        "Impossible to close position: position already closed.", 500
                    )
                return flask.jsonify(result)
            if command == PositionsCommands.GET_ALL:
                return json.dumps(
                    {
                        "real_positions": real_positions,
                        "simulated_positions": simulated_positions,
                    }
                )
        elif flask.request.method == "POST":
            result = ""
            request_data = flask.request.get_json()

            if command == PositionsCommands.CLOSE_POSITION:
                if interfaces_util.close_positions([request_data]):
                    result = "Position closed"
                else:
                    return util.get_rest_reply(
                        "Impossible to close position: position already closed.", 500
                    )
            return flask.jsonify(result)
