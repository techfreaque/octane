import octobot_services.interfaces.util as interfaces_util
import tentacles.Services.Interfaces.web_interface.login as login
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import SHARE_YOUR_OCOBOT
import tentacles.Services.Interfaces.web_interface.models as models
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    import_cross_origin_if_enabled,
)


def register_portfolio_routes(plugin):
    route = "/portfolio"

    cross_origin = import_cross_origin_if_enabled()
    if SHARE_YOUR_OCOBOT:
        _cross_origin = import_cross_origin_if_enabled(True)

        @plugin.blueprint.route(route)
        @_cross_origin(origins="*")
        def _portfolio():
            return portfolio()

    elif cross_origin:

        @plugin.blueprint.route(route)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def _portfolio():
            return portfolio()

    else:

        @plugin.blueprint.route(route)
        @login.login_required_when_activated
        def _portfolio():
            return portfolio()

    def portfolio():
        (
            has_real_trader,
            has_simulated_trader,
        ) = interfaces_util.has_real_and_or_simulated_traders()

        displayed_portfolio = models.get_exchange_holdings_per_symbol()
        symbols_values = (
            models.get_symbols_values(
                displayed_portfolio.keys(), has_real_trader, has_simulated_trader
            )
            if displayed_portfolio
            else {}
        )

        (
            _,
            _,
            portfolio_real_current_value,
            portfolio_simulated_current_value,
        ) = interfaces_util.get_portfolio_current_value()

        displayed_portfolio_value = (
            portfolio_real_current_value
            if has_real_trader
            else portfolio_simulated_current_value
        )
        reference_market = interfaces_util.get_reference_market()
        initializing_currencies_prices_set = (
            models.get_initializing_currencies_prices_set(3)
        )

        return {
            "success": True,
            "message": "Successfully fetched portfolio",
            "data": {
                "has_real_trader": has_real_trader,
                "has_simulated_trade": has_simulated_trader,
                "displayed_portfolio": displayed_portfolio,
                "symbols_values": symbols_values,
                "displayed_portfolio_value": round(displayed_portfolio_value, 8),
                "reference_unit": reference_market,
                # "initializing_currencies_prices": initializing_currencies_prices_set
            },
        }
