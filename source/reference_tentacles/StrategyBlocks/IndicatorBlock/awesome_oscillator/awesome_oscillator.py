import tulipy
import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class AwesomeOscillator(abstract_indicator_block.IndicatorBlock):
    NAME = "awesome_oscillator"
    TITLE = "Awesome Oscillator"
    TITLE_SHORT = "Awesome Oscillator"
    DESCRIPTION = "Awesome Oscillator"

    def init_block_settings(self) -> None:
        self.user_select_data_source_time_frame()
        self.register_indicator_data_output(
            title=self.TITLE_SHORT,
            plot_switch_text=f"Plot {self.TITLE_SHORT}",
            plot_color_switch_title=f"{self.TITLE_SHORT} plot color",
            default_plot_color=block_factory_enums.Colors.ORANGE,
            chart_location_title=f"{self.TITLE_SHORT} chart location",
            default_chart_location=commons_enums.PlotCharts.SUB_CHART.value,
        )

    async def execute_block(
        self,
    ) -> None:
        data = tulipy.ao(
            await self.get_candles(matrix_enums.PriceDataSources.HIGH.value),
            await self.get_candles(matrix_enums.PriceDataSources.LOW.value),
        )
        await self.store_indicator_data(
            title=f"{self.TITLE_SHORT}",
            data=data,
        )
