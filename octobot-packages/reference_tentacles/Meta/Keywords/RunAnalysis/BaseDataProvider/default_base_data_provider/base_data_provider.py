import typing
import numpy
import asyncio
import time
import numpy.typing as npt

import octobot_commons.databases.implementations.meta_database as meta_database
import octobot_commons.logging.logging_util as logging_util
import octobot_commons.constants
import octobot_commons.enums as commons_enums
import octobot_commons.logging as commons_logging
import octobot_trading.api.exchange as exchange_api
import octobot_trading.api as trading_api
import octobot_services.interfaces as interfaces
import octobot_backtesting.api as backtesting_api
import tentacles.Meta.Keywords.scripting_library.UI.plots.displayed_elements as displayed_elements

import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.analysis_errors as analysis_errors
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.custom_context as custom_context


class RunAnalysisBaseDataGenerator:
    logger: logging_util.BotLogger = commons_logging.get_logger(
        "RunAnalysisBaseDataGenerator"
    )

    def __init__(
        self,
        ctx: custom_context.Context,
        run_database,
        run_display,
        metadata,
        is_backtesting: bool,
        main_plotted_element: displayed_elements.DisplayedElements,
        sub_plotted_element: displayed_elements.DisplayedElements,
        pie_chart_plotted_element: displayed_elements.DisplayedElements,
        table_plotted_element: displayed_elements.DisplayedElements,
    ):
        self._candles_by_symbol_and_time_frame: typing.Dict[
            str,
            typing.Dict[str, typing.List[npt.NDArray[numpy.float64]]],
        ] = {}
        self._trades = None
        self._orders = None
        self._order_updates = None
        self._historical_portfolio_value = None
        self._start_end_portfolio_values = None
        self._transactions = None
        self._cached_values_by_symbols: dict = {}
        self._symbols_dbs: dict = {}
        self._plotted_elements_by_chart: typing.Dict[
            str, displayed_elements.DisplayedElements
        ] = {}
        self._portfolio_history = None
        self._start_value: float | None = None
        self._value_asset: str | None = None
        self._deposits: dict | None = None
        self._withdrawals: dict | None = None

        self.start_time: typing.Union[float, int] = None
        self.end_time: typing.Union[float, int] = None

        # TODO remove
        self._plotted_elements_by_chart["main-chart"] = main_plotted_element
        self._plotted_elements_by_chart["sub-chart"] = sub_plotted_element
        self._plotted_elements_by_chart["pie-chart"] = pie_chart_plotted_element
        self.table_plotted_element: displayed_elements.DisplayedElements = (
            table_plotted_element
        )
        self.run_database: meta_database.MetaDatabase = run_database
        self.run_display = run_display
        self.ctx: custom_context.Context = ctx
        self.exchange_name: str = ctx.exchange_name
        self.config: dict = ctx.analysis_settings
        self.metadata = metadata
        self.account_type = None
        self.is_backtesting = is_backtesting
        self.ref_market: str = None
        self.trading_type = None
        self.pairs = None

        # TODO check if needed
        self.price_data = None
        self.trades_data = None
        self.starting_portfolio: dict = None
        self.moving_portfolio_data = None
        self.trading_transactions_history: list = None
        self.portfolio_history_by_currency: dict = None
        self.buy_fees_by_currency: dict = None
        self.sell_fees_by_currency: dict = None
        self.total_start_balance_in_ref_market = None
        self.longest_candles = None
        self.funding_fees_history_by_pair = None
        self.realized_pnl_x_data: list = None
        self.realized_pnl_trade_gains_data: list = None
        self.realized_pnl_cumulative: list = None
        self.wins_and_losses_x_data: list = []
        self.wins_and_losses_data: list = []
        self.win_rates_x_data: list = []
        self.win_rates_data: list = []
        self.best_case_growth_x_data: list = []
        self.best_case_growth_data: list = []
        self.historical_portfolio_values_by_coin: dict = None
        self.historical_portfolio_amounts_by_coin: dict = None
        self.historical_portfolio_times: list = None

        self.trading_transactions_history: list = None
        self.buy_fees_by_currency: dict = None
        self.sell_fees_by_currency: dict = None
        self.portfolio_history_by_currency: dict = None

        self.trading_transactions_history: list = None
        self.buy_fees_by_currency: dict = None
        self.sell_fees_by_currency: dict = None
        self.portfolio_history_by_currency: dict = None

    def get_plotted_element(self, chart_location="main-chart"):
        return self._plotted_elements_by_chart[chart_location]

    async def get_candles(self, symbol: str, time_frame: str):
        if not self._candles_by_symbol_and_time_frame.get(symbol, {}).get(time_frame):
            await self._load_candles(symbol, time_frame)
        return self._candles_by_symbol_and_time_frame[symbol][time_frame]

    async def _load_candles(self, symbol: str, time_frame: str):
        candles_sources = await self.get_symbols_db(symbol).all(
            commons_enums.DBTables.CANDLES_SOURCE.value
        )
        # TODO use is backtesting
        if not candles_sources or (
            candles_sources[0][commons_enums.DBRows.VALUE.value]
            == octobot_commons.constants.LOCAL_BOT_DATA
        ):
            candles = await self._get_live_candles(symbol, time_frame)
        else:
            candles = await self._get_backtesting_candles(
                symbol=symbol, time_frame=time_frame, candles_sources=candles_sources
            )
        if not self._candles_by_symbol_and_time_frame.get(symbol):
            self._candles_by_symbol_and_time_frame[symbol] = {}
        self._candles_by_symbol_and_time_frame[symbol][time_frame] = candles

    async def _get_backtesting_candles(
        self, symbol: str, time_frame: str, candles_sources
    ) -> typing.List[npt.NDArray[numpy.float64]]:
        raw_candles = await backtesting_api.get_all_ohlcvs(
            candles_sources[0][commons_enums.DBRows.VALUE.value],
            self.exchange_name,
            symbol,
            commons_enums.TimeFrames(time_frame),
            inferior_timestamp=self.metadata[commons_enums.DBRows.START_TIME.value],
            superior_timestamp=self.metadata[commons_enums.DBRows.END_TIME.value],
        )
        # convert candles timestamp in millis
        opens = []
        highs = []
        lows = []
        closes = []
        volumes = []
        times = []
        for candle in raw_candles:
            opens.append(candle[commons_enums.PriceIndexes.IND_PRICE_OPEN.value])
            highs.append(candle[commons_enums.PriceIndexes.IND_PRICE_HIGH.value])
            lows.append(candle[commons_enums.PriceIndexes.IND_PRICE_LOW.value])
            closes.append(candle[commons_enums.PriceIndexes.IND_PRICE_CLOSE.value])
            volumes.append(candle[commons_enums.PriceIndexes.IND_PRICE_VOL.value])
            times.append(
                float(candle[commons_enums.PriceIndexes.IND_PRICE_TIME.value] * 1000)
            )
        return [
            numpy.array(times),
            numpy.array(opens),
            numpy.array(highs),
            numpy.array(lows),
            numpy.array(closes),
            numpy.array(volumes),
        ]

    async def _get_live_candles(
        self, symbol, time_frame, try_counter=0
    ) -> typing.List[npt.NDArray[numpy.float64]]:
        # TODO get/download history from first tradetime or start time
        # TODO multi exchange
        try_counter += 1
        for exchange_id in exchange_api.get_exchange_ids():
            exchange_manager = trading_api.get_exchange_manager_from_exchange_id(
                exchange_id
            )
            if exchange_manager.exchange_name == self.exchange_name:
                try:
                    raw_candles = trading_api.get_symbol_historical_candles(
                        trading_api.get_symbol_data(
                            exchange_manager, symbol, allow_creation=True
                        ),
                        time_frame,
                    )
                except KeyError as error:
                    running_seconds = (
                        time.time() - interfaces.get_bot_api().get_start_time()
                    )
                    if running_seconds < 120:
                        if try_counter <= 5:
                            await asyncio.sleep(4)
                            return await self._get_live_candles(
                                symbol=symbol,
                                time_frame=time_frame,
                                try_counter=try_counter,
                            )
                    # hack for binance earn pairs that start with LD
                    if symbol.startswith("LD"):
                        return await self._get_live_candles(
                            symbol=symbol[2:],
                            time_frame=time_frame,
                            try_counter=try_counter - 1,
                        )
                    raise analysis_errors.CandlesLoadingError from error
                for index in range(
                    len(raw_candles[commons_enums.PriceIndexes.IND_PRICE_TIME.value])
                ):
                    raw_candles[commons_enums.PriceIndexes.IND_PRICE_TIME.value][
                        index
                    ] *= 1000
                return [
                    raw_candles[commons_enums.PriceIndexes.IND_PRICE_TIME.value],
                    raw_candles[commons_enums.PriceIndexes.IND_PRICE_OPEN.value],
                    raw_candles[commons_enums.PriceIndexes.IND_PRICE_HIGH.value],
                    raw_candles[commons_enums.PriceIndexes.IND_PRICE_LOW.value],
                    raw_candles[commons_enums.PriceIndexes.IND_PRICE_CLOSE.value],
                    raw_candles[commons_enums.PriceIndexes.IND_PRICE_VOL.value],
                ]

    async def get_trades(self, symbols: typing.Optional[typing.List[str]] = None):
        # TODO when live load trades from bot
        if not self._trades:
            await self._load_trades()
        if symbols:
            return [
                trade
                for trade in self._trades
                if trade[commons_enums.DBRows.SYMBOL.value] in symbols
            ]
        return self._trades

    def _filter_plotted_elements_by_time_range(
        self, rows: typing.List[dict]
    ) -> typing.List[dict]:
        if not rows or not len(rows):
            return []
        return [
            row
            for row in rows
            if (
                row[commons_enums.PlotAttributes.X.value] >= self.start_time
                and row[commons_enums.PlotAttributes.X.value] <= self.end_time
            )
        ]

    async def _load_trades(self) -> None:
        self._trades = self._filter_plotted_elements_by_time_range(
            await self.run_database.get_trades_db(
                self.account_type, exchange=self.exchange_name
            ).all(
                commons_enums.DBTables.TRADES.value,
            )
        )

    async def get_open_orders(self):
        if not self._orders:
            await self._load_open_orders()
        return self._orders

    async def _load_open_orders(self):
        self._orders = await self.run_database.get_orders_db(
            self.account_type, exchange=self.exchange_name
        ).all(
            commons_enums.DBTables.ORDERS.value,
        )

    async def get_order_updates(self):
        if not self._order_updates:
            await self._load_order_updates()
        return self._order_updates

    async def _load_order_updates(self):
        self._order_updates = await self.run_database.get_orders_db(
            self.account_type, exchange=self.exchange_name
        ).all(
            commons_enums.DBTables.HISTORICAL_ORDERS_UPDATES.value,
        )

    async def get_historical_portfolio_value(self):
        if not self._historical_portfolio_value:
            await self._load_historical_portfolio_value()
        return self._historical_portfolio_value

    async def get_start_value(
        self, historical_portfolio_value
    ) -> typing.Tuple[float, str | None]:
        if self._start_value is not None and self._value_asset is not None:
            return self._start_value, self._value_asset
        start_end_portfolio_values = await self.get_start_end_portfolio_values()
        self._start_value = 0
        self._value_asset = (
            list(historical_portfolio_value[0]["v"].keys())[0]
            if len(historical_portfolio_value)
            else None
        )
        if (
            len(start_end_portfolio_values)
            and start_end_portfolio_values[0]["starting_portfolio"]
        ):
            for asset_name, asset in start_end_portfolio_values[0][
                "starting_portfolio"
            ].items():
                if asset_name == self._value_asset:
                    self._start_value = asset["total"]
                else:
                    # TODO handle multiple assets
                    self.logger.error(
                        f"Other assets than reference asset is not supported yet : {asset_name} will be ignored in unrealized pnl calculation"
                    )
        else:
            self.logger.error(
                "Starting portfolio not found, unrealized pnl calculation will be based on the first historical portfolio value"
            )
        return self._start_value, self._value_asset

    async def get_deposits_withdrawals(self):
        if self._deposits is not None and self._withdrawals is not None:
            return self._deposits, self._withdrawals

        transactions = await self.get_transactions()

        self._deposits = {}
        self._withdrawals = {}

        for transaction in transactions:
            timestamp = int(transaction["x"] / 1000)
            currency = transaction["currency"]
            quantity = transaction["quantity"]

            if transaction["type"] == "blockchain_deposit":
                if currency not in self._deposits:
                    self._deposits[currency] = {}
                if timestamp not in self._deposits[currency]:
                    self._deposits[currency][timestamp] = 0
                self._deposits[currency][timestamp] += quantity
            elif transaction["type"] == "blockchain_withdrawal":
                if currency not in self._withdrawals:
                    self._withdrawals[currency] = {}
                if timestamp not in self._withdrawals[currency]:
                    self._withdrawals[currency][timestamp] = 0
                self._withdrawals[currency][timestamp] += quantity
        return self._deposits, self._withdrawals

    async def get_historical_unrealized_pnl(self):
        historical_portfolio_value = await self.get_historical_portfolio_value()

        start_value, value_asset = await self.get_start_value(
            historical_portfolio_value
        )

        deposits, withdrawals = await self.get_deposits_withdrawals()

        historical_unrealized_pnl = []

        for day in historical_portfolio_value:
            cumulative_deposits = {value_asset: start_value} if value_asset else {}
            cumulative_withdrawals = {}
            timestamp = day["t"]
            value_by_currency = day["v"]

            for currency, value in value_by_currency.items():
                if currency not in cumulative_deposits:
                    cumulative_deposits[currency] = 0
                if currency not in cumulative_withdrawals:
                    cumulative_withdrawals[currency] = 0

                if currency in deposits:
                    for deposit_time, deposit_amount in deposits[currency].items():
                        if deposit_time < timestamp:
                            cumulative_deposits[currency] += deposit_amount

                if currency in withdrawals:
                    for withdrawal_time, withdrawal_amount in withdrawals[
                        currency
                    ].items():
                        if withdrawal_time < timestamp:
                            cumulative_withdrawals[currency] += withdrawal_amount

                adjusted_value = (
                    value
                    - cumulative_deposits[currency]
                    + cumulative_withdrawals[currency]
                )

                if not any(d["t"] == timestamp for d in historical_unrealized_pnl):
                    historical_unrealized_pnl.append({"t": timestamp, "v": {}})
                historical_unrealized_pnl[-1]["v"][currency] = adjusted_value

        return historical_unrealized_pnl

    async def _load_historical_portfolio_value(self):
        self._historical_portfolio_value = self._filter_cached_value_by_time_range(
            (
                await self.run_database.get_historical_portfolio_value_db(
                    self.account_type, exchange=self.exchange_name
                ).all(commons_enums.RunDatabases.HISTORICAL_PORTFOLIO_VALUE.value)
            )
        )

    async def get_start_end_portfolio_values(self):
        if not self._start_end_portfolio_values:
            await self._load_start_end_portfolio_values()
        return self._start_end_portfolio_values

    async def _load_start_end_portfolio_values(self):
        self._start_end_portfolio_values = (
            await self.run_database.get_historical_portfolio_value_db(
                self.account_type, exchange=self.exchange_name
            ).all(commons_enums.RunDatabases.METADATA.value)
        )

    def _filter_cached_value_by_time_range(
        self, rows: typing.List[dict]
    ) -> typing.List[dict]:
        if not rows or not len(rows):
            return []
        return [
            row
            for row in rows
            if (
                row[commons_enums.CacheDatabaseColumns.TIMESTAMP.value] * 1000
                >= self.start_time
                and row[commons_enums.CacheDatabaseColumns.TIMESTAMP.value] * 1000
                <= self.end_time
            )
        ]

    async def get_cached_values(self, symbol: str):
        if not self._cached_values_by_symbols.get(symbol):
            await self._load_cached_values(symbol)
        return self._cached_values_by_symbols[symbol]

    async def _load_cached_values(self, symbol: str):
        self._cached_values_by_symbols[symbol] = await self.get_symbols_db(symbol).all(
            commons_enums.DBTables.CACHE_SOURCE.value
        )

    def get_symbols_db(self, symbol: str):
        if not self._symbols_dbs.get(symbol):
            self._load_symbols_db(symbol)
        return self._symbols_dbs[symbol]

    def _load_symbols_db(self, symbol: str):
        self._symbols_dbs[symbol] = self.run_database.get_symbol_db(
            self.exchange_name, symbol
        )

    async def get_transactions(self):
        if not self._transactions:
            await self._load_transactions()
        return self._transactions

    async def _load_transactions(self):
        self._transactions = await self.run_database.get_transactions_db(
            self.account_type, exchange=self.exchange_name
        ).all(
            commons_enums.DBTables.TRANSACTIONS.value,
        )

    async def load_base_data(self, exchange_id: str):
        # self.load_starting_portfolio()
        # self.exchange_name = (
        #     self.exchange_name
        #     or self.metadata[commons_enums.DBRows.EXCHANGES.value][0]
        #     or (
        #         self.run_database.run_dbs_identifier.context.exchange_name
        #         if self.run_database.run_dbs_identifier.context
        #         else None
        #     )
        # )
        # TODO handle multi exchanges
        self.ref_market = self.metadata[commons_enums.DBRows.REFERENCE_MARKET.value]

        self.trading_type = self.metadata[commons_enums.DBRows.TRADING_TYPE.value]

        self.account_type = (
            trading_api.get_account_type_from_run_metadata(self.metadata)
            if self.is_backtesting
            else trading_api.get_account_type_from_exchange_manager(
                trading_api.get_exchange_manager_from_exchange_id(exchange_id)
            )
        )

        # contracts = (
        #     self.metadata[commons_enums.DBRows.FUTURE_CONTRACTS.value][
        #         self.exchange_name
        #     ]
        #     if self.trading_type == "future"
        #     else {}
        # )

        if self.metadata["end_time"] == -1:
            self.end_time = 10000000000000
            candles = await self.get_candles(
                symbol=self.ctx.symbol, time_frame=self.ctx.time_frame
            )
            if candles and len(candles) and len(candles[0]):
                self.start_time = candles[0][
                    commons_enums.PriceIndexes.IND_PRICE_TIME.value
                ]
            else:
                self.start_time = 0
            self.end_time = 10000000000000

        else:
            self.start_time = self.metadata["start_time"] * 1000
            self.end_time = self.metadata["end_time"] * 1000

        # todo all coins balance
        # self.total_start_balance_in_ref_market = self.starting_portfolio.get(
        #     self.ref_market, {}
        # ).get("total", 0)
        # self.pairs = list(self.trades_data)
        # self._set_longest_candles()

    # def load_starting_portfolio(self) -> dict:
    #     portfolio = self.metadata[
    #         commons_enums.BacktestingMetadata.START_PORTFOLIO.value
    #     ]
    #     self.starting_portfolio = json.loads(portfolio.replace("'", '"'))

    # async def load_historical_values(
    #     self,
    #     exchange_name: str,
    #     exchange_id: str,
    #     symbol: str,
    #     time_frame: str,
    #     is_backtesting: bool,
    # ):
    #     self.price_data = {}
    #     self.trades_data = {}
    #     self.moving_portfolio_data = {}

    # await self.run_database.get_symbol_db(self.exchange_name, pair)

    # # init data
    # for pair in self.metadata[commons_enums.DBRows.SYMBOLS.value]:
    #     symbol = symbol_util.parse_symbol(pair).base
    #     is_inverse_contract = (
    #         self.trading_type == "future"
    #         and trading_api.is_inverse_future_contract(
    #             trading_enums.FutureContractType(contracts[pair]["contract_type"])
    #         )
    #     )
    #     if symbol != self.ref_market or is_inverse_contract:
    #         candles_sources = await self.run_database.get_symbol_db(
    #             self.exchange_name, pair
    #         ).all(commons_enums.DBTables.CANDLES_SOURCE.value)
    #         time_frames = None
    #         if time_frame is None:
    #             time_frames = [
    #                 source[commons_enums.DBRows.TIME_FRAME.value]
    #                 for source in candles_sources
    #             ]
    #             time_frame = (
    #                 time_frame_manager.find_min_time_frame(time_frames)
    #                 if time_frames
    #                 else time_frame
    #             )
    #         if with_candles and pair not in self.price_data:
    #             try:
    #                 self.price_data[pair] = await self._get_candles(
    #                     candles_sources, pair, time_frame
    #                 )
    #             except KeyError as error:
    #                 if did_retry:
    #                     raise analysis_errors.CandlesLoadingError(
    #                         f"Unable to load {pair}/{time_frames} candles"
    #                     ) from error
    #                 await asyncio.sleep(5)
    #                 return await self.load_historical_values(
    #                     exchange=exchange,
    #                     with_candles=with_candles,
    #                     with_trades=with_trades,
    #                     with_portfolio=with_portfolio,
    #                     time_frame=time_frame,
    #                     did_retry=True,
    #                 )
    #         if with_trades and pair not in self.trades_data:
    #             self.trades_data[pair] = await self.get_trades(pair)
    #     if with_portfolio:
    #         try:
    #             self.moving_portfolio_data[symbol] = self.starting_portfolio[
    #                 symbol
    #             ][octobot_commons.constants.PORTFOLIO_TOTAL]
    #         except KeyError:
    #             self.moving_portfolio_data[symbol] = 0
    #         try:
    #             self.moving_portfolio_data[
    #                 self.ref_market
    #             ] = self.starting_portfolio[self.ref_market][
    #                 octobot_commons.constants.PORTFOLIO_TOTAL
    #             ]
    #         except KeyError:
    #             self.moving_portfolio_data[self.ref_market] = 0

    # async def generate_historical_portfolio_value(self, total_amount_in_btc=False):
    #     if not self.historical_portfolio_values_by_coin:
    #         if self.trading_type == "future":
    #             # TODO remove when FuturesBaseDataGenerator is added
    #             return
    #         self.historical_portfolio_values_by_coin: dict = {}
    #         self.historical_portfolio_amounts_by_coin: dict = {}
    #         self.historical_portfolio_times = [
    #             candle[commons_enums.PriceIndexes.IND_PRICE_TIME.value]
    #             for candle in self.longest_candles
    #         ]
    #         _tmp_portfolio_history_by_currency = {**self.portfolio_history_by_currency}
    #         longest_candles_len = len(self.longest_candles)
    #         for coin in self.portfolio_history_by_currency.keys():
    #             _this_tmp_portfolio_history = _tmp_portfolio_history_by_currency[coin]
    #             static_price_data = False
    #             price_data = None
    #             if self.ref_market == coin:
    #                 static_price_data = True
    #             else:
    #                 # handle indirect multi pair conversion
    #                 try:
    #                     price_data = self.price_data[f"{coin}/{self.ref_market}"]
    #                 except KeyError as error:
    #                     # if coin in self.pairs:

    #                     # conversion_symbol = f"{parsed_symbol.quote}/{ref_market}"
    #                     # converion_price = None
    #                     # if conversion_symbol not in price_data:
    #                     #     conversion_symbol = f"{ref_market}/{parsed_symbol.quote}"
    #                     #     if conversion_symbol not in price_data:
    #                     #         run_analysis_data.get_base_data_logger().error(
    #                     #             f"Unable to handle sell trade {trade['symbol']}, no pair "
    #                     #             "aivailable to convert value plots "
    #                     #             f"will not be accurate: {trade}"
    #                     #         )
    #                     #         break
    #                     # conversion_pair = f"{}/{self.ref_market}"
    #                     self.logger.exception(
    #                         error,
    #                         True,
    #                         f"Unable to get price data for {coin}/{self.ref_market} "
    #                         "- make sure this pair is enabled for this run - "
    #                         "Run analysis plots will not be accurate!",
    #                     )
    #                     continue
    #                 candles_len = len(price_data)
    #                 if longest_candles_len != candles_len:
    #                     # add 0 values to make all candles the same len
    #                     price_data = (
    #                         [[0, 0, 0, 0, 0]] * (longest_candles_len - candles_len)
    #                     ) + price_data

    #             self.historical_portfolio_values_by_coin[coin] = []
    #             self.historical_portfolio_amounts_by_coin[coin] = []
    #             current_amount = 0
    #             for index in range(longest_candles_len):
    #                 if static_price_data:
    #                     price = 1
    #                 else:
    #                     price = price_data[index][
    #                         commons_enums.PriceIndexes.IND_PRICE_CLOSE.value
    #                     ]
    #                 time = self.longest_candles[index][
    #                     commons_enums.PriceIndexes.IND_PRICE_TIME.value
    #                 ]
    #                 # get currency amount closest to current candle time
    #                 while (
    #                     len(_this_tmp_portfolio_history)
    #                     and _this_tmp_portfolio_history[0]["x"] <= time
    #                 ):
    #                     current_amount = _this_tmp_portfolio_history[0]["volume"]
    #                     del _this_tmp_portfolio_history[0]
    #                 self.historical_portfolio_values_by_coin[coin].append(
    #                     price * current_amount
    #                 )
    #                 self.historical_portfolio_amounts_by_coin[coin].append(
    #                     current_amount
    #                 )

    #         # total value in ref_market
    #         pairs = list(self.historical_portfolio_amounts_by_coin.keys())
    #         self.historical_portfolio_values_by_coin["total"] = []
    #         self.historical_portfolio_amounts_by_coin["total"] = []
    #         self.historical_portfolio_values_by_coin["total_btc"] = []
    #         btc_ref_market_symbol = None
    #         if total_amount_in_btc:
    #             btc_ref_market_symbol = f"BTC/{self.ref_market}"
    #             btc_ref_market_price_data = (
    #                 self.price_data[btc_ref_market_symbol]
    #                 if btc_ref_market_symbol in self.price_data
    #                 else None
    #             )

    #             btc_ref_market_price_data_len = len(btc_ref_market_price_data)
    #             if longest_candles_len == btc_ref_market_price_data_len:
    #                 pass
    #             elif longest_candles_len > btc_ref_market_price_data_len:
    #                 empty_candles_to_add = (
    #                     longest_candles_len - btc_ref_market_price_data_len
    #                 )
    #                 btc_ref_market_price_data = [
    #                     [0, 0, 0, 0, 0, 0]
    #                 ] * empty_candles_to_add + btc_ref_market_price_data
    #             else:
    #                 self.logger.error(
    #                     f"{btc_ref_market_symbol} cant be longer than the longest candle"
    #                 )
    #         for index in range(longest_candles_len):
    #             time = self.longest_candles[index][
    #                 commons_enums.PriceIndexes.IND_PRICE_TIME.value
    #             ]
    #             this_candle_value = 0
    #             for pair in pairs:
    #                 this_candle_value += self.historical_portfolio_values_by_coin[pair][
    #                     index
    #                 ]
    #             self.historical_portfolio_values_by_coin["total"].append(
    #                 this_candle_value
    #             )
    #             if btc_ref_market_symbol:
    #                 try:
    #                     self.historical_portfolio_values_by_coin["total_btc"].append(
    #                         this_candle_value
    #                         / btc_ref_market_price_data[index][
    #                             commons_enums.PriceIndexes.IND_PRICE_CLOSE.value
    #                         ]
    #                     )
    #                 except ZeroDivisionError:
    #                     self.historical_portfolio_values_by_coin["total_btc"].append(
    #                         None
    #                     )

    # def _set_longest_candles(self) -> list:
    #     longest_pair = None
    #     longest_len = 0
    #     for pair, candles in self.price_data.items():
    #         if pair not in self.pairs:
    #             continue
    #         if (new_len := len(candles)) > longest_len:
    #             longest_len = new_len
    #             longest_pair = pair
    #     self.longest_candles = self.price_data[longest_pair]

    # def _read_pnl_from_transactions(
    #     self,
    #     x_data,
    #     pnl_data,
    #     cumulative_pnl_data,
    #     x_as_trade_count,
    # ):
    #     previous_value = 0
    #     for transaction in self.trading_transactions_history:
    #         transaction_pnl = (
    #             0
    #             if transaction["realized_pnl"] is None
    #             else transaction["realized_pnl"]
    #         )
    #         transaction_quantity = (
    #             0 if transaction["quantity"] is None else transaction["quantity"]
    #         )
    #         local_quantity = transaction_pnl + transaction_quantity
    #         cumulated_pnl = local_quantity + previous_value
    #         pnl_data.append(local_quantity)
    #         cumulative_pnl_data.append(cumulated_pnl)
    #         previous_value = cumulated_pnl
    #         if x_as_trade_count:
    #             x_data.append(len(pnl_data) - 1)
    #         else:
    #             x_data.append(transaction[commons_enums.PlotAttributes.X.value])

    # async def load_realized_pnl(
    #     self,
    #     x_as_trade_count=True,
    # ):
    #     # PNL:
    #     # 1. open position: consider position opening fee from PNL
    #     # 2. close position: consider closed amount + closing fee into PNL
    #     # what is a trade ?
    #     #   futures: when position going to 0 (from long/short) => trade is closed
    #     #   spot: when position lowered => trade is closed
    #     if not (self.price_data and next(iter(self.price_data.values()))):
    #         return
    #     self.realized_pnl_x_data = [
    #         0
    #         if x_as_trade_count
    #         else next(iter(self.price_data.values()))[0][
    #             commons_enums.PriceIndexes.IND_PRICE_TIME.value
    #         ]
    #     ]
    #     self.realized_pnl_trade_gains_data = [0]
    #     self.realized_pnl_cumulative = [0]
    #     if self.trading_transactions_history:
    #         # can rely on pnl history
    #         self._read_pnl_from_transactions(
    #             self.realized_pnl_x_data,
    #             self.realized_pnl_trade_gains_data,
    #             self.realized_pnl_cumulative,
    #             x_as_trade_count,
    #         )
    #         # else:
    #         #     # recreate pnl history from trades
    #         #     self._read_pnl_from_trades(
    #         #         x_data,
    #         #         pnl_data,
    #         #         cumulative_pnl_data,
    #         #         x_as_trade_count,
    #         #     )

    #         if not x_as_trade_count:
    #             # x axis is time: add a value at the end of the axis if missing
    #             # to avoid a missing values at the end feeling
    #             last_time_value = next(iter(self.price_data.values()))[-1][
    #                 commons_enums.PriceIndexes.IND_PRICE_TIME.value
    #             ]
    #             if self.realized_pnl_x_data[-1] != last_time_value:
    #                 # append the latest value at the end of the x axis
    #                 self.realized_pnl_x_data.append(last_time_value)
    #                 self.realized_pnl_trade_gains_data.append(0)
    #                 self.realized_pnl_cumulative.append(
    #                     self.realized_pnl_cumulative[-1]
    #                 )

    # async def total_paid_fees(meta_database, all_trades):
    #     paid_fees = 0
    #     fees_currency = None
    #     if trading_transactions_history:
    #         for transaction in trading_transactions_history:
    #             if fees_currency is None:
    #                 fees_currency = transaction["currency"]
    #             if transaction["currency"] != fees_currency:
    #                 get_base_data_logger().error(f"Unknown funding fee value: {transaction}")
    #             else:
    #                 # - because funding fees are stored as negative number when paid (positive when "gained")
    #                 paid_fees -= transaction["quantity"]
    #     for trade in all_trades:
    #         currency = symbol_util.parse_symbol(
    #             trade[commons_enums.DBTables.SYMBOL.value]
    #         ).base
    #         if trade[commons_enums.DBRows.FEES_CURRENCY.value] == currency:
    #             if trade[commons_enums.DBRows.FEES_CURRENCY.value] == fees_currency:
    #                 paid_fees += trade[commons_enums.DBRows.FEES_AMOUNT.value]
    #             else:
    #                 paid_fees += (
    #                     trade[commons_enums.DBRows.FEES_AMOUNT.value]
    #                     * trade[commons_enums.PlotAttributes.Y.value]
    #                 )
    #         else:
    #             if trade[commons_enums.DBRows.FEES_CURRENCY.value] == fees_currency:
    #                 paid_fees += (
    #                     trade[commons_enums.DBRows.FEES_AMOUNT.value]
    #                     / trade[commons_enums.PlotAttributes.Y.value]
    #                 )
    #             else:
    #                 paid_fees += trade[commons_enums.DBRows.FEES_AMOUNT.value]
    #     return paid_fees

    # def generate_wins_and_losses(self, x_as_trade_count):
    #     if not (self.wins_and_losses_x_data and self.wins_and_losses_data):
    #         if not (self.price_data and next(iter(self.price_data.values()))):
    #             return
    #         if self.trading_transactions_history:
    #             # can rely on pnl history
    #             for transaction in self.trading_transactions_history:
    #                 transaction_pnl = (
    #                     0
    #                     if transaction["realized_pnl"] is None
    #                     else transaction["realized_pnl"]
    #                 )
    #                 current_cumulative_wins = (
    #                     self.wins_and_losses_data[-1]
    #                     if self.wins_and_losses_data
    #                     else 0
    #                 )
    #                 if transaction_pnl < 0:
    #                     self.wins_and_losses_data.append(current_cumulative_wins - 1)
    #                 elif transaction_pnl > 0:
    #                     self.wins_and_losses_data.append(current_cumulative_wins + 1)
    #                 else:
    #                     continue

    #                 if x_as_trade_count:
    #                     self.wins_and_losses_x_data.append(
    #                         len(self.wins_and_losses_data) - 1
    #                     )
    #                 else:
    #                     self.wins_and_losses_x_data.append(
    #                         transaction[commons_enums.PlotAttributes.X.value]
    #                     )

    # def generate_win_rates(self, x_as_trade_count):
    #     if not (self.win_rates_x_data and self.win_rates_data):
    #         if not (self.price_data and next(iter(self.price_data.values()))):
    #             return
    #         if self.trading_transactions_history:
    #             wins_count = 0
    #             losses_count = 0

    #             for transaction in self.trading_transactions_history:
    #                 transaction_pnl = (
    #                     0
    #                     if transaction["realized_pnl"] is None
    #                     else transaction["realized_pnl"]
    #                 )
    #                 if transaction_pnl < 0:
    #                     losses_count += 1
    #                 elif transaction_pnl > 0:
    #                     wins_count += 1
    #                 else:
    #                     continue

    #                 self.win_rates_data.append(
    #                     (wins_count / (losses_count + wins_count)) * 100
    #                 )
    #                 if x_as_trade_count:
    #                     self.win_rates_x_data.append(len(self.win_rates_data) - 1)
    #                 else:
    #                     self.win_rates_x_data.append(
    #                         transaction[commons_enums.PlotAttributes.X.value]
    #                     )

    # async def get_best_case_growth_from_transactions(
    #     self,
    #     x_as_trade_count,
    # ):
    #     if not (self.best_case_growth_x_data and self.best_case_growth_data):
    #         if not (self.price_data and next(iter(self.price_data.values()))):
    #             return
    #         if self.trading_transactions_history:
    #             (
    #                 self.best_case_growth_data,
    #                 _,
    #                 _,
    #                 _,
    #                 self.best_case_growth_x_data,
    #             ) = await portfolio_util.get_coefficient_of_determination_data(
    #                 transactions=self.trading_transactions_history,
    #                 longest_candles=self.longest_candles,
    #                 start_balance=self.total_start_balance_in_ref_market,
    #                 use_high_instead_of_end_balance=True,
    #                 x_as_trade_count=x_as_trade_count,
    #             )

    # async def generate_transactions(self):
    #     raise NotImplementedError("generate_transactions() must be implemented")


# def _position_factory(symbol, contract_data):
#     # TODO: historical unrealized pnl, maybe find a better solution that this
#     import mock

#     class _TraderMock:
#         def __init__(self):
#             self.exchange_manager = mock.Mock()
#             self.simulate = True

#     contract = trading_exchange_data.FutureContract(
#         symbol,
#         trading_enums.MarginType(contract_data["margin_type"]),
#         trading_enums.FutureContractType(contract_data["contract_type"]),
#     )
#     return trading_personal_data.create_position_from_type(_TraderMock(), contract)
