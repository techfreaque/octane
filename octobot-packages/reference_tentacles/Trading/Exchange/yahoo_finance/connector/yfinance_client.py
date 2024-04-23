import datetime
import enum
import logging
import time
import typing
import numpy
import yfinance

import octobot_commons.enums as commons_enums
from octobot_commons.symbols.symbol import Symbol
from octobot_commons.symbols.symbol_util import parse_symbol
from .yfinance_symbols_list import symbols


class YFinanceTimeFrames(enum.Enum):
    """
    YFinance supported time frames values
    """

    ONE_MINUTE = "1m"
    TWO_MINUTES = "2m"
    THREE_MINUTES = "3m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    NINETY_MINUTES = "90m"
    ONE_DAY = "1d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"
    THREE_MONTH = "3mo"


SECONDS_PER_DAY = 60 * 60 * 24


class YFinanceClient:
    name: str = "yahoofinance"
    id: str = "yahoofinance"

    symbols: set = symbols
    _TIMEFRAME_MAP = {
        commons_enums.TimeFrames.ONE_MINUTE.value: YFinanceTimeFrames.ONE_MINUTE.value,
        # commons_enums.TimeFrames.THREE_MINUTES.value: YFinanceTimeFrames.THREE_MINUTES.value,
        # commons_enums.TimeFrames.TWO_MINUTES.value: IBKRTimeFrames.TWO_MINUTES.value,
        commons_enums.TimeFrames.FIVE_MINUTES.value: YFinanceTimeFrames.FIVE_MINUTES.value,
        # commons_enums.TimeFrames.TEN_MINUTES.value: IBKRTimeFrames.TEN_MINUTES.value,
        commons_enums.TimeFrames.FIFTEEN_MINUTES.value: YFinanceTimeFrames.FIFTEEN_MINUTES.value,
        commons_enums.TimeFrames.THIRTY_MINUTES.value: YFinanceTimeFrames.THIRTY_MINUTES.value,
        commons_enums.TimeFrames.ONE_HOUR.value: YFinanceTimeFrames.ONE_HOUR.value,
        commons_enums.TimeFrames.ONE_DAY.value: YFinanceTimeFrames.ONE_DAY.value,
        commons_enums.TimeFrames.ONE_WEEK.value: YFinanceTimeFrames.ONE_WEEK.value,
        commons_enums.TimeFrames.ONE_MONTH.value: YFinanceTimeFrames.ONE_MONTH.value,
    }
    max_history_per_call_by_timeframe = {
        commons_enums.TimeFrames.ONE_MINUTE.value: 7,
        # commons_enums.TimeFrames.THREE_MINUTES.value: 180,
        # commons_enums.TimeFrames.TWO_MINUTES.180.value,
        commons_enums.TimeFrames.FIVE_MINUTES.value: 180,
        # commons_enums.TimeFrames.TEN_MINUTES.180.value,
        commons_enums.TimeFrames.FIFTEEN_MINUTES.value: 180,
        commons_enums.TimeFrames.THIRTY_MINUTES.value: 180,
        commons_enums.TimeFrames.ONE_HOUR.value: 180,
        commons_enums.TimeFrames.ONE_DAY.value: 180,
        commons_enums.TimeFrames.ONE_WEEK.value: 180,
        commons_enums.TimeFrames.ONE_MONTH.value: 180,
    }
    max_history_by_timeframe = {
        commons_enums.TimeFrames.ONE_MINUTE.value: 28 * SECONDS_PER_DAY,
        # commons_enums.TimeFrames.THREE_MINUTES.value: 58 * SECONDS_PER_DAY,
        # commons_enums.TimeFrames.TWO_MINUTES.180.value,
        commons_enums.TimeFrames.FIVE_MINUTES.value: 58 * SECONDS_PER_DAY,
        # commons_enums.TimeFrames.TEN_MINUTES.180.value,
        commons_enums.TimeFrames.FIFTEEN_MINUTES.value: 58 * SECONDS_PER_DAY,
        commons_enums.TimeFrames.THIRTY_MINUTES.value: 58 * SECONDS_PER_DAY,
        commons_enums.TimeFrames.ONE_HOUR.value: 728 * SECONDS_PER_DAY,
        commons_enums.TimeFrames.ONE_DAY.value: 730000000 * SECONDS_PER_DAY,
        commons_enums.TimeFrames.ONE_WEEK.value: 730000000 * SECONDS_PER_DAY,
        commons_enums.TimeFrames.ONE_MONTH.value: 730000000 * SECONDS_PER_DAY,
    }

    timeframes: set = {
        commons_enums.TimeFrames.ONE_MINUTE.value,
        # commons_enums.TimeFrames.TWO_MINUTES.value,
        # commons_enums.TimeFrames.THREE_MINUTES.value,
        commons_enums.TimeFrames.FIVE_MINUTES.value,
        # commons_enums.TimeFrames.TEN_MINUTES.value,
        commons_enums.TimeFrames.FIFTEEN_MINUTES.value,
        commons_enums.TimeFrames.THIRTY_MINUTES.value,
        commons_enums.TimeFrames.ONE_HOUR.value,
        commons_enums.TimeFrames.TWO_HOURS.value,
        commons_enums.TimeFrames.THREE_HOURS.value,
        commons_enums.TimeFrames.FOUR_HOURS.value,
        commons_enums.TimeFrames.HEIGHT_HOURS.value,
        commons_enums.TimeFrames.ONE_DAY.value,
        commons_enums.TimeFrames.ONE_WEEK.value,
        commons_enums.TimeFrames.ONE_MONTH.value,
    }

    def convert_timeframe_to_yfinance_timeframe(self, timeframe: str) -> str:
        return self._TIMEFRAME_MAP[timeframe]

    async def close(self):
        pass

    def setSandboxMode(self, is_sandboxed: bool):
        pass

    async def fetch_balance(self, **params: dict):
        return {}

    async def load_markets(self, config_symbols: typing.List[str]):
        logging.getLogger("yfinance").setLevel(logging.CRITICAL)
        self.symbols.add(tuple(config_symbols))

    @staticmethod
    def milliseconds():
        return time.time() * 1000

    async def fetch_trades(self, symbol: str, limit: int, params: dict = None):
        return []

    async def fetch_ohlcv(
        self, symbol: str, time_frame: str, limit: int, since, params: dict = None
    ):
        try:
            history_length = self.max_history_per_call_by_timeframe[time_frame]
        except KeyError:
            raise RuntimeError(
                f"Timeframe {time_frame} is not supported on yahoo finance"
            )
        c_time = time.time()
        parsed_symbol = parse_symbol(symbol)
        max_fetchable_time = c_time - self.max_history_by_timeframe[time_frame]
        since_seconds = since / 1000 if since else None
        if since_seconds and since_seconds < max_fetchable_time:
            since_seconds = max_fetchable_time
        start_datetime = datetime.datetime.utcfromtimestamp(
            since_seconds
            if since_seconds
            else c_time
            - (
                (self.max_history_per_call_by_timeframe[time_frame] - 2)
                * SECONDS_PER_DAY
            )
        ) - datetime.timedelta(days=1)
        start = start_datetime.strftime("%Y-%m-%d")
        end_datetime = start_datetime + datetime.timedelta(days=history_length)
        end = end_datetime.strftime("%Y-%m-%d")
        errors = None
        downloaded_data = None
        try:
            downloaded_data = yfinance.download(
                tickers=parsed_symbol.base,  # list of tickers
                start=start,
                end=end,
                interval=self.convert_timeframe_to_yfinance_timeframe(time_frame),
                prepost=False,  # download pre/post market hours data?
                repair=False,  # repair obvious price errors e.g. 100x?
                progress=False,
                ignore_tz=True,
            )
            errors = yfinance.shared._ERRORS.get(parsed_symbol.base)
        except Exception as error:
            errors = [error]
        if errors is not None:
            test = 1
        timestamps = (
            get_unixtime(numpy.array(downloaded_data.index))
            if downloaded_data is not None
            else []
        )
        if not len(timestamps):
            end_time_stamp = end_datetime.timestamp()
            if c_time > end_time_stamp:
                return await self.fetch_ohlcv(
                    symbol=symbol,
                    time_frame=time_frame,
                    limit=limit,
                    since=end_time_stamp * 1000,
                )

        parsed_candles = [
            [
                timestamps[candle_index],  # add an hour because of timezone offset
                candle[0],
                candle[1],
                candle[2],
                candle[3],
                candle[5],
            ]
            for candle_index, candle in enumerate(numpy.array(downloaded_data))
            if not since_seconds or timestamps[candle_index] >= since_seconds
        ]
        if limit and len(parsed_candles) > limit:
            parsed_candles = parsed_candles[-limit:]
        return parsed_candles

    def market(self, symbol: str):
        parsed_symbol: Symbol = parse_symbol(symbol)
        return {
            # "id": "ETHBTC",
            "symbol": symbol,
            "base": parsed_symbol.base,
            "quote": parsed_symbol.quote,
            # "baseId": "ETH",
            # "quoteId": "BTC",
            # "active": True,
            # "type": "spot",
            # "linear": None,
            # "inverse": None,
            # "spot": True,
            # "swap": False,
            # "future": False,
            # "option": False,
            # "margin": False,
            # "contract": False,
            # "contractSize": False,
            # "expiry": False,
            # "expiryDatetime": False,
            # "optionType": False,
            # "strike": False,
            # "settle": False,
            # "settleId": False,
            # "precision": False,
            # "limits": False,
            # "percentage": False,
            # "feeSide": False,
            # "tierBased": False,
            # "taker": False,
            # "maker": False,
            # "lowercaseId": False,
        }

    async def is_market_open(self, symbol: str) -> bool:
        return False


def get_unixtime(dt64, unit="s"):
    return dt64.astype(f"datetime64[{unit}]").astype(numpy.int64)
