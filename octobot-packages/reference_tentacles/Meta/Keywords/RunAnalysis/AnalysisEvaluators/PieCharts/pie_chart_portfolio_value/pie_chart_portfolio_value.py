from octobot_commons.constants import CONFIG_EXCHANGE_FUTURE
from octobot_commons.symbols.symbol_util import merge_currencies, merge_symbol
import tentacles.Meta.Keywords.RunAnalysis.AnalysisKeywords.common_user_inputs as common_user_inputs
import tentacles.Meta.Keywords.RunAnalysis.BaseDataProvider.default_base_data_provider.base_data_provider as base_data_provider
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.abstract_analysis_evaluator as abstract_analysis_evaluator


class PieChartPortfolio(abstract_analysis_evaluator.AnalysisEvaluator):
    PIE_CHART_PORFOLIO_NAME = "_portfolio_value"
    PIE_CHART_PORFOLIO_TILE = "Portfolio Value"

    @classmethod
    def init_user_inputs(
        cls, analysis_mode_plugin, inputs: dict, parent_input_name: str
    ) -> None:
        common_user_inputs.init_data_source_settings(
            data_source_input_name=cls.PIE_CHART_PORFOLIO_NAME,
            data_source_input_title=cls.PIE_CHART_PORFOLIO_TILE,
            analysis_mode_plugin=analysis_mode_plugin,
            inputs=inputs,
            parent_input_name=parent_input_name,
            has_chart_location=False,
            default_data_source_enabled=True,
        )

    async def evaluate(
        self,
        run_data: base_data_provider.RunAnalysisBaseDataGenerator,
        analysis_type: str,
    ):
        plotted_element = common_user_inputs.get_plotted_element_based_on_settings(
            run_data,
            analysis_type=analysis_type,
            data_source_input_name=self.PIE_CHART_PORFOLIO_NAME,
            default_data_source_enabled=True,
            default_chart_location="pie-chart",
        )
        if plotted_element is not None:
            for portfolio_name, time_key in (
                ("starting_portfolio", "starting_time"),
                ("ending_portfolio", "last_update_time"),
            ):
                start_end_portfolio_values = (
                    await run_data.get_start_end_portfolio_values()
                )
                values = []
                labels = []
                if len(start_end_portfolio_values) and start_end_portfolio_values[
                    0
                ].get(portfolio_name):
                    for currency, balance in start_end_portfolio_values[0][
                        portfolio_name
                    ].items():
                        if currency != run_data.ref_market:
                            merged_symbol = merge_currencies(
                                currency,
                                market=run_data.ref_market,
                                settlement_asset=run_data.ref_market
                                if run_data.trading_type == CONFIG_EXCHANGE_FUTURE
                                else None,
                            )
                            conversion_candles = await run_data.get_candles(
                                symbol=merged_symbol, time_frame=run_data.ctx.time_frame
                            )
                            portfolio_time = (
                                start_end_portfolio_values[0][time_key] * 1000
                            )
                            closest_close_price = None
                            for candle_index, candle_time in enumerate(
                                conversion_candles[0]
                            ):
                                if portfolio_time > candle_time:
                                    closest_close_price = conversion_candles[4][
                                        candle_index
                                    ]
                            total_balance_in_ref = (
                                balance["total"] * closest_close_price
                            )
                        else:
                            total_balance_in_ref = balance["total"]
                        values.append(total_balance_in_ref)
                        labels.append(currency)

                    plotted_element.pie_chart(
                        values,
                        labels,
                        title="Starting Portfolio"
                        if portfolio_name == "starting_portfolio"
                        else "Current Portfolio",
                        text="Starting"
                        if portfolio_name == "starting_portfolio"
                        else "Current",
                        hole_size=0.4,
                    )
