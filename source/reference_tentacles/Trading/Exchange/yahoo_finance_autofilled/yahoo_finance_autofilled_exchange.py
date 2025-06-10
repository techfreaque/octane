import octobot_commons.logging as commons_logging
import octobot_trading.exchanges as exchanges
from ..yahoo_finance.yahoo_finance_exchange import YahooFinance


class YahooFinanceAutofilled(YahooFinance):
    HAS_FETCHED_DETAILS = True

    @staticmethod
    def supported_autofill_exchanges(tentacle_config):
        # return list(tentacle_config["auto_filled"]) if tentacle_config else []
        return [YahooFinance.get_name()]

    @classmethod
    def init_user_inputs_from_class(cls, inputs: dict) -> None:
        pass

    @classmethod
    async def get_autofilled_exchange_details(
        cls, aiohttp_session, tentacle_config, exchange_name
    ):
        return exchanges.ExchangeDetails(
            exchange_name,
            "Yahoo Finance",
            "https://finance.yahoo.com",
            "",
            "https://static.wikia.nocookie.net/logopedia/images/0/03/Yahoo%21_Finance_2019.svg",
            False,
        )

    def _supports_autofill(self, exchange_name):
        return True

    @staticmethod
    def _has_websocket(tentacle_config, exchange_name):
        return False

    @staticmethod
    def _get_autofilled_config(tentacle_config, exchange_name):
        return tentacle_config["auto_filled"][exchange_name]

    def _apply_config(self, autofilled_exchange_details: exchanges.ExchangeDetails):
        self.logger = commons_logging.get_logger(autofilled_exchange_details.name)
        self.tentacle_config[self.REST_KEY] = autofilled_exchange_details.api
        self.tentacle_config[self.HAS_WEBSOCKETS_KEY] = (
            autofilled_exchange_details.has_websocket
        )

    @classmethod
    def is_supporting_sandbox(cls) -> bool:
        return False

    def get_rest_name(self):
        return YahooFinance.get_name()

    @classmethod
    def get_name(cls):
        return cls.__name__
