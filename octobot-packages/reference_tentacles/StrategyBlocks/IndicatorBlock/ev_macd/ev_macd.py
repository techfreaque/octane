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

import pandas as pd
from functools import wraps

import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class EvMacdIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "ev_macd"
    TITLE = "EV MACD"
    TITLE_SHORT = "EV MACD"
    DESCRIPTION = "EV MACD"

    fast_length: int
    slow_length: int
    signal_smoothing: int

    def init_block_settings(self) -> None:
        self.fast_length = self.user_input("EV MACD fast length", "int", 12)
        self.slow_length = self.user_input("EV MACD slow length", "int", 26)
        self.signal_smoothing = self.user_input("EV MACD signal smoothing", "int", 9)
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=self.TITLE_SHORT,
            plot_switch_text=f"Plot {self.TITLE_SHORT}",
            plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} chart location",
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
        )
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Signal",
            plot_switch_text=f"Plot {self.TITLE_SHORT} Signal",
            plot_color_switch_title=f"{self.TITLE_SHORT} Signal plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} Signal chart location",
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        data_frame = pd.DataFrame(
            {
                "open": await self.get_candles(
                    matrix_enums.PriceDataSources.OPEN.value
                ),
                "high": await self.get_candles(
                    matrix_enums.PriceDataSources.HIGH.value
                ),
                "low": await self.get_candles(matrix_enums.PriceDataSources.LOW.value),
                "close": await self.get_candles(
                    matrix_enums.PriceDataSources.CLOSE.value
                ),
                "volume": await self.get_candles(
                    matrix_enums.PriceDataSources.VOLUME.value
                ),
            }
        )
        macd_df = CustomFta.EV_MACD(
            data_frame,
            period_fast=self.fast_length,
            period_slow=self.slow_length,
            signal=self.signal_smoothing,
        )
        cut_first_n_candles = self.slow_length * 2 + 80
        macd = macd_df.iloc[cut_first_n_candles:, 1]
        macd_signal = macd_df.iloc[cut_first_n_candles:, 0]
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} {self.signal_smoothing}-{self.fast_length}-{self.slow_length}",
            data=list(macd),
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} Signal {self.signal_smoothing}-{self.fast_length}-{self.slow_length}",
            data=list(macd_signal),
        )

# code copied from finta as its not compatible with latest python version
def inputvalidator(input_="ohlc"):
    def dfcheck(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            args = list(args)
            i = 0 if isinstance(args[0], pd.DataFrame) else 1

            args[i] = args[i].rename(columns={c: c.lower() for c in args[i].columns})

            inputs = {
                "o": "open",
                "h": "high",
                "l": "low",
                "c": kwargs.get("column", "close").lower(),
                "v": "volume",
            }

            if inputs["c"] != "close":
                kwargs["column"] = inputs["c"]

            for l in input_:
                if inputs[l] not in args[i].columns:
                    raise LookupError(
                        'Must have a dataframe column named "{0}"'.format(inputs[l])
                    )

            return func(*args, **kwargs)

        return wrap

    return dfcheck


class CustomFta():
    @classmethod
    @inputvalidator(input_="ohlcv")
    def EV_MACD(
        cls,
        ohlcv,
        period_fast: int = 20,
        period_slow: int = 40,
        signal: int = 9,
        adjust: bool = True,
    ):
        """
        Elastic Volume Weighted MACD is a variation of standard MACD,
        calculated using two EVWMA's.

        :period_slow: Specifies the number of Periods used for the slow EVWMA calculation
        :period_fast: Specifies the number of Periods used for the fast EVWMA calculation
        :signal: Specifies the number of Periods used for the signal calculation
        """

        evwma_slow = cls.EVWMA(ohlcv, period_slow)

        evwma_fast = cls.EVWMA(ohlcv, period_fast)

        MACD = pd.Series(evwma_fast - evwma_slow, name="MACD")
        MACD_signal = pd.Series(
            MACD.ewm(ignore_na=False, span=signal, adjust=adjust).mean(), name="SIGNAL"
        )

        return pd.concat([MACD, MACD_signal], axis=1)

    @classmethod
    @inputvalidator(input_="ohlcv")
    def EVWMA(cls, ohlcv, period: int = 20):
        """
        The eVWMA can be looked at as an approximation to the
        average price paid per share in the last n periods.

        :period: Specifies the number of Periods used for eVWMA calculation
        """

        vol_sum = (
            ohlcv["volume"].rolling(window=period).sum()
        )  # floating shares in last N periods

        x = (vol_sum - ohlcv["volume"]) / vol_sum
        y = (ohlcv["volume"] * ohlcv["close"]) / vol_sum

        evwma = [0]

        #  evwma = (evma[-1] * (vol_sum - volume)/vol_sum) + (volume * price / vol_sum)
        for x, y in zip(x.fillna(0).items(), y.items()):
            if x[1] == 0 or y[1] == 0:
                evwma.append(0)
            else:
                evwma.append(evwma[-1] * x[1] + y[1])

        return pd.Series(
            evwma[1:],
            index=ohlcv.index,
            name="{0} period EVWMA.".format(period),
        )
