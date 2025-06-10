from tentacles.Services.Interfaces.octo_ui2.models import neural_net_helper
from tentacles.Services.Interfaces.octo_ui2.utils import basic_utils

import tentacles.Services.Interfaces.web_interface.login as login
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    import_cross_origin_if_enabled,
)

# try:
#     import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.orders.managed_order_pro.daemons.ping_pong.ping_pong_storage as ping_pong_storage
# except (ModuleNotFoundError, ImportError):
#     ping_pong_storage = None


def register_daemons_routes(plugin):
    route = "/stop_training"
    methods = ["POST", "GET"]

    if cross_origin := import_cross_origin_if_enabled():

        @plugin.blueprint.route(route, methods=methods)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def stop_training():
            return _stop_training()

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def stop_training():
            return _stop_training()

    def _stop_training():
        neural_net_helper.SHOULD_STOP_TRAINING = True
        return basic_utils.get_response(success=True)

    route = "/daemons/reset"
    methods = ["POST", "GET"]
    # if ping_pong_storage:
    #     route = "/daemons"
    #     methods = ["POST", "GET"]

    #     if cross_origin := import_cross_origin_if_enabled():

    #         @plugin.blueprint.route(route, methods=methods)
    #         @cross_origin(origins="*")
    #         @login.login_required_when_activated
    #         def daemons():
    #             return _daemons()

    #     else:

    #         @plugin.blueprint.route(route, methods=methods)
    #         @login.login_required_when_activated
    #         def daemons():
    #             return _daemons()

    #     def _daemons():
    #         daemons_data = {}
    #         exchange_managers = interfaces.AbstractInterface.get_exchange_managers()
    #         for exchange_manager in exchange_managers:
    #             if exchange_manager.id not in daemons_data:
    #                 daemons_data[exchange_manager.id] = {}
    #             daemons_data[exchange_manager.id][
    #                 "ping_pong"
    #             ] = ping_pong_storage.get_all_ping_pong_data_as_dict(exchange_manager)
    #         return basic_utils.get_response(success=True, data=daemons_data)

    #     route = "/daemons/reset"
    #     methods = ["POST", "GET"]

    #     if cross_origin := import_cross_origin_if_enabled():

    #         @plugin.blueprint.route(route, methods=methods)
    #         @cross_origin(origins="*")
    #         @login.login_required_when_activated
    #         def reset_daemons():
    #             return _reset_daemons()

    #     else:

    #         @plugin.blueprint.route(route, methods=methods)
    #         @login.login_required_when_activated
    #         def reset_daemons():
    #             return _reset_daemons()

    #     def _reset_daemons():
    #         exchange_managers = interfaces.AbstractInterface.get_exchange_managers()
    #         for exchange_manager in exchange_managers:
    #             ping_pong_storage.reset_all_ping_pong_data(exchange_manager)
    #         return basic_utils.get_response(
    #             success=True,
    #         )
