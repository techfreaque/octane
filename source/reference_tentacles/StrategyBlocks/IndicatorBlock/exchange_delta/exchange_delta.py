# a42.ch CONFIDENTIAL
# __________________
#
#  [2021] - [∞] a42.ch Incorporated
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of a42.ch Incorporated and its suppliers,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to a42.ch Incorporated
# and its suppliers and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from a42.ch Incorporated.
#
# If you want to use any code for commercial purposes,
# or you want your own custom solution,
# please contact me at max@a42.ch

from octobot_trading.api.exchange import (
    get_all_exchange_ids_from_matrix_id,
    get_exchange_managers_from_exchange_ids,
    get_matrix_id_from_exchange_id,
)
from octobot_commons import enums
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
    get_similar_symbol,
)
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block



class ExchangeDeltaIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "exchange_delta"
    TITLE = "Exchange A and B delta"
    TITLE_SHORT = "Exchange Delta"
    DESCRIPTION = (
        "Exchange delta can be used to to compare prices "
        "of the same asset on different exchanges"
    )
    candle_source: str
    to_exchange: str
    plot_precent: bool
    plot_fees: bool

    exchange_managers = None

    def init_block_settings(self) -> None:
        self.candle_source = self.user_select_candle_source_name(
            "Select Candle Source", enable_volume=True
        )
        matrix_id = get_matrix_id_from_exchange_id(
            exchange_name=self.block_factory.trading_mode.exchange_manager.exchange_name,
            exchange_id=self.block_factory.trading_mode.exchange_manager.id,
        )
        exchange_ids = get_all_exchange_ids_from_matrix_id(matrix_id)
        self.exchange_managers = get_exchange_managers_from_exchange_ids(exchange_ids)
        exchanges = [
            exchange_manager.exchange_name
            for exchange_manager in self.exchange_managers
        ]
        # from_exchange = await user_input2(
        #     maker, indicator, "From exchange", "options", exchanges[0], options=exchanges
        # )
        self.to_exchange = self.user_input(
            "Reference exchange",
            "options",
            exchanges[-1],
            options=exchanges,
        )
        self.plot_precent = self.user_input(
            "Plot percent insted of prices",
            "boolean",
            True,
        )
        # TODO

        # self.plot_fees = self.user_input(
        #     "Plot fees as a horizontal line",
        #     "boolean",
        #     False,
        # )
        # if self.plot_fees:
        #     self.register_indicator_data_output(
        #         title=self.TITLE_SHORT,
        #         plot_switch_text="Plot fees for this exchange",
        #         plot_color_switch_title="Fees plot color",
        #         default_plot_color=block_factory_enums.Colors.PURPLE,
        #         chart_location_title="Fees chart location",
        #         default_chart_location=enums.PlotCharts.SUB_CHART.value,
        #     )
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=self.TITLE_SHORT,
            plot_switch_text=f"Plot {self.TITLE_SHORT}",
            plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
            default_plot_color=block_factory_enums.Colors.PURPLE,
            chart_location_title=f"{self.TITLE_SHORT} chart location",
            default_chart_location=enums.PlotCharts.SUB_CHART.value
            if self.candle_source == matrix_enums.PriceDataSources.VOLUME.value
            else enums.PlotCharts.MAIN_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        from_closes = None
        to_closes = None
        from_exchange_fee = None
        from_closes = await self.get_candles()
        from_exchange_fee = None
        # data_source = {
        #     "v": {
        #         "title": f" candle {self.candle_source} delta from "
        #         f"{maker.ctx.exchange_manager.exchange_name} to {self.to_exchange}",
        #         "chart_location": "sub-chart",
        #     },
        #     "f": {
        #         "title": f"{maker.ctx.exchange_manager.exchange_name} "
        #         f"{self.candle_source} price",
        #         "chart_location": "main-chart",
        #     },
        #     "t": {
        #         "title": f"{self.to_exchange} {self.candle_source} price",
        #         "chart_location": "main-chart",
        #     },
        #     "lf": {
        #         "title": f"Long Maker and Taker fee for "
        #         f"{maker.ctx.exchange_manager.exchange_name}",
        #         "chart_location": "sub-chart",
        #     },
        #     "hf": {
        #         "title": f"Short Maker and Taker fee for "
        #         f"{maker.ctx.exchange_manager.exchange_name}",
        #         "chart_location": "sub-chart",
        #     },
        #     "llf": {
        #         "title": f"Long Maker and Maker fee for "
        #         f"{maker.ctx.exchange_manager.exchange_name}",
        #         "chart_location": "sub-chart",
        #     },
        #     "hlf": {
        #         "title": f"Short Maker and Maker fee for "
        #         f"{maker.ctx.exchange_manager.exchange_name}",
        #         "chart_location": "sub-chart",
        #     },
        # }
        # if self.plot_fees:
        #     from_exchange_fee = position_sizing.get_fees(
        #         self.block_factory.ctx, use_decimal=False
        #     )
        #     limit_fee, market_fee = from_exchange_fee
        #     data_len = len(from_closes)
        #     from_exchange_fee_low = [limit_fee + market_fee] * data_len
        #     from_exchange_fee_high = [(market_fee + limit_fee) * -1] * data_len
        #     from_exchange_fee_low_limit = [limit_fee * 2] * data_len
        #     from_exchange_fee_high_limit = [limit_fee * -2] * data_len
        #     # TODO
        #     # data_source["lf"]["data"] = from_exchange_fee_low
        #     # data_source["hf"]["data"] = from_exchange_fee_high
        #     # data_source["llf"]["data"] = from_exchange_fee_low_limit
        #     # data_source["hlf"]["data"] = from_exchange_fee_high_limit
        try:
            for exchange_manager in self.exchange_managers:
                if self.to_exchange == exchange_manager.exchange_name:
                    to_closes = await self.get_candles(
                        source_name=self.candle_source,
                        symbol=get_similar_symbol(
                            symbol=self.block_factory.ctx.symbol,
                            this_exchange_manager=self.block_factory.ctx.exchange_manager,
                            other_exchange_manager=exchange_manager,
                        ),
                        block_factory=exchange_manager.trading_modes[0]
                        .producers[0]
                        .block_factory,
                    )
                    break
            if to_closes is None:
                raise OtherExchangeNotInitializedError
            from_closes, to_closes = cut_data_to_same_len((from_closes, to_closes))
            if self.plot_precent:
                delta_data = (to_closes - from_closes) / (to_closes / 100)
            else:
                delta_data = to_closes - from_closes
            await self.store_indicator_data(
                title=(
                    f" candle {self.candle_source} delta from "
                    f"{self.block_factory.ctx.exchange_name} to {self.to_exchange}"
                ),
                data=delta_data,
            )

            # TODO
            # data_source["f"]["data"] = from_closes
            # data_source["t"]["data"] = to_closes
        except (
            AttributeError,
            TypeError,
            OtherExchangeNotInitializedError,
            IndexError,
        ) as error:
            self.block_factory.ctx.logger.info(
                "Plot exchange delta is not possible. Other exchange is not initialized - "
                f"this is normal if you just started octobot. Error: {error}"
            )


class OtherExchangeNotInitializedError(Exception):
    """
    Raised when the candle data for the other
    exchange is not initialized or available yet
    """
