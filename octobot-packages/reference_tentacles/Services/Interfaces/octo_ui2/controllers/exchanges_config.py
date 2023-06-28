import flask

import octobot_commons.constants as commons_constants
import octobot_commons.symbols.symbol_util as symbol_util
import octobot_services.constants as services_constants
import octobot_services.interfaces.util as interfaces_util

import tentacles.Services.Interfaces.web_interface.login as login
import tentacles.Services.Interfaces.web_interface.models as models
import tentacles.Services.Interfaces.octo_ui2.utils.basic_utils as basic_utils
import tentacles.Services.Interfaces.octo_ui2.models.exchanges_config as exchanges_config
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    SHARE_YOUR_OCOBOT,
    import_cross_origin_if_enabled,
)


def register_exchanges_routes(plugin):
    route = "/exchanges-info"
    cross_origin = import_cross_origin_if_enabled()
    if SHARE_YOUR_OCOBOT:
        _cross_origin = import_cross_origin_if_enabled(True)

        @plugin.blueprint.route(route)
        @_cross_origin(origins="*")
        def exchanges_info():
            return _exchanges_info()

    elif cross_origin:

        @plugin.blueprint.route(route)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def exchanges_info():
            return _exchanges_info()

    else:

        @plugin.blueprint.route(route)
        @login.login_required_when_activated
        def exchanges_info():
            return _exchanges_info()

    def _exchanges_info():
        selected_profile = flask.request.args.get("select", None)
        next_url = flask.request.args.get("next", None)
        if (
            selected_profile is not None
            and selected_profile != models.get_current_profile().profile_id
        ):
            models.select_profile(selected_profile)
            current_profile = models.get_current_profile()
            flask.flash(f"Switched to {current_profile.name} profile", "success")
        else:
            current_profile = models.get_current_profile()
        if next_url is not None:
            return flask.redirect(next_url)
        display_config = interfaces_util.get_edited_config()

        config_exchanges = display_config[commons_constants.CONFIG_EXCHANGES]
        # enabled_exchanges = trading_api.get_enabled_exchanges_names(display_config)
        # exchange_details = models.get_exchanges_details(config_exchanges)
        all_symbols: set = set()
        symbols_by_exchanges: dict = {}
        for exchange in config_exchanges.keys():
            if config_exchanges[exchange].get("enabled"):
                this_exchange_symbols = models.get_symbol_list([exchange])
                all_symbols.update(this_exchange_symbols)
                symbols_by_exchanges[exchange] = sorted(this_exchange_symbols)

        all_currencies: set = set()
        for symbol in all_symbols:
            parsed_symbol = symbol_util.parse_symbol(symbol)
            all_currencies.add(parsed_symbol.base)
            all_currencies.add(parsed_symbol.quote)

        currency_name_info = {}
        currency_name_info_list = models.get_all_symbols_list()
        for currency in currency_name_info_list:
            currency_name = currency.get("s")
            if currency_name in all_currencies:
                currency_name_info[currency_name] = currency

        return basic_utils.get_response(
            data={
                "config_exchanges": config_exchanges,
                "config_symbols": models.format_config_symbols(display_config),
                "symbols_by_exchanges": symbols_by_exchanges,
                "currency_name_info": currency_name_info,
                # "symbol_list": sorted(
                #     models.get_symbol_list(enabled_exchanges or config_exchanges)
                # ),
                # "exchanges_details": exchange_details,
            },
        )

    route = "/exchanges-list"
    cross_origin = import_cross_origin_if_enabled()
    if SHARE_YOUR_OCOBOT:
        _cross_origin = import_cross_origin_if_enabled(True)

        @plugin.blueprint.route(route)
        @_cross_origin(origins="*")
        def exchanges_list():
            return _exchanges_list()

    elif cross_origin:

        @plugin.blueprint.route(route)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def exchanges_list():
            return _exchanges_list()

    else:

        @plugin.blueprint.route(route)
        @login.login_required_when_activated
        def exchanges_list():
            return _exchanges_list()

    def _exchanges_list():
        display_config = interfaces_util.get_edited_config()
        data = {
            "exchanges": exchanges_config.get_exchanges_config(display_config),
        }
        return basic_utils.get_response(data=data)

    # route = "/services-info"
    # if cross_origin := import_cross_origin_if_enabled():

    #     @plugin.blueprint.route(route)
    #     @cross_origin(origins="*")
    #     @login.login_required_when_activated
    #     def services_info():
    #         return _services_info()

    # else:

    #     @plugin.blueprint.route(route)
    #     @login.login_required_when_activated
    #     def services_info():
    #         return _services_info()

    # def _services_info():
    #     display_config = interfaces_util.get_edited_config()

    #     # service lists
    #     service_list = models.get_services_list()
    #     notifiers_list = models.get_notifiers_list()

    #     data = {
    #         "config_notifications": display_config[
    #             services_constants.CONFIG_CATEGORY_NOTIFICATION
    #         ],
    #         "config_services": display_config[
    #             services_constants.CONFIG_CATEGORY_SERVICES
    #         ],
    #         "services_list": service_list,
    #         "notifiers_list": notifiers_list,
    #     }
    #     return basic_utils.get_response(data=data)

