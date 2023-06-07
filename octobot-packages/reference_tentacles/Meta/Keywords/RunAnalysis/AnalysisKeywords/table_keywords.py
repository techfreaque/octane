import typing
from tentacles.Meta.Keywords.RunAnalysis.BaseDataProvider.default_base_data_provider import (
    base_data_provider,
)


def plot_table_data(
    data,
    data_name: str,
    run_data: base_data_provider.RunAnalysisBaseDataGenerator,
    additional_key_to_label: dict,
    additional_columns: list,
    additional_column_types: typing.Dict[str, str],
    datum_columns_callback,
    icon: typing.Optional[str] = None,
):
    if not data:
        run_data.logger.debug(
            f"Nothing to create a table from when reading {data_name}"
        )
        return
    column_render = _get_default_column_render()
    types = {**_get_default_types(), **additional_column_types}
    key_to_label = {
        **run_data.table_plotted_element.TABLE_KEY_TO_COLUMN,
        **additional_key_to_label,
    }
    columns = (
        _get_default_columns(
            run_data.table_plotted_element, data, column_render, key_to_label
        )
        + additional_columns
    )
    if datum_columns_callback:
        for datum in data:
            datum_columns_callback(datum)
    rows = _get_default_rows(data, columns)
    searches = _get_default_searches(columns, types)
    try:
        run_data.table_plotted_element.table(
            data_name,
            columns=columns,
            rows=rows,
            searches=searches,
            config={"antIcon": icon},
        )
    except Exception:
        # TODO remove when merged
        run_data.table_plotted_element.table(
            data_name,
            columns=columns,
            rows=rows,
            searches=searches,
        )


# async def plot_table(
#     meta_database,
#     plotted_element,
#     data_source,
#     columns=None,
#     rows=None,
#     searches=None,
#     column_render=None,
#     types=None,
#     cache_value=None,
# ):
#     data = []
#     if data_source == commons_enums.DBTables.TRADES.value:
#         data = await meta_database.get_trades_db().all(
#             commons_enums.DBTables.TRADES.value
#         )
#     elif data_source == commons_enums.DBTables.ORDERS.value:
#         data = await meta_database.get_orders_db().all(
#             commons_enums.DBTables.ORDERS.value
#         )
#     else:
#         exchange = meta_database.run_dbs_identifier.context.exchange_name
#         symbol = meta_database.run_dbs_identifier.context.symbol
#         symbol_db = meta_database.get_symbol_db(exchange, symbol)
#         if cache_value is None:
#             data = await symbol_db.all(data_source)
#         else:
#             query = (await symbol_db.search()).title == data_source
#             cache_data = await symbol_db.select(
#                 commons_enums.DBTables.CACHE_SOURCE.value, query
#             )
#             if cache_data:
#                 try:
#                     cache_database = databases.CacheDatabase(
#                         cache_data[0][commons_enums.PlotAttributes.VALUE.value]
#                     )
#                     cache = await cache_database.get_cache()
#                     x_shift = cache_data[0]["x_shift"]
#                     data = [
#                         {
#                             "x": (
#                                 cache_element[
#                                     commons_enums.CacheDatabaseColumns.TIMESTAMP.value
#                                 ]
#                                 + x_shift
#                             )
#                             * 1000,
#                             "y": cache_element[cache_value],
#                         }
#                         for cache_element in cache
#                     ]
#                 except KeyError as error:
#                     get_base_data_logger().warning(
#                         f"Missing cache values when plotting data: {error}"
#                     )
#                 except commons_errors.DatabaseNotFoundError as error:
#                     get_base_data_logger().warning(
#                         f"Missing cache values when plotting data: {error}"
#                     )

#     if not data:
#         get_base_data_logger().debug(
#             f"Nothing to create a table from when reading {data_source}"
#         )
#         return
#     column_render = column_render or _get_default_column_render()
#     types = types or _get_default_types()
#     columns = columns or _get_default_columns(plotted_element, data, column_render)
#     rows = rows or _get_default_rows(data, columns)
#     searches = searches or _get_default_searches(columns, types)
#     plotted_element.table(data_source, columns=columns, rows=rows, searches=searches)


def _get_default_column_render():
    return {"Time": "datetime", "Entry time": "datetime", "Exit time": "datetime"}


def _get_default_types():
    return {
        "Time": "datetime",
        "Entry time": "datetime",
        "Exit time": "datetime",
    }


def _get_default_columns(plotted_element, data, column_render, key_to_label=None):
    key_to_label = key_to_label or plotted_element.TABLE_KEY_TO_COLUMN
    return [
        {
            "field": row_key,
            "text": key_to_label[row_key],
            "render": column_render.get(key_to_label[row_key], None),
            "sortable": True,
        }
        for row_key, row_value in data[0].items()
        if row_key in key_to_label and row_value is not None
    ]


def _get_default_rows(data, columns):
    column_fields = set(col["field"] for col in columns)
    return [
        {key: val for key, val in row.items() if key in column_fields} for row in data
    ]


def _get_default_searches(columns, types):
    return [
        {
            "field": col["field"],
            "label": col["text"],
            "type": types.get(col["text"]),
        }
        for col in columns
    ]
