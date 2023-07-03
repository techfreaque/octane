import tulipy
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums import (
    PriceDataSources,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_indicator_data,
    allow_enable_plot,
)


async def get_awesome_oscillator(maker, indicator, evaluator):
    await allow_enable_plot(maker, indicator, "Plot awesome_oscillator")
    data = tulipy.ao(
        await get_candles_(maker, PriceDataSources.HIGH.value),
        await get_candles_(maker, PriceDataSources.LOW.value),
    )
    data_source = {
        "v": {
            "title": "awesome_oscillator",
            "data": data,
            "chart_location": "sub-chart",
        }
    }
    return await store_indicator_data(maker, indicator, data_source)
