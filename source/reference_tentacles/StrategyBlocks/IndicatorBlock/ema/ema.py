import tulipy
import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class EmaIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "ema"
    TITLE = "Exponential Moving Average"
    TITLE_SHORT = "EMA"
    DESCRIPTION = "EMA is arguably the most known indicator"

    length: int
    candle_source: str

    def init_block_settings(self) -> None:
        self.length = self.user_input(
            name=f"{self.TITLE_SHORT} length",
            input_type=commons_enums.UserInputTypes.INT,
            def_val=50,
            min_val=0,
            grid_columns=12,
        )
        self.candle_source = self.user_select_candle_source_name(
            name=f"Select {self.TITLE_SHORT} Candle Source", enable_volume=True
        )
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=self.TITLE_SHORT,
            plot_switch_text=f"Plot {self.TITLE_SHORT}",
            plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} chart location",
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value
            if self.candle_source == matrix_enums.PriceDataSources.VOLUME.value
            else commons_enums.PlotCharts.MAIN_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        data = tulipy.ema(
            await self.get_candles(self.candle_source),
            self.length,
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT} {self.length}",
            data=data,
        )
