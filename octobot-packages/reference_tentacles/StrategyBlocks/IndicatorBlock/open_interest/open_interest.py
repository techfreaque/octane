import octobot_commons.enums as commons_enums

import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_indicator_block as abstract_indicator_block


class OpenInterestIndicator(abstract_indicator_block.IndicatorBlock):
    NAME = "open_interest"
    TITLE = "Open Interest"
    TITLE_SHORT = "Open Interest"
    DESCRIPTION = (
        "Note that Open Interest is only available for futures exchanges and "
        "currently only supported in live trading "
        "and doesnt work in backtesting"
    )

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
        if (
            self.block_factory.ctx.exchange_manager.is_future
            and not self.block_factory.ctx.exchange_manager.is_backtesting
        ):
            raw_data = await self.block_factory.ctx.exchange_manager.exchange.get_open_interest_history(
                symbol=self.block_factory.ctx.symbol,
                time_frame=self.block_factory.ctx.time_frame,
            )
            open_interest_history = [candle["openInterestValue"] for candle in raw_data]
            await self.store_indicator_data(
                title=f"{self.TITLE_SHORT}",
                data=open_interest_history,
            )
        elif not self.block_factory.ctx.exchange_manager.is_future:
            self.block_factory.logger.error(
                "Open interest is only supported for futures exchanges"
            )
        elif self.block_factory.ctx.exchange_manager.is_backtesting:
            raise RuntimeError(
                "Open interest is currently only supported in live trading"
            )
