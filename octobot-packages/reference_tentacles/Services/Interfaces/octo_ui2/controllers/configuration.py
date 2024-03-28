# from flask_cors import cross_origin
import flask
import octobot_commons.constants as commons_constants

from tentacles.Services.Interfaces.octo_ui2.models import config
from tentacles.Services.Interfaces.octo_ui2.utils import basic_utils
from tentacles.Services.Interfaces.octo_ui2 import octo_ui2_plugin
import tentacles.Services.Interfaces.web_interface.login as login
import tentacles.Services.Interfaces.web_interface.login.web_login_manager as web_login_manager
import tentacles.Services.Interfaces.web_interface.models as models
import tentacles.Services.Interfaces.web_interface.util as util
import octobot_backtesting.api as backtesting_api
import octobot_services.interfaces.util as interfaces_util
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import SHARE_YOUR_OCOBOT
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    import_cross_origin_if_enabled,
)


def register_bot_config_routes(plugin):
    route = "/ui_config"
    methods = ["GET", "POST"]

    cross_origin = import_cross_origin_if_enabled()
    if SHARE_YOUR_OCOBOT:
        _cross_origin = import_cross_origin_if_enabled(True)
        @plugin.blueprint.route(route, methods=methods)
        @_cross_origin(origins="*")
        def ui_config():
            return _ui_config()

    elif cross_origin:

        @plugin.blueprint.route(route, methods=methods)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def ui_config():
            return _ui_config()

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def ui_config():
            return _ui_config()

    def _ui_config():
        if flask.request.method == "POST":
            if (
                not web_login_manager.is_login_required()
                or web_login_manager.is_authenticated()
            ):
                try:
                    request_data = flask.request.get_json()
                    return util.get_rest_reply(
                        flask.jsonify(
                            config.save_ui_config(request_data, octo_ui2_plugin.O_UI)
                        )
                    )
                except Exception as e:
                    basic_utils.get_octo_ui_2_logger().exception(e)
                    return util.get_rest_reply(str(e), 500)
            return util.get_rest_reply("You are not logged in", 500)
        return config.get_ui_config(octo_ui2_plugin.O_UI)

    route = "/bot-config"
    if cross_origin := import_cross_origin_if_enabled():

        @plugin.blueprint.route(route)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def bot_config():
            return _bot_config()

    else:

        @plugin.blueprint.route(route)
        @login.login_required_when_activated
        def bot_config():
            return _bot_config()

    def _bot_config():
        if flask.request.method == "GET":
            display_config = interfaces_util.get_edited_config()
            current_profile = models.get_current_profile()
            profiles = models.get_profiles()
            # active_tentacles = models.get_profiles_activated_tentacles({"current_profile": current_profile})

            requested_config_keys = flask.request.args["config_keys"].split(",")
            configs = {
                "configs": {
                    "type": "object",
                    "Title": "Bot Config",
                    "properties": {
                        "profile": {
                            "type": "object",
                            "title": "profile",
                            "properties": {
                                "profile_info": {
                                    "type": "object",
                                    "title": "Profile Info",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "name": {"type": "string"},
                                        "description": {"type": "string"},
                                        "avatar": {"type": "string"},
                                        "read_only": {"type": "boolean"},
                                    },
                                },
                                "crypto-currencies": {
                                    "type": "object",
                                    "title": "Crypto Currencies",
                                    "additionalProperties": {
                                        "type": "object",
                                        "properties": {
                                            "enabled": {"type": "boolean"},
                                            "pairs": {
                                                "type": "array",
                                                "uniqueItems": True,
                                                "items": {"type": "string"},
                                            },
                                            "quote": {"type": "string"},
                                            "add": {
                                                "type": "array",
                                                "uniqueItems": True,
                                                "items": {"type": "string"},
                                            },
                                        },
                                    },
                                },
                                "exchanges": {
                                    "type": "object",
                                    "title": "Exchanges",
                                    "additionalProperties": {
                                        "type": "object",
                                        "properties": {
                                            "enabled": {
                                                "type": "boolean",
                                                "format": "checkbox",
                                                "fieldType": "boolean",
                                            },
                                            "exchange-type": {"type": "string"},
                                        },
                                        "required": ["enabled"],
                                    },
                                },
                                "trader": {
                                    "type": "object",
                                    "title": "Real Trading Settings",
                                    "properties": {
                                        "enabled": {
                                            "type": "boolean",
                                            "format": "checkbox",
                                            "fieldType": "boolean",
                                            "title": "Enable real trading",
                                        },
                                        "load-trade-history": {
                                            "type": "boolean",
                                            "format": "checkbox",
                                            "fieldType": "boolean",
                                            "title": "Load trade history from exchange",
                                        },
                                    },
                                },
                                "trader-simulator": {
                                    "type": "object",
                                    "title": "Simulated Trading Settings",
                                    "properties": {
                                        "enabled": {
                                            "type": "boolean",
                                            "format": "checkbox",
                                            "fieldType": "boolean",
                                            "title": "Enable simulated trading",
                                        },
                                        "fees": {
                                            "type": "object",
                                            "title": "Simulated exchange fees",
                                            "properties": {
                                                "maker": {
                                                    "type": "number",
                                                    "title": "Maker Fees (Market Orders)",
                                                    "minimum": -100,
                                                    "maximum": 100,
                                                },
                                                "taker": {
                                                    "type": "number",
                                                    "title": "Taker Fees (Limit Orders)",
                                                    "minimum": -100,
                                                    "maximum": 100,
                                                },
                                            },
                                            "required": ["maker", "taker"],
                                        },
                                        "starting-portfolio": {
                                            "type": "object",
                                            "title": "Simulated Starting Portfolio",
                                            "additionalProperties": {
                                                "type": "number",
                                                "minimum": 0,
                                            },
                                        },
                                    },
                                    "required": ["fees", "starting-portfolio"],
                                },
                                "trading": {
                                    "type": "object",
                                    "title": "Trading Settings",
                                    "properties": {
                                        "reference-market": {
                                            "type": "string",
                                            "title": "Reference market",
                                        },
                                        "risk": {
                                            "type": "number",
                                            "minimum": 0,
                                            "maximum": 1,
                                            "default": 1,
                                            "options": {"hidden": True},
                                        },
                                        # "current-bot-recording-id": {
                                        #     "type": "integer",
                                        #     "minimum": 1,
                                        # },
                                    },
                                    "required": ["reference-market"],
                                },
                            },
                        },
                    },
                },
                "data": {
                    "profile": {
                        "profile_info": {
                            "avatar": current_profile.avatar,
                            "avatar_path": current_profile.avatar,
                            "description": current_profile.description,
                            "name": current_profile.name,
                            "path": current_profile.path,
                            "read_only": current_profile.read_only,
                            "profile_id": current_profile.profile_id,
                        },
                        "crypto-currencies": current_profile.config[
                            "crypto-currencies"
                        ],
                        "exchanges": current_profile.config["exchanges"],
                        "trader": current_profile.config["trader"],
                        "trader-simulator": current_profile.config["trader-simulator"],
                        "trading": current_profile.config["trading"],
                    }
                },
            }
            configs_to_send = {}
            # for key in requested_config_keys:
            #     try:
            #         paths = key.split("/")
            #         configs_to_send[paths[0]] = configs[paths[0]]
            #     except KeyError:
            #         configs_to_send[key] = {}
            media_url = flask.url_for("tentacle_media", _external=True)

            display_config = interfaces_util.get_edited_config()

            missing_tentacles = set()
            profiles = models.get_profiles()
            config_exchanges = display_config[commons_constants.CONFIG_EXCHANGES]

            # profiles_activated_tentacles = models.get_profiles_activated_tentacles(profiles),
            #
            config_trading = (display_config[commons_constants.CONFIG_TRADING],)
            config_trader = (display_config[commons_constants.CONFIG_TRADER],)
            config_trader_simulator = (
                display_config[commons_constants.CONFIG_SIMULATOR],
            )
            config_symbols = (models.format_config_symbols(display_config),)
            config_reference_market = (
                display_config[commons_constants.CONFIG_TRADING][
                    commons_constants.CONFIG_TRADER_REFERENCE_MARKET
                ],
            )

            real_trader_activated = (
                interfaces_util.has_real_and_or_simulated_traders()[0],
            )

            symbol_list = (
                sorted(
                    models.get_symbol_list(
                        [
                            exchange
                            for exchange in display_config[
                                commons_constants.CONFIG_EXCHANGES
                            ]
                        ]
                    )
                ),
            )
            # full_symbol_list = models.get_all_symbols_dict(),
            evaluator_config = (
                models.get_evaluator_detailed_config(media_url, missing_tentacles),
            )
            strategy_config = (
                models.get_strategy_config(media_url, missing_tentacles),
            )
            evaluator_startup_config = (
                models.get_evaluators_tentacles_startup_activation(),
            )
            trading_startup_config = (
                models.get_trading_tentacles_startup_activation(),
            )

            in_backtesting = (backtesting_api.is_backtesting_enabled(display_config),)

            config_tentacles_by_group = (
                models.get_tentacles_activation_desc_by_group(
                    media_url, missing_tentacles
                ),
            )

            exchanges_details = models.get_exchanges_details(config_exchanges)

            try:
                return util.get_rest_reply(
                    {
                        "success": True,
                        "message": "Successfully fetched profiles data",
                        "data": configs,
                    }
                )

            except Exception as e:
                basic_utils.get_octo_ui_2_logger("plotted_data").exception(e)
                return util.get_rest_reply(str(e), 500)
