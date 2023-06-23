import tentacles.Meta.Keywords.RunAnalysis.AnalysisKeywords.common_user_inputs as common_user_inputs
import tentacles.Meta.Keywords.RunAnalysis.AnalysisKeywords.analysis_enums as analysis_enums
import tentacles.Meta.Keywords.RunAnalysis.AnalysisKeywords.table_keywords as table_keywords
import tentacles.Meta.Keywords.RunAnalysis.BaseDataProvider.default_base_data_provider.base_data_provider as base_data_provider
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.abstract_analysis_evaluator as abstract_analysis_evaluator


class TradesTable(abstract_analysis_evaluator.AnalysisEvaluator):
    TRADES_TABLE_NAME = "_trades_table"
    TRADES_TABLE_TITLE = "Trades Table"

    @classmethod
    def init_user_inputs(
        cls, analysis_mode_plugin, inputs: dict, parent_input_name: str
    ) -> None:
        common_user_inputs.init_data_source_settings(
            data_source_input_name=cls.TRADES_TABLE_NAME,
            data_source_input_title=cls.TRADES_TABLE_TITLE,
            analysis_mode_plugin=analysis_mode_plugin,
            inputs=inputs,
            parent_input_name=parent_input_name,
            default_data_source_enabled=True,
            has_chart_location=False,
            can_select_symbols=True,
            default_symbols=analysis_enums.SymbolsOptions.ALL_SYMBOLS,
        )

    async def evaluate(
        self,
        run_data: base_data_provider.RunAnalysisBaseDataGenerator,
        analysis_type: str,
    ):
        if common_user_inputs.get_is_data_source_enabled(
            run_data,
            data_source_input_name=self.TRADES_TABLE_NAME,
            def_val=True,
            analysis_type=analysis_type,
        ):
            symbols_settings = common_user_inputs.get_enabled_symbols(
                run_data,
                data_source_input_name=self.TRADES_TABLE_NAME,
                analysis_type=analysis_type,
                default_symbols=analysis_enums.SymbolsOptions.ALL_SYMBOLS,
            )
            symbols = (
                None
                if symbols_settings == analysis_enums.SymbolsOptions.ALL_SYMBOLS
                else [run_data.ctx.symbol]
            )
            trades = await run_data.get_trades(symbols)
            if bool(trades):
                # TODO use constants
                key_to_label = {
                    "id": "ID",
                    "y": "Price",
                    "type": "Type",
                    "side": "Side",
                }
                additional_column_types = {
                    "Time": "datetime",
                    "Entry time": "datetime",
                    "Exit time": "datetime",
                    "ID": "text",
                    "Symbol": "text",
                    "Type": "text",
                    "Side": "text",
                    "Price": "float",
                    "Fees": "text",
                    "Total": "text",
                    "Volume": "text",
                }
                additional_columns = [
                    {
                        "field": "total",
                        "text": "Total",
                        "render": None,
                        "sortable": True,
                    },
                    {"field": "fees", "text": "Fees", "render": None, "sortable": True},
                ]

                def datum_columns_callback(datum):
                    datum[
                        "total"
                    ] = f"{datum['cost']} {datum['origin_value']['market']}"
                    datum[
                        "volume"
                    ] = f"{datum['volume']} {datum['origin_value']['quantity_currency']}"
                    datum["fees"] = f'{datum["fees_amount"]} {datum["fees_currency"]}'

                table_keywords.plot_table_data(
                    data=trades,
                    data_name=f"Trades for {'all symbols' if symbols_settings == analysis_enums.SymbolsOptions.ALL_SYMBOLS else run_data.ctx.symbol}",
                    run_data=run_data,
                    additional_key_to_label=key_to_label,
                    additional_columns=additional_columns,
                    additional_column_types=additional_column_types,
                    datum_columns_callback=datum_columns_callback,
                    icon="ShoppingCartOutlined",
                )
