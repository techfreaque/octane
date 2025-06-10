import typing
from octobot_trading.exchanges.connectors.ccxt.ccxt_connector import CCXTConnector
from tentacles.Trading.Exchange.yahoo_finance.connector.yfinance_client import (
    YFinanceClient,
)


class YahooFinanceConnector(CCXTConnector):
    """
    yfinance library connector
    """

    def __init__(
        self,
        config,
        exchange_manager,
        adapter_class=None,
        additional_config=None,
        rest_name=None,
        force_auth=False,
    ):
        super().__init__(config, exchange_manager)

    def _create_client(self):
        self.client: YFinanceClient = YFinanceClient()
        self.is_authenticated = True
        # self._connect_client()

    def _create_exchange_type(self):
        self.exchange_type = self.exchange_manager.exchange_class_string

    def get_pair_cryptocurrency(self, pair) -> str:
        try:
            return self.client.market(pair)["base"]
        except KeyError:
            pass
        raise ValueError(f"{pair} is not supported")

    async def is_market_open(self, symbol: str) -> bool:
        return await self.client.is_market_open(symbol)

    async def load_symbol_markets(
        self,
        reload=False,
        market_filter: typing.Union[None, typing.Callable[[dict], bool]] = None,
    ):
        config_symbols = [
            pair
            for currency_conf in self.config["crypto-currencies"].values()
            for pair in currency_conf["pairs"]
        ]
        await self.client.load_markets(config_symbols=config_symbols)
