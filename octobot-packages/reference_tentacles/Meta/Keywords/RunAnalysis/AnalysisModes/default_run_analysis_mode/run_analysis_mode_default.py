import datetime as datetime
import json as json
import typing
import octobot_commons.logging as logging
import octobot_commons.enums as commons_enums
import octobot_trading.api as trading_api

import tentacles.Meta.Keywords.RunAnalysis.AnalysisKeywords.analysis_enums as analysis_enums
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.abstract_analysis_evaluator as abstract_analysis_evaluator
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.abstract_run_analysis_mode as abstract_run_analysis_mode
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.init_base_data as init_base_data
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.custom_context as custom_context
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.run_analysis_factory as run_analysis_factory
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    UserInputOtherSchemaValuesTypes,
)


class DefaultRunAnalysisMode(abstract_run_analysis_mode.AbstractRunAnalysisMode):
    logger: logging.BotLogger = logging.get_logger("DefaultRunAnalysisMode")
    available_run_analyzer_plot_modules: dict = None
    available_run_analyzer_table_modules: dict = None
    available_run_analyzer_pie_chart_modules: dict = None
    available_run_analyzer_dictionaries_modules: dict = None
    available_run_analyzer_module_names: list = None
    selected_run_analyzer_module_names: list = None

    initialized_group_input_name: list = []

    ENABLED_RUN_ANALYZERS_SETTING_NAME: str = "enabled_run_analyzers"
    ENABLE_RUN_ANALYSIS_MODE_SETTING_NAME: str = "enable_run_analysis_mode"

    @staticmethod
    def init_user_inputs(cls, analysis_mode_plugin, inputs: dict) -> None:
        cls.reload_available_run_analyzers()
        analysis_mode_plugin.CLASS_UI.user_input(
            analysis_enums.AnalysisModeSettingsTypes.LIVE_RUN_ANALYSIS_MODE_SETTINGS_NAME,
            commons_enums.UserInputTypes.OBJECT,
            None,
            inputs,
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12
            },
            other_schema_values={
                UserInputOtherSchemaValuesTypes.DISPLAY_AS_TAB.value: True
            },
            title="Live Display Settings",
        )
        analysis_mode_plugin.CLASS_UI.user_input(
            analysis_enums.AnalysisModeSettingsTypes.BACKTESTING_RUN_ANALYSIS_MODE_SETTINGS_NAME,
            commons_enums.UserInputTypes.OBJECT,
            None,
            inputs,
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
                commons_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: True,
            },
            other_schema_values={
                UserInputOtherSchemaValuesTypes.DISPLAY_AS_TAB.value: True
            },
            title="Backtesting Display Settings",
        )
        cls._init_run_analyzers_user_inputs(
            analysis_mode_plugin,
            inputs,
            parent_input_name=analysis_enums.AnalysisModeSettingsTypes.LIVE_RUN_ANALYSIS_MODE_SETTINGS_NAME,
        )
        cls._init_run_analyzers_user_inputs(
            analysis_mode_plugin,
            inputs,
            parent_input_name=analysis_enums.AnalysisModeSettingsTypes.BACKTESTING_RUN_ANALYSIS_MODE_SETTINGS_NAME,
        )

    @classmethod
    def _init_run_analyzers_user_inputs(
        cls, analysis_mode_plugin, inputs: dict, parent_input_name: str
    ) -> None:
        enable_run_analysis_mode = analysis_mode_plugin.CLASS_UI.user_input(
            parent_input_name + cls.ENABLE_RUN_ANALYSIS_MODE_SETTING_NAME,
            commons_enums.UserInputTypes.BOOLEAN,
            True,
            inputs,
            title=f"Enable {parent_input_name} Run Analysis Mode",
            parent_input_name=parent_input_name,
            editor_options={
                commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12
            },
        )
        if enable_run_analysis_mode:
            enabled_run_analyzers = analysis_mode_plugin.CLASS_UI.user_input(
                parent_input_name + cls.ENABLED_RUN_ANALYZERS_SETTING_NAME,
                commons_enums.UserInputTypes.MULTIPLE_OPTIONS,
                cls.available_run_analyzer_module_names,
                inputs,
                title=f"Enabled {parent_input_name} Run Analyzers",
                options=cls.available_run_analyzer_module_names,
                parent_input_name=parent_input_name,
                editor_options={
                    commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12
                },
                order=1000,
            )
            sorted_analyzers: typing.List[str] = cls.get_sorted_run_analyzers(
                enabled_run_analyzers
            )
            for run_analyzer_module_name in sorted_analyzers:
                cls._init_run_analyzer_user_inputs(
                    analysis_mode_plugin,
                    run_analyzer_module_name,
                    inputs,
                    parent_input_name,
                )

    @classmethod
    def _init_run_analyzer_user_inputs(
        cls,
        analysis_mode_plugin,
        run_analyzer_module_name: str,
        inputs: dict,
        parent_input_name: str,
    ) -> None:
        group_input_name: str = None
        group_input_title: str = None
        modules: dict = None
        if cls.available_run_analyzer_plot_modules.get(run_analyzer_module_name):
            modules = cls.available_run_analyzer_plot_modules
            group_input_name = (
                parent_input_name
                + analysis_enums.AnalysisModePlotSettingsTypes.PLOTS_SETTINGS_NAME
            )
            group_input_title = (
                analysis_enums.AnalysisModePlotSettingsTypes.PLOTS_SETTINGS_TITLE
            )
        elif cls.available_run_analyzer_table_modules.get(run_analyzer_module_name):
            modules = cls.available_run_analyzer_table_modules
            group_input_name = (
                parent_input_name
                + analysis_enums.AnalysisModePlotSettingsTypes.TABLE_SETTINGS_NAME
            )
            group_input_title = (
                analysis_enums.AnalysisModePlotSettingsTypes.TABLE_SETTINGS_TITLE
            )
        elif cls.available_run_analyzer_dictionaries_modules.get(
            run_analyzer_module_name
        ):
            modules = cls.available_run_analyzer_dictionaries_modules
            group_input_name = (
                parent_input_name
                + analysis_enums.AnalysisModePlotSettingsTypes.DICTIONARY_SETTINGS_NAME
            )
            group_input_title = (
                analysis_enums.AnalysisModePlotSettingsTypes.DICTIONARY_SETTINGS_TITLE
            )
        elif cls.available_run_analyzer_pie_chart_modules.get(run_analyzer_module_name):
            modules = cls.available_run_analyzer_pie_chart_modules
            group_input_name = (
                parent_input_name
                + analysis_enums.AnalysisModePlotSettingsTypes.PIE_CHARTS_SETTINGS_NAME
            )
            group_input_title = (
                analysis_enums.AnalysisModePlotSettingsTypes.PIE_CHARTS_SETTINGS_TITLE
            )
        else:
            return
        cls._init_run_analyzer_user_inputs_group(
            analysis_mode_plugin=analysis_mode_plugin,
            inputs=inputs,
            group_input_name=group_input_name,
            group_input_title=group_input_title,
            parent_input_name=parent_input_name,
        )
        cls._init_run_analyzer_user_inputs_in_module(
            analysis_mode_plugin=analysis_mode_plugin,
            run_analyzer_module_name=run_analyzer_module_name,
            modules=modules,
            inputs=inputs,
            parent_input_name=group_input_name,
        )

    @classmethod
    def _init_run_analyzer_user_inputs_group(
        cls,
        analysis_mode_plugin,
        inputs: dict,
        group_input_name: str,
        group_input_title: str,
        parent_input_name: str,
    ):
        if group_input_name not in cls.initialized_group_input_name:
            analysis_mode_plugin.CLASS_UI.user_input(
                group_input_name,
                commons_enums.UserInputTypes.OBJECT,
                None,
                inputs,
                title=group_input_title,
                parent_input_name=parent_input_name,
                editor_options={
                    commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
                    commons_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: True,
                },
            )
            cls.initialized_group_input_name.append(True)

    @classmethod
    def _init_run_analyzer_user_inputs_in_module(
        cls,
        analysis_mode_plugin,
        run_analyzer_module_name: str,
        inputs: dict,
        modules: dict,
        parent_input_name: str,
    ) -> None:
        for sub_module in modules.get(run_analyzer_module_name, {}).values():
            try:
                sub_module.init_user_inputs(
                    analysis_mode_plugin, inputs, parent_input_name
                )
            except Exception as error:
                cls.logger.exception(
                    error,
                    True,
                    f"Failed to initialize {run_analyzer_module_name} run analyzer",
                )

    @classmethod
    def reload_available_run_analyzers(cls, force_reload: bool = False) -> None:
        if force_reload or not (
            cls.available_run_analyzer_plot_modules
            and cls.available_run_analyzer_table_modules
            and cls.available_run_analyzer_dictionaries_modules
            and cls.available_run_analyzer_pie_chart_modules
        ):
            import tentacles.Meta.Keywords.RunAnalysis.AnalysisEvaluators.Table as analysis_table
            import tentacles.Meta.Keywords.RunAnalysis.AnalysisEvaluators.Plot as analysis_plots
            import tentacles.Meta.Keywords.RunAnalysis.AnalysisEvaluators.Dictionaries as analysis_dictionaries
            import tentacles.Meta.Keywords.RunAnalysis.AnalysisEvaluators.PieCharts as analysis_pie_charts

            cls.available_run_analyzer_plot_modules = (
                run_analysis_factory.get_installed_run_analyzer_modules(analysis_plots)
            )
            cls.available_run_analyzer_table_modules = (
                run_analysis_factory.get_installed_run_analyzer_modules(analysis_table)
            )
            cls.available_run_analyzer_dictionaries_modules = (
                run_analysis_factory.get_installed_run_analyzer_modules(
                    analysis_dictionaries
                )
            )
            cls.available_run_analyzer_pie_chart_modules = (
                run_analysis_factory.get_installed_run_analyzer_modules(
                    analysis_pie_charts
                )
            )
            cls.available_run_analyzer_module_names: list = list(
                set(
                    list(cls.available_run_analyzer_plot_modules.keys())
                    + list(cls.available_run_analyzer_table_modules.keys())
                    + list(cls.available_run_analyzer_dictionaries_modules.keys())
                    + list(cls.available_run_analyzer_pie_chart_modules.keys())
                )
            )

    @classmethod
    def get_run_analyzer_priority(cls, analyzer_name):
        analyzer_module: typing.Dict[abstract_analysis_evaluator.AnalysisEvaluator] = (
            cls.available_run_analyzer_plot_modules.get(analyzer_name)
            or cls.available_run_analyzer_plot_modules.get(analyzer_name)
            or cls.available_run_analyzer_plot_modules.get(analyzer_name)
        )
        return next(iter(analyzer_module.values())).PRIORITY if analyzer_module else 0

    @classmethod
    def get_sorted_run_analyzers(
        cls, enabled_run_analyzers: typing.List[str]
    ) -> typing.List[str]:
        return sorted(
            enabled_run_analyzers, key=cls.get_run_analyzer_priority, reverse=True
        )

    @classmethod
    async def get_and_execute_run_analysis_mode(
        cls,
        trading_mode_class,
        config: dict,
        exchange_name: str,
        exchange_id: str,
        symbol: str,
        time_frame: str,
        backtesting_id: typing.Optional[int] = None,
        optimizer_id: typing.Optional[int] = None,
        live_id: typing.Optional[int] = None,
        optimization_campaign: typing.Optional[str] = None,
    ):
        try:
            await cls.init_mode_features(exchange_id)
        except Exception as error:
            cls.logger.warning(f"Failed to activate candles storage {error}")
            # try to continue

        cls.reload_available_run_analyzers()
        if live_id:
            config_name = (
                analysis_enums.AnalysisModeSettingsTypes.LIVE_RUN_ANALYSIS_MODE_SETTINGS_NAME
            )
            is_backtesting = False
            parent_input_name = (
                analysis_enums.AnalysisModeSettingsTypes.LIVE_RUN_ANALYSIS_MODE_SETTINGS_NAME
            )
        else:
            is_backtesting = True
            config_name = (
                analysis_enums.AnalysisModeSettingsTypes.BACKTESTING_RUN_ANALYSIS_MODE_SETTINGS_NAME
            )
            parent_input_name = (
                analysis_enums.AnalysisModeSettingsTypes.BACKTESTING_RUN_ANALYSIS_MODE_SETTINGS_NAME
            )

        # TODO replace with default context when merged
        ctx: custom_context.Context = custom_context.Context.minimal(
            trading_mode_class=trading_mode_class,
            logger=cls.logger,
            exchange_name=exchange_name,
            traded_pair=symbol,
            backtesting_id=backtesting_id,
            optimizer_id=optimizer_id,
            optimization_campaign_name=optimization_campaign,
            analysis_settings=config.get(config_name, {}),
            live_id=live_id,
        )
        ctx.time_frame = time_frame
        async with ctx.backtesting_results() as (run_database, run_display):
            with run_display.part(
                "main-chart"
            ) as main_plotted_element, run_display.part(
                "sub-chart"
            ) as sub_plotted_element, run_display.part(
                "pie-chart"
            ) as pie_chart_plotted_element, run_display.part(
                "table"
            ) as table_plotted_element:
                run_data = await init_base_data.get_base_data(
                    ctx=ctx,
                    exchange_id=exchange_id,
                    is_backtesting=is_backtesting,
                    run_database=run_database,
                    run_display=run_display,
                    main_plotted_element=main_plotted_element,
                    sub_plotted_element=sub_plotted_element,
                    pie_chart_plotted_element=pie_chart_plotted_element,
                    table_plotted_element=table_plotted_element,
                )
                enabled_run_analyzers = (
                    run_data.config.get(
                        parent_input_name + cls.ENABLED_RUN_ANALYZERS_SETTING_NAME
                    )
                    or cls.available_run_analyzer_module_names
                )
                sorted_analyzers: typing.List[str] = cls.get_sorted_run_analyzers(
                    enabled_run_analyzers
                )
                if run_data.config.get(
                    parent_input_name + cls.ENABLE_RUN_ANALYSIS_MODE_SETTING_NAME,
                    True,
                ):
                    for run_analyzer_module_name in sorted_analyzers:
                        await cls._get_and_execute_run_analyzer_module(
                            run_analyzer_module_name=run_analyzer_module_name,
                            run_data=run_data,
                            parent_input_name=parent_input_name,
                        )
                return run_data.run_display.to_json()

    @classmethod
    async def _get_and_execute_run_analyzer_module(
        cls, run_analyzer_module_name: str, run_data, parent_input_name: str
    ):
        if cls.available_run_analyzer_plot_modules.get(run_analyzer_module_name):
            run_analyzer_module = cls.available_run_analyzer_plot_modules
            _parent_input_name = (
                parent_input_name
                + analysis_enums.AnalysisModePlotSettingsTypes.PLOTS_SETTINGS_NAME
            )
        elif cls.available_run_analyzer_table_modules.get(run_analyzer_module_name):
            run_analyzer_module = cls.available_run_analyzer_table_modules
            _parent_input_name = (
                parent_input_name
                + analysis_enums.AnalysisModePlotSettingsTypes.TABLE_SETTINGS_NAME
            )
        elif cls.available_run_analyzer_dictionaries_modules.get(
            run_analyzer_module_name
        ):
            run_analyzer_module = cls.available_run_analyzer_dictionaries_modules
            _parent_input_name = (
                parent_input_name
                + analysis_enums.AnalysisModePlotSettingsTypes.DICTIONARY_SETTINGS_NAME
            )
        elif cls.available_run_analyzer_pie_chart_modules.get(run_analyzer_module_name):
            run_analyzer_module = cls.available_run_analyzer_pie_chart_modules
            _parent_input_name = (
                parent_input_name
                + analysis_enums.AnalysisModePlotSettingsTypes.PIE_CHARTS_SETTINGS_NAME
            )
        await cls._evaluate_all_run_analyzers_in_module(
            run_analyzer_module_name=run_analyzer_module_name,
            run_analyzer_module=run_analyzer_module,
            run_data=run_data,
            parent_input_name=_parent_input_name,
        )

    @classmethod
    async def _evaluate_all_run_analyzers_in_module(
        cls,
        run_analyzer_module: dict,
        run_analyzer_module_name: str,
        run_data,
        parent_input_name: str,
    ):
        for sub_module in run_analyzer_module[run_analyzer_module_name].values():
            try:
                await sub_module.evaluate(sub_module, run_data, parent_input_name)
            except Exception as error:
                cls.logger.exception(
                    error,
                    True,
                    f"Failed to evaluate {run_analyzer_module_name} run analyzer",
                )

    @classmethod
    async def init_mode_features(cls, exchange_id):
        try:
            exchange_manager = trading_api.get_exchange_manager_from_exchange_id(
                exchange_id
            )
            if not exchange_manager.storage_manager.candles_storage.enabled:
                exchange_manager.storage_manager.candles_storage.enabled = True
                await exchange_manager.storage_manager.candles_storage.start()

        except KeyError:
            raise RuntimeError(
                "Failed to activate candles storage, exchange "
                f"ID is not valid {exchange_id}"
            )
        except Exception as error:
            cls.logger.exception(error, True, "Failed to activate candles storage")

    # async def run_analysis_script(self, run_data):
    #     pass
    # RunAnalysisModePlugin.get_and_execute_run_analysis_mode(ctx)

    # # TODO tmp remove
    # if not "chart_location_unrealized_portfolio_value" in ctx.analysis_settings:
    #     return await default_backtesting_run_analysis_script.default_backtesting_analysis_script(
    #         ctx
    #     )
    # else:
    #     run_data = await init_base_data.get_base_data(ctx)

    #     # TODO add plot_candles and plot_trades and plot_cached_values and plot_withdrawals

    #     # TODO move chart location handling to frontend
    #     for chart_location in {
    #         run_data.analysis_settings["chart_location_unrealized_portfolio_value"],
    #         run_data.analysis_settings["chart_location_realized_portfolio_value"],
    #         run_data.analysis_settings["chart_location_realized_trade_gains"],
    #         run_data.analysis_settings["chart_location_best_case_growth"],
    #         run_data.analysis_settings["chart_location_wins_and_losses_count"],
    #         run_data.analysis_settings["chart_location_win_rate"],
    #     }:
    #         with run_data.run_display.part(chart_location) as plotted_element:
    #             if (
    #                 run_data.analysis_settings["plot_unrealized_portfolio_value"]
    #                 and run_data.analysis_settings[
    #                     "chart_location_unrealized_portfolio_value"
    #                 ]
    #             ):
    #                 await analysis_plots.unrealized_portfolio_value(
    #                     run_data,
    #                     plotted_element,
    #                     own_yaxis=True,
    #                     all_coins_in_ref_market=run_data.analysis_settings.get(
    #                         "plot_unrealized_portfolio_value_for_each_asset"
    #                     ),
    #                     all_coins_amounts=run_data.analysis_settings.get(
    #                         "plot_unrealized_portfolio_amount_for_each_asset"
    #                     ),
    #                     total_amount_in_btc=run_data.analysis_settings.get(
    #                         "plot_unrealized_portfolio_amount_in_btc"
    #                     ),
    #                 )
    #             if (
    #                 run_data.analysis_settings["plot_realized_portfolio_value"]
    #                 and run_data.analysis_settings[
    #                     "chart_location_realized_portfolio_value"
    #                 ]
    #             ):
    #                 await analysis_plots.plot_realized_portfolio_value(
    #                     run_data,
    #                     plotted_element,
    #                     x_as_trade_count=False,
    #                     own_yaxis=True,
    #                 )
    #             if (
    #                 run_data.analysis_settings["plot_realized_trade_gains"]
    #                 and run_data.analysis_settings[
    #                     "chart_location_realized_trade_gains"
    #                 ]
    #             ):
    #                 await analysis_plots.plot_realized_trade_gains(
    #                     run_data,
    #                     plotted_element,
    #                     x_as_trade_count=False,
    #                     own_yaxis=True,
    #                 )

    #             if (
    #                 run_data.analysis_settings["plot_best_case_growth"]
    #                 and run_data.analysis_settings[
    #                     "chart_location_best_case_growth"
    #                 ]
    #             ):
    #                 await analysis_plots.plot_best_case_growth(
    #                     run_data,
    #                     plotted_element,
    #                     x_as_trade_count=False,
    #                     own_yaxis=False,
    #                 )
    #             if (
    #                 run_data.analysis_settings["plot_funding_fees"]
    #                 and run_data.analysis_settings["chart_location_funding_fees"]
    #             ):
    #                 await analysis_plots.plot_historical_fees(
    #                     run_data,
    #                     plotted_element,
    #                     own_yaxis=True,
    #                 )
    #             if (
    #                 run_data.analysis_settings["plot_wins_and_losses_count"]
    #                 and run_data.analysis_settings[
    #                     "chart_location_wins_and_losses_count"
    #                 ]
    #             ):
    #                 analysis_plots.historical_wins_and_losses(
    #                     run_data,
    #                     plotted_element,
    #                     own_yaxis=True,
    #                     x_as_trade_count=False,
    #                 )
    #             if (
    #                 run_data.analysis_settings["plot_win_rate"]
    #                 and run_data.analysis_settings["chart_location_win_rate"]
    #             ):
    #                 analysis_plots.historical_win_rates(
    #                     run_data,
    #                     plotted_element,
    #                     own_yaxis=True,
    #                     x_as_trade_count=False,
    #                 )
    #             # if (
    #             #     run_data.analysis_settings["plot_withdrawals"]
    #             #     and run_data.analysis_settings["chart_location_withdrawals"]
    #             # ):
    #             #     await run_analysis_plots.plot_withdrawals(run_data, plotted_element)
    #     with run_data.run_display.part("list-of-trades-part", "table") as part:
    #         if run_data.analysis_settings["display_trades_and_positions"]:
    #             await analysis_table.plot_trades_table(run_data.run_database, part)
    #             await analysis_table.plot_positions_table(run_data, part)
    #         if run_data.analysis_settings["display_withdrawals_table"]:
    #             await analysis_table.plot_withdrawals_table(
    #                 run_data, plotted_element
    #             )

    #     # TODO allow to define cache keys via api
    #     # await plot_table(run_data, part, "SMA 1")  # plot any cache key as a table
    # return run_data.run_display
