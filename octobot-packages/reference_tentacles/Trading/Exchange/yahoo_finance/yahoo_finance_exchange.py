from octobot_trading import exchanges

from tentacles.Trading.Exchange.yahoo_finance.connector.yfinance_connector import (
    YahooFinanceConnector,
)


class YahooFinance(exchanges.RestExchange):
    DEFAULT_CONNECTOR_CLASS = YahooFinanceConnector

    @classmethod
    def get_name(cls) -> str:
        return "yahoofinance"

    @classmethod
    def is_supporting_exchange(cls, exchange_candidate_name) -> bool:
        return cls.get_name() == exchange_candidate_name

    async def initialize_impl(self):
        await self.connector.initialize()
        self.symbols = self.connector.symbols
        self.time_frames = self.connector.time_frames

    @classmethod
    def init_user_inputs(cls, inputs: dict) -> None:
        """
        Called at constructor, should define all the exchange's user inputs.
        """

    def symbol_exists(self, symbol):
        return True

    @classmethod
    def is_configurable(cls):
        return True

    async def stop(self) -> None:
        await self.connector.stop()
        self.exchange_manager = None

    def get_default_type(self):
        return "spot"

    async def is_market_open(self, symbol: str) -> bool:
        return await self.connector.is_market_open(symbol)
