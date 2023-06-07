import flask
import octobot_services.interfaces as interfaces
import octobot_services.interfaces.util as interfaces_util
import octobot_trading.enums as trading_enums
import tentacles.Services.Interfaces.web_interface.login as login
import tentacles.Services.Interfaces.web_interface.models as models
import tentacles.Services.Interfaces.octo_ui2.utils.basic_utils as basic_utils
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    import_cross_origin_if_enabled,
)


def register_symbols_info_routes(plugin):
    route = "/symbols-info"
    methods = ["GET", "POST"]
    if cross_origin := import_cross_origin_if_enabled():

        @plugin.blueprint.route(route, methods=methods)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def symbols_info():
            return _symbols_info()

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def symbols_info():
            return _symbols_info()

    def _symbols_info():
        if flask.request.method == "POST":
            request_data = flask.request.get_json()
            exchanges = request_data.get("exchanges")
            symbols = request_data.get("symbols")
        else:
            exchanges = None
            symbols = None
        data=interfaces_util.run_in_bot_main_loop(
                get_symbols_infos_by_exchange(exchanges, symbols)
            )
        return basic_utils.get_response(
            success=True if data else False,
            message="Successfully fetched symbols info",
            data=data,
        )


async def get_symbols_infos_by_exchange(exchanges, symbols):
    exchange_managers: list = interfaces.AbstractInterface.get_exchange_managers()
    symbols_info: dict = {}
    for _exchange_manager in exchange_managers:
        if exchanges:
            if _exchange_manager.name not in exchanges:
                continue
        if not _exchange_manager.is_future:
            continue
        if not symbols:
            if _exchange_manager.trading_modes:
                symbols = models.get_enabled_trading_pairs()
            else:
                continue
        symbols_info[_exchange_manager.exchange_name] = {}
        try:
            if not _exchange_manager.is_simulated:
                symbols_info[_exchange_manager.exchange_name][
                    "leverage_tiers"
                ] = await _exchange_manager.exchange.get_leverage_tiers()
        except NotImplementedError:
            pass
        symbols_info[_exchange_manager.exchange_name]["funding"] = {}
        for symbol in symbols:
            ticker_manager = (
                _exchange_manager.exchange_symbols_data.exchange_symbol_data[
                    symbol
                ].ticker_manager
            )
            symbols_info[_exchange_manager.exchange_name]["funding"][symbol] = {
                "funding_rate": ticker_manager.ticker.get(
                    trading_enums.ExchangeConstantsFundingColumns.FUNDING_RATE.value
                ),
                "last_updated": ticker_manager.ticker.get(
                    trading_enums.ExchangeConstantsFundingColumns.LAST_FUNDING_TIME.value
                ),
                "next_update": ticker_manager.ticker.get(
                    trading_enums.ExchangeConstantsFundingColumns.NEXT_FUNDING_TIME.value
                ),
            }
    return symbols_info
