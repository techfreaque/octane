# import flask
# import tentacles.Services.Interfaces.web_interface.login as login
# import tentacles.Services.Interfaces.web_interface.models as models
# import tentacles.Services.Interfaces.web_interface.util as util
# import octobot_commons.symbols.symbol_util as symbol_util

# from tentacles.Services.Interfaces.octo_ui2.models import octo_ui2
# from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
#     import_cross_origin_if_enabled,
#     dev_mode_is_on,
# )


# def register_plot_routes(plugin):
#     route = "/run_anaylsis_plots"
#     if cross_origin := import_cross_origin_if_enabled():
#         if dev_mode_is_on:

#             @plugin.blueprint.route(route)
#             @cross_origin(origins="*")
#             def run_analysis_plots():
#                 return _run_analysis_plots()

#         else:

#             @plugin.blueprint.route(route)
#             @cross_origin(origins="*")
#             @login.login_required_when_activated
#             def run_analysis_plots():
#                 return _run_analysis_plots()

#     else:

#         @plugin.blueprint.route(route)
#         @login.login_required_when_activated
#         def run_analysis_plots():
#             return _run_analysis_plots()

#     def _run_analysis_plots():
#         try:
#             request_data = flask.request.get_json()
#             trading_mode_class = models.get_config_activated_trading_mode()
#             symbol = symbol_util.convert_symbol(request_data["symbol"], "|")
#             optimizer_id = None
#             backtesting_id = None
#             if not (live_id := int(request_data.get("live_id", 0)) or None):
#                 optimizer_id = int(request_data.get("optimizer_id", 0)) or None
#                 backtesting_id = int(request_data.get("backtesting_id", 0))
#             optimization_campaign = request_data.get("campaign_name", None)
#             exchange_id = request_data.get("exchange_id", None)
#             time_frame = request_data.get("time_frame", None)
#             exchange = request_data.get("exchange", None)
#             analysis_settings = request_data.get("analysis_settings", {})
#             # return util.get_rest_reply(
#             #     {
#             #         "success": True,
#             #         "message": "Successfully fetched plotted data",
#             #         "data": RunAnalysisModePlugin.get_and_execute_run_analysis_mode(
#             #             trading_mode_class=trading_mode_class,
#             #             exchange_name=exchange,
#             #             symbol=symbol,
#             #             time_frame=time_frame,
#             #             optimizer_id=optimizer_id,
#             #             exchange_id=exchange_id,
#             #             backtesting_id=backtesting_id,
#             #             live_id=live_id,
#             #             optimization_campaign_name=optimization_campaign,
#             #             analysis_settings=analysis_settings,
#             #         ),
#             #     },
#             #     200,
#             # )
#         except Exception as error:
#             octo_ui2.get_octo_ui_2_logger("run_analysis_plotted_data").exception(error)
#             return util.get_rest_reply(str(error), 500)
