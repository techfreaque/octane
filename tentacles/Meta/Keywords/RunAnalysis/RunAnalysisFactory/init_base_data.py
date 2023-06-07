import octobot_commons.enums as commons_enums
import octobot_trading.modes.script_keywords.context_management as context_management
import tentacles.Meta.Keywords.scripting_library.UI.plots.displayed_elements as displayed_elements
import tentacles.Meta.Keywords.RunAnalysis.BaseDataProvider.default_base_data_provider.future_base_data_provider as future_base_data_provider
import tentacles.Meta.Keywords.RunAnalysis.BaseDataProvider.default_base_data_provider.spot_base_data_provider as spot_base_data_provider
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.analysis_errors as analysis_errors


async def get_base_data(
    ctx: context_management.Context,
    exchange_id: str,
    is_backtesting: bool,
    run_database,
    run_display,
    main_plotted_element: displayed_elements.DisplayedElements,
    sub_plotted_element: displayed_elements.DisplayedElements,
    pie_chart_plotted_element: displayed_elements.DisplayedElements,
    table_plotted_element: displayed_elements.DisplayedElements,
):
    # load and generate unified base data

    metadata = await _get_metadata(run_database)

    if ctx.time_frame not in metadata.get(
        commons_enums.BacktestingMetadata.TIME_FRAMES.value, []
    ):
        # timeframe not available, use first available
        ctx.time_frame = metadata[commons_enums.BacktestingMetadata.TIME_FRAMES.value][
            0
        ]
    if metadata["trading_type"] == "spot":
        run_data = spot_base_data_provider.SpotRunAnalysisBaseDataGenerator(
            ctx=ctx,
            run_database=run_database,
            run_display=run_display,
            metadata=metadata,
            is_backtesting=is_backtesting,
            main_plotted_element=main_plotted_element,
            sub_plotted_element=sub_plotted_element,
            pie_chart_plotted_element=pie_chart_plotted_element,
            table_plotted_element=table_plotted_element,
        )
    elif metadata["trading_type"] == "future":
        run_data = future_base_data_provider.FutureRunAnalysisBaseDataGenerator(
            ctx=ctx,
            run_database=run_database,
            run_display=run_display,
            metadata=metadata,
            is_backtesting=is_backtesting,
            main_plotted_element=main_plotted_element,
            sub_plotted_element=sub_plotted_element,
            pie_chart_plotted_element=pie_chart_plotted_element,
            table_plotted_element=table_plotted_element,
        )
    else:
        raise NotImplementedError(
            f"RunDataAnalysis is not supported for {metadata['trading_type']}"
        )
    await run_data.load_base_data(exchange_id)
    return run_data


async def _get_metadata(run_database):
    try:
        return (
            await run_database.get_run_db().all(commons_enums.DBTables.METADATA.value)
        )[0]
    except IndexError:
        raise analysis_errors.LiveMetaDataNotInitializedError
