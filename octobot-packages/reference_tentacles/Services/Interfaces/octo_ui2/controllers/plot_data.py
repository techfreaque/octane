import flask

from tentacles.Services.Interfaces.octo_ui2.utils import basic_utils
import tentacles.Services.Interfaces.web_interface.login as login
import tentacles.Services.Interfaces.web_interface.models as models
import tentacles.Services.Interfaces.web_interface.util as util
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import SHARE_YOUR_OCOBOT
import octobot_commons.symbols.symbol_util as symbol_util
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    import_cross_origin_if_enabled,
)


def register_plot_data_routes(plugin):
    route = "/plotted_run_data"
    methods = ["POST"]

    cross_origin = import_cross_origin_if_enabled()
    if SHARE_YOUR_OCOBOT:
        _cross_origin = import_cross_origin_if_enabled(True)

        @plugin.blueprint.route(route, methods=methods)
        @_cross_origin(origins="*")
        def run_plotted_data():
            return _run_plotted_data()

    elif cross_origin:

        @plugin.blueprint.route(route, methods=methods)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def run_plotted_data():
            return _run_plotted_data()

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def run_plotted_data():
            return _run_plotted_data()

    def _run_plotted_data():
        from tentacles.Services.Interfaces.run_analysis_mode.run_analysis_modes_plugin import (
            RunAnalysisModePlugin,
        )

        try:
            request_data = flask.request.get_json()
            trading_mode = models.get_config_activated_trading_mode()
            symbol = (
                symbol_util.convert_symbol(request_data["symbol"], "|")
                if request_data.get("symbol")
                else None
            )
            optimizer_id = None
            backtesting_id = None
            if not (live_id := int(request_data.get("live_id", 0)) or None):
                optimizer_id = int(request_data.get("optimizer_id", 0)) or None
                backtesting_id = int(request_data.get("backtesting_id", 0))
            optimization_campaign = request_data.get("campaign_name", None)
            exchange_id = request_data.get("exchange_id", None)
            time_frame = request_data.get("time_frame", None)
            exchange = request_data.get("exchange", None)
            return util.get_rest_reply(
                {
                    "success": True,
                    "message": "Successfully fetched plotted data",
                    "data": RunAnalysisModePlugin.get_and_execute_run_analysis_mode(
                        trading_mode_class=trading_mode,
                        exchange_name=exchange,
                        exchange_id=exchange_id,
                        symbol=symbol,
                        time_frame=time_frame,
                        backtesting_id=backtesting_id,
                        optimizer_id=optimizer_id,
                        optimization_campaign=optimization_campaign
                        if not live_id
                        else None,
                        live_id=live_id,
                    ),
                },
                200,
            )
        except Exception as error:
            basic_utils.get_octo_ui_2_logger("run_analysis_plotted_data").exception(
                error,
                True,
                f"Failed to get run analysis plotted data. Request: {request_data}",
            )
            return util.get_rest_reply(str(error), 500)
