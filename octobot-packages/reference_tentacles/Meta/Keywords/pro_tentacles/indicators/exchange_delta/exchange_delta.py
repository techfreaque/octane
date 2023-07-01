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

from octobot_trading.api.exchange import (
    get_all_exchange_ids_from_matrix_id,
    get_exchange_managers_from_exchange_ids,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools import (
    utilities,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
    user_select_candle_source_name,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_indicator_data,
    allow_enable_plot,
)
import tentacles.Meta.Keywords.pro_tentacles.pro_keywords.orders.managed_order_pro.calculators.position_sizing as position_sizing


class OtherExchangeNotInitializedError(Exception):
    """
    Raised when the candle data for the other
    exchange is not initialized or available yet
    """


async def get_exchange_delta(maker, indicator, evaluator):
    matrix_id = maker.ctx.matrix_id
    exchange_ids = get_all_exchange_ids_from_matrix_id(matrix_id)
    exchange_managers = get_exchange_managers_from_exchange_ids(exchange_ids)
    exchanges = [
        exchange_manager.exchange_name for exchange_manager in exchange_managers
    ]
    candle_source_name = await user_select_candle_source_name(
        maker, indicator, "Select Candle Source"
    )
    # from_exchange = await user_input2(
    #     maker, indicator, "From exchange", "options", exchanges[0], options=exchanges
    # )
    to_exchange = await user_input2(
        maker,
        indicator,
        "Reference exchange",
        "options",
        exchanges[-1],
        options=exchanges,
    )
    plot_precent = await user_input2(
        maker,
        indicator,
        "Plot percent insted of prices",
        "boolean",
        True,
    )
    plot_fees = await user_input2(
        maker,
        indicator,
        "Plot fees as a horizontal line",
        "boolean",
        True,
    )
    await allow_enable_plot(maker, indicator, "Plot exchange delta")
    from_closes = None
    to_closes = None
    from_exchange_fee = None
    from_closes = await get_candles_(
        maker,
        candle_source_name,
        time_frame=maker.ctx.time_frame,
        symbol=maker.ctx.symbol,
    )
    from_exchange_fee = None
    data_source = {
        "v": {
            "title": f" candle {candle_source_name} delta from "
            f"{maker.ctx.exchange_manager.exchange_name} to {to_exchange}",
            "chart_location": "sub-chart",
        },
        "f": {
            "title": f"{maker.ctx.exchange_manager.exchange_name} "
            f"{candle_source_name} price",
            "chart_location": "main-chart",
        },
        "t": {
            "title": f"{to_exchange} {candle_source_name} price",
            "chart_location": "main-chart",
        },
        "lf": {
            "title": f"Long Maker and Taker fee for "
            f"{maker.ctx.exchange_manager.exchange_name}",
            "chart_location": "sub-chart",
        },
        "hf": {
            "title": f"Short Maker and Taker fee for "
            f"{maker.ctx.exchange_manager.exchange_name}",
            "chart_location": "sub-chart",
        },
        "llf": {
            "title": f"Long Maker and Maker fee for "
            f"{maker.ctx.exchange_manager.exchange_name}",
            "chart_location": "sub-chart",
        },
        "hlf": {
            "title": f"Short Maker and Maker fee for "
            f"{maker.ctx.exchange_manager.exchange_name}",
            "chart_location": "sub-chart",
        },
    }
    if plot_fees:
        from_exchange_fee = position_sizing.get_fees(maker.ctx, use_decimal=False)
        limit_fee, market_fee = from_exchange_fee
        data_len = len(from_closes)
        from_exchange_fee_low = [limit_fee + market_fee] * data_len
        from_exchange_fee_high = [(market_fee + limit_fee) * -1] * data_len
        from_exchange_fee_low_limit = [limit_fee * 2] * data_len
        from_exchange_fee_high_limit = [limit_fee * -2] * data_len
        data_source["lf"]["data"] = from_exchange_fee_low
        data_source["hf"]["data"] = from_exchange_fee_high
        data_source["llf"]["data"] = from_exchange_fee_low_limit
        data_source["hlf"]["data"] = from_exchange_fee_high_limit
    try:
        for exchange_manager in exchange_managers:
            if to_exchange == exchange_manager.exchange_name:
                to_closes = await get_candles_(
                    exchange_manager.trading_modes[0].producers[0],
                    candle_source_name,
                    time_frame=maker.ctx.time_frame,
                    symbol=utilities.get_similar_symbol(
                        symbol=maker.ctx.symbol,
                        this_exchange_manager=maker.exchange_manager,
                        other_exchange_manager=exchange_manager,
                    ),
                )
                break
        if to_closes is None:
            raise OtherExchangeNotInitializedError
        from_closes, to_closes = cut_data_to_same_len((from_closes, to_closes))
        if plot_precent:
            delta_data = (to_closes - from_closes) / (to_closes / 100)
        else:
            delta_data = to_closes - from_closes
        data_source["v"]["data"] = delta_data
        data_source["f"]["data"] = from_closes
        data_source["t"]["data"] = to_closes
    except (
        AttributeError,
        TypeError,
        OtherExchangeNotInitializedError,
        IndexError,
    ) as error:
        data_source["v"]["data"] = [0]
        data_source["f"]["data"] = [0]
        data_source["t"]["data"] = [0]
        maker.logger.info(
            "Plot exchange delta is not possible. Other exchange is not initialized - "
            f"this is normal if you just started octobot. Error: {error}"
        )
    return await store_indicator_data(maker, indicator, data_source)
