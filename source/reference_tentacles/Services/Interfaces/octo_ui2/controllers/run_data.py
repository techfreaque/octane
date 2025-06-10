import flask
import flask_login

from tentacles.Services.Interfaces.octo_ui2.utils import basic_utils
from tentacles.Services.Interfaces.web_interface import models
import tentacles.Services.Interfaces.web_interface.login as login
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    SHARE_YOUR_OCOBOT,
    dev_mode_is_on,
    import_cross_origin_if_enabled,
)
from tentacles.Services.Interfaces.web_interface.login import web_login_manager
import tentacles.Services.Interfaces.web_interface.util as util
import tentacles.Services.Interfaces.octo_ui2.models.run_data as run_data_models


def register_run_data_routes(plugin):
    route = "/backtesting_runs/<command>"
    methods = ["POST"]
    cross_origin = import_cross_origin_if_enabled()
    if SHARE_YOUR_OCOBOT:
        _cross_origin = import_cross_origin_if_enabled(True)

        @plugin.blueprint.route(route, methods=methods)
        @_cross_origin(origins="*")
        def run_data(command):
            return _run_data(command)

    elif cross_origin:
        if dev_mode_is_on():

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            def run_data(command):
                return _run_data(command)

        else:

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            @login.login_required_when_activated
            def run_data(command):
                return _run_data(command)

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def run_data(command):
            return _run_data(command)

    def _run_data(command):
        request_data = flask.request.get_json()
        if command == "get":
            try:
                return util.get_rest_reply(
                    {
                        "success": True,
                        "message": "Successfully fetched run data",
                        "data": run_data_models.get_backtesting_run_data(request_data),
                    },
                    200,
                )
            except Exception as error:
                basic_utils.get_octo_ui_2_logger("run_data").exception(error)
                return util.get_rest_reply(str(error), 500)
        elif command == "delete" and (
            not web_login_manager.is_login_required()
            or web_login_manager.is_authenticated()
        ):
            trading_mode = models.get_config_activated_trading_mode()
            runs = request_data.get("runs", [])
            return util.get_rest_reply(
                run_data_models.delete_run_data(trading_mode, runs), 200
            )
