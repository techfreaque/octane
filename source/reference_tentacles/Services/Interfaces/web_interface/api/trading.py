#  Drakkar-Software OctoBot-Interfaces
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import flask

import octobot_services.interfaces.util as interfaces_util
import tentacles.Services.Interfaces.web_interface.util as util
import tentacles.Services.Interfaces.web_interface.models as models
import tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 as octo_ui2_models


def register(blueprint):
    @octo_ui2_models.octane_route(blueprint, route="/orders", can_be_shared_public=True)
    def orders():
        return _orders()
        
    @octo_ui2_models.octane_route(blueprint, route="/orders", methods=['POST'])
    def edit_orders():
        return _orders()
    
    def _orders():
        if flask.request.method == 'GET':
            return flask.jsonify(models.get_all_orders_data())
        elif flask.request.method == "POST":
            result = ""
            request_data = flask.request.get_json()
            action = flask.request.args.get("action")
            if action == "cancel_order":
                if interfaces_util.cancel_orders([request_data]):
                    result = "Order cancelled"
                else:
                    return util.get_rest_reply('Impossible to cancel order: order not found.', 500)
            elif action == "cancel_orders":
                removed_count = interfaces_util.cancel_orders(request_data)
                result = f"{removed_count} orders cancelled"
            return flask.jsonify(result)


    @octo_ui2_models.octane_route(blueprint, route="/trades", can_be_shared_public=True)
    def trades():
        return flask.jsonify(models.get_all_trades_data())


    @octo_ui2_models.octane_route(blueprint, route="/positions", can_be_shared_public=True)
    def positions():
        return _positions()
    
    @octo_ui2_models.octane_route(blueprint, route="/positions", methods=['POST'])
    def edit_positions():
        return _positions()
        
    def _positions():
        if flask.request.method == 'GET':
            return flask.jsonify(models.get_all_positions_data())
        elif flask.request.method == "POST":
            result = ""
            request_data = flask.request.get_json()
            action = flask.request.args.get("action")
            if action == "close_position":
                if interfaces_util.close_positions([request_data]):
                    result = "Position closed"
                else:
                    return util.get_rest_reply('Impossible to close position: position already closed.', 500)
            return flask.jsonify(result)


    @octo_ui2_models.octane_route(blueprint, route="/refresh_portfolio", methods=['POST'])
    def refresh_portfolio():
        try:
            interfaces_util.trigger_portfolios_refresh()
            return flask.jsonify("Portfolio(s) refreshed")
        except RuntimeError:
            return util.get_rest_reply("No portfolio to refresh", 500)


    @octo_ui2_models.octane_route(blueprint, route="/currency_list", can_be_shared_public=True)
    def currency_list():
        return flask.jsonify(models.get_all_symbols_list())


    @octo_ui2_models.octane_route(blueprint, route="/historical_portfolio_value", can_be_shared_public=True)
    def historical_portfolio_value():
        currency = flask.request.args.get("currency", "USDT")
        time_frame = flask.request.args.get("time_frame")
        from_timestamp = flask.request.args.get("from_timestamp")
        to_timestamp = flask.request.args.get("to_timestamp")
        exchange = flask.request.args.get("exchange")
        try:
            return flask.jsonify(models.get_portfolio_historical_values(currency, time_frame,
                                                                        from_timestamp, to_timestamp,
                                                                        exchange))
        except KeyError:
            return util.get_rest_reply("No exchange portfolio", 404)


    @octo_ui2_models.octane_route(blueprint, route="/pnl_history", can_be_shared_public=True)
    def pnl_history():
        exchange = flask.request.args.get("exchange")
        symbol = flask.request.args.get("symbol")
        quote = flask.request.args.get("quote")
        since = flask.request.args.get("since")
        scale = flask.request.args.get("scale", "")
        return flask.jsonify(
            models.get_pnl_history(
                exchange=exchange,
                quote=quote,
                symbol=symbol,
                since=since,
                scale=scale,
            )
        )


    @octo_ui2_models.octane_route(blueprint, route="/clear_orders_history", methods=['POST'])
    def clear_orders_history():
        return util.get_rest_reply(models.clear_exchanges_orders_history())


    @octo_ui2_models.octane_route(blueprint, route="/clear_trades_history", methods=['POST'])
    def clear_trades_history():
        return util.get_rest_reply(models.clear_exchanges_trades_history())


    @octo_ui2_models.octane_route(blueprint, route="/clear_portfolio_history", methods=['POST'])
    def clear_portfolio_history():
        return flask.jsonify(models.clear_exchanges_portfolio_history())


    @octo_ui2_models.octane_route(blueprint, route="/clear_transactions_history", methods=['POST'])
    def clear_transactions_history():
        return flask.jsonify(models.clear_exchanges_transactions_history())
