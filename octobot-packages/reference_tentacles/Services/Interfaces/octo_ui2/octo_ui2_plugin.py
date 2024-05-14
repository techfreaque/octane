import os
import octobot.constants as octobot_constants
from octobot_commons import optimization_campaign
import octobot_trading.util as trading_util
import octobot_tentacles_manager.api as tentacles_manager_api
import octobot_commons.constants as commons_constants
import octobot_services.interfaces.util as interfaces_util


import tentacles.Services.Interfaces.web_interface.plugins as plugins
import tentacles.Services.Interfaces.web_interface.models as models
import tentacles.Services.Interfaces.web_interface.enums as web_enums
from .controllers import (
    frontend,
    configuration,
    portfolio,
    plot_data,
    bot_info,
    app_store,
    run_data,
    semi_auto_trade,
    trading,
    daemons,
    tentacles_config,
    symbols_info,
    exchanges_config,
)


class O_UI(plugins.AbstractWebInterfacePlugin):
    NAME = "octo_ui2"
    PLUGIN_ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))

    def register_routes(self):
        frontend.register_frontend_route(self)
        bot_info.register_bot_info_routes(self)
        plot_data.register_plot_data_routes(self)
        configuration.register_bot_config_routes(self)
        portfolio.register_portfolio_routes(self)
        app_store.register_appstore_routes(self)
        run_data.register_run_data_routes(self)
        semi_auto_trade.register_semi_auto_trade_routes(self)
        trading.register_cancel_orders_routes(self)
        tentacles_config.register_tentacles_config_routes(self)
        daemons.register_daemons_routes(self)
        symbols_info.register_symbols_info_routes(self)
        exchanges_config.register_exchanges_routes(self)

    def get_tabs(self):
        return [
            models.WebInterfaceTab(
                "octo_ui2",
                "octo_ui2.home",
                "O UI",
                web_enums.TabsLocation.START,
            )
        ]

    @classmethod
    def get_ui_config(
        cls,
    ):
        campaign_config = cls._get_campaign_config()
        config = tentacles_manager_api.get_tentacle_config(
            interfaces_util.get_edited_tentacles_config(), cls
        )
        if not config:
            config = DEFAULT_CONFIG
        config[octobot_constants.OPTIMIZATION_CAMPAIGN_KEY] = campaign_config
        config["optimizer_campaigns_to_load"][
            campaign_config[commons_constants.CONFIG_NAME]
        ] = True
        config[commons_constants.CONFIG_CURRENT_LIVE_ID] = (
            trading_util.get_current_bot_live_id(interfaces_util.get_edited_config())
        )
        return config

    @classmethod
    def optimization_campaign_name(cls, tentacles_setup_config=None):
        return cls._get_campaign_config(tentacles_setup_config)[
            commons_constants.CONFIG_NAME
        ]

    @classmethod
    def _get_campaign_config(cls, tentacles_setup_config=None):
        config = tentacles_manager_api.get_tentacle_config(
            tentacles_setup_config or interfaces_util.get_edited_tentacles_config(), cls
        )
        campaign_config = config.get(octobot_constants.OPTIMIZATION_CAMPAIGN_KEY, {})
        campaign_config[commons_constants.CONFIG_NAME] = campaign_config.get(
            commons_constants.CONFIG_NAME, commons_constants.DEFAULT_CAMPAIGN
        )
        return campaign_config


optimization_campaign.register_optimization_campaign_name_proxy(
    O_UI.optimization_campaign_name
)

DEFAULT_CONFIG = {
    "backtesting_run_settings": {
        "data_sources": ["current_bot_data"],
        "end_timestamp": None,
        "exchange_names": [],
        "exchange_type": "use_current_profile",
        "start_timestamp": None,
    },
    "display_settings": {
        "graphs": {
            "display_unified_tooltip": True,
            "display_use_log_scale": False,
            "max_candles_before_line_display": 10000,
            "max_candles_line_sources": ["high", "low"],
        }
    },
    "optimizer_campaigns_to_load": {"default_campaign": True},
    "optimizer_run_settings": {
        "data_files": ["current_bot_data"],
        "end_timestamp": None,
        "exchange_names": [],
        "exchange_type": "use_current_profile",
        "idle_cores": 1,
        "notify_when_complete": True,
        "optimizer_id": 1,
        "queue_size": 1000,
        "start_timestamp": None,
    },
}
