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
import datetime
from dateutil.relativedelta import relativedelta
import typing
import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_evaluator_block as abstract_evaluator_block


class TimeSignalsEvaluator(abstract_evaluator_block.EvaluatorBlock):
    NAME = "time_signals"
    TITLE = "Time based signals"
    TITLE_SHORT = "Time based signals"
    DESCRIPTION = "Get signals based on time"
    day: typing.Optional[str]
    hour: typing.Optional[str]
    minute: typing.Optional[str]
    month: typing.Optional[str]

    def init_block_settings(self) -> None:
        self.day = self.user_input(
            "signals on every n days",
            "options",
            "every",
            options=[
                "every",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
                "27",
                "28",
                "29",
                "30",
                "31",
            ],
        )
        if self.day == "every":
            self.day = 1
        else:
            self.day = int(self.day)
        self.hour = self.user_input(
            "signals on hour",
            "options",
            "0",
            options=[
                "every",
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
            ],
        )
        if self.hour == "every":
            self.hour = None

        self.minute = self.user_input(
            "signals on minute",
            "options",
            "0",
            options=[
                "every",
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
                "27",
                "28",
                "29",
                "30",
                "31",
                "32",
                "33",
                "34",
                "35",
                "36",
                "37",
                "38",
                "39",
                "40",
                "41",
                "42",
                "43",
                "44",
                "45",
                "46",
                "47",
                "48",
                "49",
                "50",
                "51",
                "52",
                "53",
                "54",
                "55",
                "56",
                "57",
                "58",
                "59",
            ],
        )
        if self.minute == "every":
            self.minute = None

        self.register_evaluator_data_output(
            title="DCA Signals",
            plot_switch_text="Plot DCA signals",
            plot_color_switch_title="Signals plot color",
            default_plot_color=block_factory_enums.Colors.GREEN,
        )

    async def execute_block(
        self,
    ) -> None:
        values = await self.get_candles(matrix_enums.PriceDataSources.LOW.value)
        times = await self.get_candles(matrix_enums.PriceDataSources.TIME.value)
        signals = []
        for timestamp in times:
            signals.append(
                get_buy_signal_from_time(timestamp, self.day, self.hour, self.minute)
            )
        await self.store_evaluator_signals(
            title=f"DCA buy signal (d:{self.day or 'every'} h:{self.hour or 'every'} m:{self.minute or 'every'}",
            signals=signals,
            signal_values=values,
            chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )


def get_buy_signal_from_time(
    current_time: float,
    every_n_days: int | None = None,
    hour: str | None = None,
    minute: str | None = None,
):
    current_datetime = datetime.datetime.fromtimestamp(current_time)
    time_to_buy = current_datetime

    if every_n_days:
        start_date = datetime.datetime(1970, 1, 1)
        delta_days = (current_datetime - start_date).days
        if delta_days % every_n_days != 0:
            return False
    if hour:
        time_to_buy = time_to_buy.replace(
            hour=int(hour),
        )
    if minute:
        time_to_buy = time_to_buy.replace(
            minute=int(minute),
        )

    return current_datetime == time_to_buy
