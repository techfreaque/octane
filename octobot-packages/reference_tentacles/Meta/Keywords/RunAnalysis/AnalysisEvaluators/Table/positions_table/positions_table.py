import tentacles.Meta.Keywords.RunAnalysis.AnalysisKeywords.common_user_inputs as common_user_inputs
import tentacles.Meta.Keywords.RunAnalysis.AnalysisKeywords.table_keywords as table_keywords
import tentacles.Meta.Keywords.RunAnalysis.BaseDataProvider.default_base_data_provider.base_data_provider as base_data_provider
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.abstract_analysis_evaluator as abstract_analysis_evaluator


class PositionsTable(abstract_analysis_evaluator.AnalysisEvaluator):
    POSITIONS_TABLE_NAME = "_positions_table"
    POSITIONS_TABLE_TITLE = "Positions Table"

    @classmethod
    def init_user_inputs(
        cls, analysis_mode_plugin, inputs: dict, parent_input_name: str
    ) -> None:
        common_user_inputs.init_data_source_settings(
            data_source_input_name=cls.POSITIONS_TABLE_NAME,
            data_source_input_title=cls.POSITIONS_TABLE_TITLE,
            analysis_mode_plugin=analysis_mode_plugin,
            inputs=inputs,
            parent_input_name=parent_input_name,
            default_data_source_enabled=True,
            has_chart_location=False,
            # can_select_symbols=True,
        )

    async def evaluate(
        self,
        run_data: base_data_provider.RunAnalysisBaseDataGenerator,
        analysis_type: str,
    ):
        if common_user_inputs.get_is_data_source_enabled(
            run_data,
            data_source_input_name=self.POSITIONS_TABLE_NAME,
            def_val=True,
            analysis_type=analysis_type,
        ):
            # symbols_settings = common_user_inputs.get_enabled_symbols(
            #     run_data,
            #     data_source_input_name=self.POSITIONS_TABLE_NAME,
            #     analysis_type=analysis_type,
            # )
            # symbols = (
            #     None
            #     if symbols_settings == analysis_enums.SymbolsOptions.ALL_SYMBOLS
            #     else [run_data.ctx.symbol]
            # )
            transactions = await run_data.get_transactions()
            if bool(transactions):
                # TODO use constants
                key_to_label = {
                    "x": "Exit time",
                    "first_entry_time": "Entry time",
                    "average_entry_price": "Average entry price",
                    "average_exit_price": "Average exit price",
                    "cumulated_closed_quantity": "Cumulated closed quantity",
                    "realized_pnl": "Realized PNL",
                    "side": "Side",
                    "trigger_source": "Closed by",
                }
                additional_column_types = {
                    "Time": "datetime",
                    "Entry time": "datetime",
                    "Exit time": "datetime",
                    "Average entry price": "float",
                    "Average exit price": "float",
                    "Cumulated closed quantity": "float",
                    "Realized PNL": "float",
                    "Side": "float",
                    "trigger_source": "text",
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
                    pass
                    # datum[
                    #     "total"
                    # ] = f"{datum['cost']} {datum['origin_value']['market']}"
                    # datum[
                    #     "volume"
                    # ] = f"{datum['volume']} {datum['origin_value']['quantity_currency']}"
                    # datum["fees"] = f'{datum["fees_amount"]} {datum["fees_currency"]}'

                table_keywords.plot_table_data(
                    data=transactions,
                    data_name=f"Position History for {run_data.exchange_name}",
                    run_data=run_data,
                    additional_key_to_label=key_to_label,
                    additional_columns=additional_columns,
                    additional_column_types=additional_column_types,
                    datum_columns_callback=datum_columns_callback,
                    icon="ShoppingCartOutlined",
                )


# async def plot_positions_table(
#     run_data: base_data_provider.RunAnalysisBaseDataGenerator, plotted_element
# ):
#     import tentacles.Meta.Keywords.scripting_library.run_analysis.run_analysis_plots as run_analysis_plots

#     realized_pnl_history = await run_data.load_spot_or_futures_base_data(
#         transaction_types=(
#             trading_enums.TransactionType.REALIZED_PNL.value,
#             trading_enums.TransactionType.CLOSE_REALIZED_PNL.value,
#         )
#     )
#     key_to_label = {
#         "x": "Exit time",
#         "first_entry_time": "Entry time",
#         "average_entry_price": "Average entry price",
#         "average_exit_price": "Average exit price",
#         "cumulated_closed_quantity": "Cumulated closed quantity",
#         "realized_pnl": "Realized PNL",
#         "side": "Side",
#         "trigger_source": "Closed by",
#     }

#     run_analysis_plots.plot_table_data(
#         realized_pnl_history, plotted_element, "Positions", key_to_label, [], None
#     )
