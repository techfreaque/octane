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

import typing

import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block
import tentacles.Meta.Keywords.indicator_keywords.vwap_lib.vwap_library as vwap_library


class VwapIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "vwap"
    TITLE = "Volume Weighted Average Price"
    TITLE_SHORT = "VWAP"
    DESCRIPTION = "Volume Weighted Average Price"

    selected_vwap_timeframe: str
    candle_source: str
    custom_vwap_timeframe: typing.Optional[str]
    enable_upper_bands: bool
    enable_lower_bands: bool
    standard_diviation_multiplier: typing.Optional[float]

    def init_block_settings(self) -> None:
        custom_time_range_name = "custom time range"
        self.selected_vwap_timeframe = self.user_input(
            "VWAP time Window",
            commons_enums.UserInputTypes.OPTIONS.value,
            "24h",
            options=[custom_time_range_name, "24h", "session", "week", "month"],
        )
        self.user_select_data_source_time_frame()
        if self.custom_time_frame:
            available_timeframes: list = [self.custom_time_frame]
        else:
            available_timeframes: list = self.get_available_time_frames()
        minutes_in_time_frame = max(
            (
                commons_enums.TimeFramesMinutes[commons_enums.TimeFrames(time_frame)]
                for time_frame in available_timeframes
            )
        )
        if custom_time_range_name == self.selected_vwap_timeframe:
            self.custom_vwap_timeframe = self.user_input(
                "Custom VWAP time Window in minutes",
                commons_enums.UserInputTypes.INT.value,
                60,
                min_val=minutes_in_time_frame * 2,
            )
        else:
            self.custom_vwap_timeframe = None
        self.candle_source = self.user_select_candle_source_name(
            "Select VWAP Candle Source", matrix_enums.PriceDataSources.HLC3.value
        )
        self.register_indicator_data_output(
            title=self.TITLE_SHORT,
            plot_switch_text=f"Plot {self.TITLE_SHORT}",
            plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
            default_plot_color=block_factory_enums.Colors.WHITE,
            chart_location_title=f"{self.TITLE_SHORT} chart location",
            default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
        )
        self.user_input(
            "Enable upper VWAP bands",
            commons_enums.UserInputTypes.BOOLEAN.value,
            False,
        )
        self.user_input(
            "Enable lower VWAP bands",
            commons_enums.UserInputTypes.BOOLEAN.value,
            False,
        )
        self.enable_upper_bands = self.user_input(
            "Enable upper VWAP bands",
            commons_enums.UserInputTypes.BOOLEAN.value,
            False,
        )
        self.enable_lower_bands = self.user_input(
            "Enable lower VWAP bands",
            commons_enums.UserInputTypes.BOOLEAN.value,
            False,
        )
        self.standard_diviation_multiplier = None
        if self.enable_upper_bands or self.enable_lower_bands:
            self.standard_diviation_multiplier = self.user_input(
                "standard_diviation_multiplier",
                commons_enums.UserInputTypes.FLOAT.value,
                0.88,
                min_val=0.1,
                title="VWAP bands standard diviation multiplier",
            )
        if self.enable_lower_bands:
            self.register_indicator_data_output(
                title="Lower Band 1",
                plot_switch_text=f"Plot {self.TITLE_SHORT} lower band 1",
                plot_color_switch_title=f"{self.TITLE_SHORT} lower band 1 plot color",
                default_plot_color=block_factory_enums.Colors.ORANGE,
                chart_location_title=f"{self.TITLE_SHORT} lower band 1 chart location",
                default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
            )
            self.register_indicator_data_output(
                title="Lower Band 2",
                plot_switch_text=f"Plot {self.TITLE_SHORT} lower band 2",
                plot_color_switch_title=f"{self.TITLE_SHORT} lower band 2 plot color",
                default_plot_color=block_factory_enums.Colors.RED,
                chart_location_title=f"{self.TITLE_SHORT} lower band 2 chart location",
                default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
            )
        if self.enable_upper_bands:
            self.register_indicator_data_output(
                title="Upper Band 1",
                plot_switch_text=f"Plot {self.TITLE_SHORT} upper band 1",
                plot_color_switch_title=f"{self.TITLE_SHORT} upper band 1 plot color",
                default_plot_color=block_factory_enums.Colors.GREEN,
                chart_location_title=f"{self.TITLE_SHORT} upper band 1 chart location",
                default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
            )
            self.register_indicator_data_output(
                title="Upper Band 2",
                plot_switch_text=f"Plot {self.TITLE_SHORT} upper band 2",
                plot_color_switch_title=f"{self.TITLE_SHORT} upper band 2 plot color",
                default_plot_color=block_factory_enums.Colors.CYAN,
                chart_location_title=f"{self.TITLE_SHORT} upper band 2 chart location",
                default_chart_location=commons_enums.PlotCharts.MAIN_CHART.value,
            )

    async def execute_block(
        self,
    ) -> None:
        vwap_data, standard_diviations = vwap_library.calculate_historical_VWAP(
            await self.get_candles(self.candle_source),
            await self.get_candles(matrix_enums.PriceDataSources.VOLUME.value),
            time_data=await self.get_candles(matrix_enums.PriceDataSources.TIME.value),
            window=self.selected_vwap_timeframe,
            custom_window_in_minutes=self.custom_vwap_timeframe,
            time_frame=self.custom_time_frame or self.block_factory.ctx.time_frame,
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} {self.selected_vwap_timeframe}",
            data=vwap_data,
        )
        if self.enable_lower_bands:
            band_1 = (
                vwap_data - standard_diviations * self.standard_diviation_multiplier
            )
            band_2 = (
                vwap_data - 2 * standard_diviations * self.standard_diviation_multiplier
            )
            await self.store_indicator_data(
                title=f"{self.TITLE_SHORT} lower band 1 {self.selected_vwap_timeframe}",
                data=band_1,
            )
            await self.store_indicator_data(
                title=f"{self.TITLE_SHORT} lower band 2 {self.selected_vwap_timeframe}",
                data=band_2,
            )
        if self.enable_upper_bands:
            band_1 = (
                vwap_data + standard_diviations * self.standard_diviation_multiplier
            )
            band_2 = (
                vwap_data + 2 * standard_diviations * self.standard_diviation_multiplier
            )
            await self.store_indicator_data(
                title=f"{self.TITLE_SHORT} upper band 1 {self.selected_vwap_timeframe}",
                data=band_1,
            )
            await self.store_indicator_data(
                title=f"{self.TITLE_SHORT} upper band 2 {self.selected_vwap_timeframe}",
                data=band_2,
            )
