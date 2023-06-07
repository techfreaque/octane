import tentacles.Meta.Keywords.RunAnalysis.AnalysisKeywords.analysis_enums as analysis_enums
import tentacles.Meta.Keywords.RunAnalysis.AnalysisKeywords.common_user_inputs as common_user_inputs
import tentacles.Meta.Keywords.RunAnalysis.AnalysisKeywords.plot_keywords as plot_keywords
import tentacles.Meta.Keywords.RunAnalysis.BaseDataProvider.default_base_data_provider.base_data_provider as base_data_provider
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.abstract_analysis_evaluator as abstract_analysis_evaluator


class PlotTrades(abstract_analysis_evaluator.AnalysisEvaluator):
    PRIORITY: float = 900

    PLOT_TRADES_NAME = "_trades"
    PLOT_TRADES_TILE = "Trades"

    @classmethod
    def init_user_inputs(
        cls, analysis_mode_plugin, inputs: dict, parent_input_name: str
    ) -> None:
        common_user_inputs.init_data_source_settings(
            data_source_input_name=cls.PLOT_TRADES_NAME,
            data_source_input_title=cls.PLOT_TRADES_TILE,
            analysis_mode_plugin=analysis_mode_plugin,
            inputs=inputs,
            parent_input_name=parent_input_name,
            default_chart_location="main-chart",
            default_data_source_enabled=True,
            can_select_symbols=True,
            default_symbols=analysis_enums.SymbolsOptions.CURRENT_SYMBOL,
        )

    async def evaluate(
        self,
        run_data: base_data_provider.RunAnalysisBaseDataGenerator,
        analysis_type: str,
    ):
        plotted_element = common_user_inputs.get_plotted_element_based_on_settings(
            run_data,
            analysis_type=analysis_type,
            data_source_input_name=self.PLOT_TRADES_NAME,
            default_chart_location="main-chart",
            default_data_source_enabled=True,
        )
        if plotted_element is not None:
            symbols_settings = common_user_inputs.get_enabled_symbols(
                run_data,
                data_source_input_name=self.PLOT_TRADES_NAME,
                analysis_type=analysis_type,
                default_symbols=analysis_enums.SymbolsOptions.CURRENT_SYMBOL,
            )
            symbols = (
                None
                if symbols_settings == analysis_enums.SymbolsOptions.ALL_SYMBOLS
                else [run_data.ctx.symbol]
            )
            trades = await run_data.get_trades(symbols)
            plot_keywords.plot_from_standard_data(
                trades,
                plotted_element,
                title=f"Trades for {'all symbols' if symbols_settings == analysis_enums.SymbolsOptions.ALL_SYMBOLS else run_data.ctx.symbol}",
            )
