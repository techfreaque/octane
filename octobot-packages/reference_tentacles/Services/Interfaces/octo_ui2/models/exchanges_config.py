from copy import deepcopy
import octobot_commons.constants as commons_constants
import octobot_commons.tentacles_management as tentacles_management
import octobot_services.interfaces.util as interfaces_util
import octobot_trading.api as trading_api
import octobot_trading.exchanges as trading_exchanges

import tentacles.Services.Interfaces.web_interface.models.configuration as configuration
import tentacles.Services.Interfaces.web_interface.models as models


def get_exchanges_config(display_config):
    # prevent modification of config
    config_exchanges = deepcopy(display_config[commons_constants.CONFIG_EXCHANGES])
    tentacles_setup_config = interfaces_util.get_edited_tentacles_config()
    ccxt_simulated_tested_exchanges = models.get_simulated_exchange_list()
    ccxt_tested_exchanges = models.get_tested_exchange_list()
    ccxt_other_exchanges = models.get_other_exchange_list()

    # exchange_managers = {
    #     exchange.name: exchange
    #     for exchange in interfaces.AbstractInterface.get_exchange_managers().items()
    # }
    for exchange_name in (
        ccxt_tested_exchanges + ccxt_simulated_tested_exchanges + ccxt_other_exchanges
    ):
        if exchange_name not in config_exchanges:
            config_exchanges[exchange_name] = {}
        else:
            if config_exchanges[exchange_name].get("enabled"):
                # if exchange_managers.get(exchange_name):
                #     exchange_managers[exchange_name]
                import tentacles.Trading.Exchange as exchanges

                exchange_class = tentacles_management.get_class_from_string(
                    exchange_name,
                    trading_exchanges.AbstractExchange,
                    exchanges,
                    tentacles_management.default_parents_inspection,
                )
                config_exchanges[exchange_name]["configurable"] = (
                    False
                    if exchange_class is None
                    else exchange_class.is_configurable()
                )
                try:
                    validation_data = configuration.are_compatible_accounts(
                        {
                            exchange_name: {
                                "exchange": exchange_name,
                                "apiKey": config_exchanges[exchange_name].get(
                                    "api-key"
                                ),
                                "apiSecret": config_exchanges[exchange_name].get(
                                    "api-secret"
                                ),
                                "apiPassword": config_exchanges[exchange_name].get(
                                    "api-password"
                                ),
                                commons_constants.CONFIG_EXCHANGE_SANDBOXED: config_exchanges[
                                    exchange_name
                                ].get(
                                    commons_constants.CONFIG_EXCHANGE_SANDBOXED
                                ),
                            }
                        }
                    )
                    config_exchanges[exchange_name] = {
                        **config_exchanges[exchange_name],
                        **validation_data[exchange_name],
                    }
                    if config_exchanges[exchange_name].get("exchange_type"):
                        config_exchanges[exchange_name][
                            commons_constants.CONFIG_EXCHANGE_TYPE
                        ] = (
                            config_exchanges[exchange_name][
                                commons_constants.CONFIG_EXCHANGE_TYPE
                            ]
                            or config_exchanges[exchange_name]["exchange_type"]
                        )
                        del config_exchanges[exchange_name]["exchange_type"]
                except:
                    pass
        config_exchanges[exchange_name]["is_tested_simulated"] = (
            exchange_name in ccxt_simulated_tested_exchanges
        )
        config_exchanges[exchange_name]["is_tested"] = (
            exchange_name in ccxt_tested_exchanges
        )
        try:
            config_exchanges[exchange_name]["has_websockets"] = (
                trading_api.supports_websockets(exchange_name, tentacles_setup_config)
            )
            config_exchanges[exchange_name]["supported_exchange_types"] = [
                exchange_type.value
                for exchange_type in trading_api.get_supported_exchange_types(
                    exchange_name, tentacles_setup_config
                )
            ]
            config_exchanges[exchange_name]["default_exchange_type"] = (
                trading_api.get_default_exchange_type(exchange_name)
            )
        except:
            pass
    return config_exchanges
