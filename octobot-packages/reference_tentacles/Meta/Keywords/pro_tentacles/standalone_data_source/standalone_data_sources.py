# a42.ch CONFIDENTIAL
# __________________
#
#  [2021] - [∞] a42.ch Incorporated
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of a42.ch Incorporated and its suppliers,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to a42.ch Incorporated
# and its suppliers and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from a42.ch Incorporated.
#
# If you want to use any code for commercial purposes,
# or you want your own custom solution,
# please contact me at max@a42.ch

import time
from octobot_services import interfaces
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)


async def activate_standalone_data_source(
    title,
    parent_input_name: str = None,
    indicator_id: int = 1,
    maker=None,
):
    # use higher ids to avoid conflicts with strategy maker

    data_source_values, indicator = await _get_standalone_data_source(
        maker, title, parent_input_name, indicator_id
    )
    times = await get_candles_(maker, PriceDataSources.TIME.value)
    times, data_source_values = cut_data_to_same_len((times, data_source_values))

    data_source_dict = {}
    for index in range(len(data_source_values)):
        data_source_dict[times[index]] = data_source_values[index]
    cache_path = get_cache_path(maker, indicator_id)
    maker.consumable_indicator_cache[cache_path] = data_source_dict
    maker.standalone_indicators[cache_path] = indicator
    return indicator


def get_standalone_data_source(indicator_id, maker):
    # use higher ids to avoid conflicts with strategy maker
    try:
        return maker.consumable_indicator_cache[get_cache_path(maker, indicator_id)][
            float(maker.ctx.trigger_cache_timestamp)
        ]
    except KeyError as error:
        running_seconds = time.time() - interfaces.get_bot_api().get_start_time()
        if running_seconds > 50:
            raise RuntimeError(
                f"Data source {maker.standalone_indicators[indicator_id].shared_cache_path or maker.standalone_indicators[indicator_id].cache_path } doesnt have a value for the "
                f"current candle. Check the candle history size"
            ) from error


async def _get_standalone_data_source(
    maker,
    title,
    parent_input_name: str = None,
    indicator_id: int = 1,
):
    from tentacles.Meta.Keywords.pro_tentacles.evaluators.evaluators_handling import (
        Evaluator_,
    )
    from tentacles.Meta.Keywords.pro_tentacles.indicators import (
        Indicator,
    )

    _evaluator = Evaluator_(
        maker,
        input_path_short_root=parent_input_name,
        input_name_root=parent_input_name,
    )
    await _evaluator.init_evaluator(
        maker, maker.ctx, indicator_id, use_compact_mode=True
    )
    indicator = Indicator()
    await indicator.init_indicator(
        maker,
        _evaluator,
        data_source_name=title,
        def_val="EMA",
        enable_oscillators=True,
        enable_price_indicators=True,
        enable_price_data=True,
        enable_volume=True,
        enable_static_value=True,
        enable_force_def_val=False,
        supports_shared_sources=False,
    )
    indicator.time_frame = maker.ctx.time_frame
    maker.indicators[indicator.cache_path] = _evaluator.indicators[
        indicator_id
    ] = indicator
    maker.current_strategy_id = None
    data_source_values, _, _ = await indicator.get_indicator_data(
        maker,
        evaluator=_evaluator,
    )
    return data_source_values, indicator


def get_cache_path(maker, indicator_id):
    return (
        f"b-{indicator_id}"
        if maker.ctx.exchange_manager.is_backtesting
        else f"l-{indicator_id}"
    )
