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
    interval_type: typing.Optional[str]
    interval_value: typing.Optional[int]

    def init_block_settings(self) -> None:
        self.interval_type = self.user_input(
            "Interval type",
            "options",
            "hours",
            options=["hours", "days", "weeks", "months"],
        )
        self.interval_value = int(self.user_input(
            "Interval value",
            "number",
            "1",
        ))

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
                get_buy_signal_from_time(timestamp, self.interval_type, self.interval_value)
            )
        await self.store_evaluator_signals(
            title=f"DCA buy signal ({self.interval_value} {self.interval_type})",
            signals=signals,
            signal_values=values,
            chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )


def get_buy_signal_from_time(current_time, interval_type, interval_value):
    current_datetime = datetime.datetime.fromtimestamp(current_time)
    if interval_type == "hours":
        next_signal_time = current_datetime + datetime.timedelta(hours=interval_value)
    elif interval_type == "days":
        next_signal_time = current_datetime + datetime.timedelta(days=interval_value)
    elif interval_type == "weeks":
        next_signal_time = current_datetime + datetime.timedelta(weeks=interval_value)
    elif interval_type == "months":
        next_signal_time = current_datetime + datetime.timedelta(days=30 * interval_value)  # Approximation
    else:
        return False

    return current_datetime >= next_signal_time