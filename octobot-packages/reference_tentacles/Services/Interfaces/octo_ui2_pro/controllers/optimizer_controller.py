import flask
from tentacles.Services.Interfaces import web_interface
import tentacles.Services.Interfaces.octo_ui2.utils.basic_utils as basic_utils
import tentacles.Services.Interfaces.octo_ui2.models as octo_ui2_models
from tentacles.Services.Interfaces.octo_ui2_pro.models import optimizer_model
import tentacles.Services.Interfaces.web_interface.login as login
import tentacles.Services.Interfaces.web_interface.models as models


def register_optimizer_routes(plugin):
    route = "/optimizer/<command>"
    methods = ["POST", "GET"]
    if cross_origin := octo_ui2_models.import_cross_origin_if_enabled():

        @plugin.blueprint.route(route, methods=methods)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def optimizer(command):
            return _optimizer(command)

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def optimizer(command):
            return _optimizer(command)


def _optimizer(command):
    trading_mode = models.get_config_activated_trading_mode()
    if flask.request.method == "POST":
        try:
            request_data = flask.request.get_json()
            if command == "add":
                return optimizer_model.add_to_optimizer_queue(
                    request_data, trading_mode
                )
            elif command == "update":
                return optimizer_model.update_optimizer_queue(
                    request_data, trading_mode
                )
            elif command == "start":
                return optimizer_model.start_strategy_design_optimizer(
                    trading_mode=trading_mode,
                    request_data=request_data,
                    collector_start_callback=web_interface.send_data_collector_status,
                    start_callback=web_interface.send_strategy_optimizer_status,
                )
                return
        except Exception as error:
            if command in ("add", "update"):
                return optimizer_model.handle_queue_update_fail(error)
            else:
                return optimizer_model.handle_start_fail(error)
    else:
        try:
            return optimizer_model.get_optimizer_queue(trading_mode)
        except Exception as error:
            octo_ui2_models.get_octo_ui_2_logger().exception(
                error, True, "Failed to get optimizer queue"
            )
            return basic_utils.get_response(
                success=False, message=f"Failed to get optimizer queue, error: {error}"
            )
