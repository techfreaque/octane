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

from finta import TA as fta
import pandas as pd
import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class IchimokuIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "ichimoku"
    TITLE = "Ichimoku"
    TITLE_SHORT = "Ichimoku"
    DESCRIPTION = "Ichimoku"

    conversion_line_length: int
    base_line_length: int
    leading_span_b_length: int
    displacement: int

    def init_block_settings(self) -> None:
        self.conversion_line_length = self.user_input(
            "conversion line length", "int", 9
        )
        self.base_line_length = self.user_input("base line length", "int", 26)
        self.leading_span_b_length = self.user_input("leading span b length", "int", 52)
        self.displacement = self.user_input("displacement", "int", 26)
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Conversion Line",
            plot_switch_text=f"Plot {self.TITLE_SHORT} Conversion Line",
            plot_color_switch_title=f"{self.TITLE_SHORT} Conversion Line plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} Conversion Line chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Base Line",
            plot_switch_text=f"Plot {self.TITLE_SHORT} Base Line",
            plot_color_switch_title=f"{self.TITLE_SHORT} Base Line plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} Base Line chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Leading Span B",
            plot_switch_text=f"Plot {self.TITLE_SHORT} Leading Span B",
            plot_color_switch_title=f"{self.TITLE_SHORT} Leading Span B plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} Leading Span B chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )
        self.register_indicator_data_output(
            title=f"{self.TITLE_SHORT} Leading Span A",
            plot_switch_text=f"Plot {self.TITLE_SHORT} Leading Span A",
            plot_color_switch_title=f"{self.TITLE_SHORT} Leading Span A plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} Leading Span A chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
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
            }
        )
        ichimoku_df = fta.ICHIMOKU(
            data_frame,
            tenkan_period=self.conversion_line_length,
            kijun_period=self.base_line_length,
            senkou_period=self.leading_span_b_length,
            chikou_period=self.displacement,
        )
        ichimoku_df = ichimoku_df.drop(["CHIKOU"], axis=1)
        ichimoku_df = ichimoku_df.dropna()
        await self.store_indicator_data(
            title="Ichimoku Conversion Line",
            data=list(ichimoku_df["TENKAN"]),
        )
        await self.store_indicator_data(
            title="Ichimoku Base Line",
            data=list(ichimoku_df["KIJUN"]),
        )
        await self.store_indicator_data(
            title="Ichimoku Leading Span B",
            data=list(ichimoku_df["SENKOU"]),
        )
        await self.store_indicator_data(
            title="Ichimoku Leading Span A",
            data=list(ichimoku_df["senkou_span_a"]),
        )
