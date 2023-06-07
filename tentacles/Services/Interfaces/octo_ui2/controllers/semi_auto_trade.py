import flask
from tentacles.Services.Interfaces.octo_ui2.utils import basic_utils
from tentacles.Services.Interfaces.web_interface import models
import tentacles.Services.Interfaces.web_interface.login as login
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    dev_mode_is_on,
    import_cross_origin_if_enabled,
)
import octobot_services.api as services_api
import octobot_services.interfaces.util as interfaces_util
import tentacles.Services.Interfaces.web_interface.models.configuration as web_configuration

# big orders might take along time
EXECUTE_TIMEOUT = 500


def register_semi_auto_trade_routes(plugin):
    route = "/trading_mode_command/<command>"
    methods = ["POST"]
    if cross_origin := import_cross_origin_if_enabled():
        if dev_mode_is_on():

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            def semi_auto_trade(command):
                return _semi_auto_trade(command)

        else:

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            @login.login_required_when_activated
            def semi_auto_trade(command):
                return _semi_auto_trade(command)

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def semi_auto_trade(command):
            return _semi_auto_trade(command)

    def _semi_auto_trade(command):
        if flask.request.method == "POST":
            action = flask.request.args.get("action")
            success = True
            response = ""
            if action == "update":
                request_data = flask.request.get_json()
                responses = []
                for tentacle, config in request_data.items():
                    update_success, update_response = models.update_tentacle_config(
                        tentacle, config
                    )
                    success = update_success and success
                    responses.append(update_response)
                response = ", ".join(responses)
            try:
                send_command_to_activated_tentacles(command)
                return {
                    "success": True,
                    "message": "Successfully execute trading mode",
                    "data": response,
                }
            except Exception as error:
                basic_utils.get_octo_ui_2_logger().exception(
                    error, True, "Failed to execute trades"
                )
                raise


def send_command_to_activated_tentacles(command, wait_for_processing=True):
    trading_mode_name = web_configuration.get_config_activated_trading_mode().get_name()
    evaluator_names = [
        evaluator.get_name()
        for evaluator in web_configuration.get_config_activated_evaluators()
    ]
    send_command_to_tentacles(
        command,
        [trading_mode_name] + evaluator_names,
        wait_for_processing=wait_for_processing,
    )


def send_command_to_tentacles(command, tentacle_names: list, wait_for_processing=True):
    for tentacle_name in tentacle_names:
        interfaces_util.run_in_bot_main_loop(
            services_api.send_user_command(
                interfaces_util.get_bot_api().get_bot_id(),
                tentacle_name,
                command,
                None,
                wait_for_processing=wait_for_processing,
            ),
            timeout=EXECUTE_TIMEOUT,
        )
