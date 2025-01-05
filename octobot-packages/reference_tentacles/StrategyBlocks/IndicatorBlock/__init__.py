from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version("0.9.52", "ema", "Matrix-Strategy-Blocks"):
    try:
        from .ema import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading ema: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "combined_indicator_line", "Matrix-Strategy-Blocks"
):
    try:
        from .combined_indicator_line import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading combined_indicator_line: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "rsi", "Matrix-Strategy-Blocks"):
    try:
        from .rsi import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading rsi: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "price_data", "Matrix-Strategy-Blocks"):
    try:
        from .price_data import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading price_data: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "static_value", "Matrix-Strategy-Blocks"):
    try:
        from .static_value import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading static_value: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "evwma", "Matrix-Strategy-Blocks"):
    try:
        from .evwma import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading evwma: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "sma", "Matrix-Strategy-Blocks"):
    try:
        from .sma import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading sma: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "zlema", "Matrix-Strategy-Blocks"):
    try:
        from .zlema import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading zlema: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "ultimate_oscillator", "Matrix-Strategy-Blocks"):
    try:
        from .ultimate_oscillator import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading ultimate_oscillator: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "vwap", "Matrix-Strategy-Blocks"):
    try:
        from .vwap import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading vwap: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "balance_of_power", "Matrix-Strategy-Blocks"):
    try:
        from .balance_of_power import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading balance_of_power: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "special_lows", "Matrix-Strategy-Blocks"):
    try:
        from .special_lows import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading special_lows: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "hma", "Matrix-Strategy-Blocks"):
    try:
        from .hma import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading hma: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "vector_addition", "Matrix-Strategy-Blocks"):
    try:
        from .vector_addition import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading vector_addition: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "magic_trend", "Matrix-Strategy-Blocks"):
    try:
        from .magic_trend import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading magic_trend: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "fib_line", "Matrix-Strategy-Blocks"):
    try:
        from .fib_line import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading fib_line: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "aroon", "Matrix-Strategy-Blocks"):
    try:
        from .aroon import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading aroon: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "mfi", "Matrix-Strategy-Blocks"):
    try:
        from .mfi import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading mfi: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "williams_r", "Matrix-Strategy-Blocks"):
    try:
        from .williams_r import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading williams_r: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "break_up2", "Matrix-Strategy-Blocks"):
    try:
        from .break_up2 import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading break_up2: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "break_up", "Matrix-Strategy-Blocks"):
    try:
        from .break_up import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading break_up: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "accumulation_distribution_line", "Matrix-Strategy-Blocks"
):
    try:
        from .accumulation_distribution_line import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading accumulation_distribution_line: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "awesome_oscillator", "Matrix-Strategy-Blocks"):
    try:
        from .awesome_oscillator import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading awesome_oscillator: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "vw_macd", "Matrix-Strategy-Blocks"):
    try:
        from .vw_macd import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading vw_macd: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "supertrend", "Matrix-Strategy-Blocks"):
    try:
        from .supertrend import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading supertrend: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "break_down", "Matrix-Strategy-Blocks"):
    try:
        from .break_down import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading break_down: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "vector_absolute_value", "Matrix-Strategy-Blocks"):
    try:
        from .vector_absolute_value import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading vector_absolute_value: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "dema", "Matrix-Strategy-Blocks"):
    try:
        from .dema import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading dema: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "tema", "Matrix-Strategy-Blocks"):
    try:
        from .tema import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading tema: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "vwma", "Matrix-Strategy-Blocks"):
    try:
        from .vwma import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading vwma: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "growth_rate", "Matrix-Strategy-Blocks"):
    try:
        from .growth_rate import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading growth_rate: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "ichimoku", "Matrix-Strategy-Blocks"):
    try:
        from .ichimoku import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading ichimoku: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "cci", "Matrix-Strategy-Blocks"):
    try:
        from .cci import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading cci: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "obv", "Matrix-Strategy-Blocks"):
    try:
        from .obv import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading obv: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "bollinger_bands", "Matrix-Strategy-Blocks"):
    try:
        from .bollinger_bands import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bollinger_bands: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "stochastic_oscillator", "Matrix-Strategy-Blocks"):
    try:
        from .stochastic_oscillator import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading stochastic_oscillator: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "alma", "Matrix-Strategy-Blocks"):
    try:
        from .alma import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading alma: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "wma", "Matrix-Strategy-Blocks"):
    try:
        from .wma import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading wma: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "atr", "Matrix-Strategy-Blocks"):
    try:
        from .atr import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading atr: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "candle_average", "Matrix-Strategy-Blocks"):
    try:
        from .candle_average import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading candle_average: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "ssl_channel", "Matrix-Strategy-Blocks"):
    try:
        from .ssl_channel import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading ssl_channel: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "halftrend", "Matrix-Strategy-Blocks"):
    try:
        from .halftrend import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading halftrend: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "adx", "Matrix-Strategy-Blocks"):
    try:
        from .adx import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading adx: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "KELTNER_CHANNEL", "Matrix-Strategy-Blocks"):
    try:
        from .KELTNER_CHANNEL import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading KELTNER_CHANNEL: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "ev_macd", "Matrix-Strategy-Blocks"):
    try:
        from .ev_macd import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading ev_macd: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "aroon_oscillator", "Matrix-Strategy-Blocks"):
    try:
        from .aroon_oscillator import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading aroon_oscillator: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "candle_range", "Matrix-Strategy-Blocks"):
    try:
        from .candle_range import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading candle_range: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "absolute_price_oscillator", "Matrix-Strategy-Blocks"
):
    try:
        from .absolute_price_oscillator import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading absolute_price_oscillator: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "special_highs", "Matrix-Strategy-Blocks"):
    try:
        from .special_highs import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading special_highs: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "accumulation_distribution_oscillator", "Matrix-Strategy-Blocks"
):
    try:
        from .accumulation_distribution_oscillator import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading accumulation_distribution_oscillator: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "average_directional_movement_rating", "Matrix-Strategy-Blocks"
):
    try:
        from .average_directional_movement_rating import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading average_directional_movement_rating: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "psar", "Matrix-Strategy-Blocks"):
    try:
        from .psar import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading psar: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "break_down2", "Matrix-Strategy-Blocks"):
    try:
        from .break_down2 import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading break_down2: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "chande_momentum_oscillator", "Matrix-Strategy-Blocks"
):
    try:
        from .chande_momentum_oscillator import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading chande_momentum_oscillator: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "macd", "Matrix-Strategy-Blocks"):
    try:
        from .macd import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading macd: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "unbroken_highs_and_lows", "Matrix-Strategy-Blocks"
):
    try:
        from .unbroken_highs_and_lows import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading unbroken_highs_and_lows: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "highs_and_lows", "Matrix-Strategy-Blocks"):
    try:
        from .highs_and_lows import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading highs_and_lows: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "exchange_delta", "Matrix-Strategy-Blocks"):
    try:
        from .exchange_delta import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading exchange_delta: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "open_interest", "Octane-Default-Tentacles"):
    try:
        from .open_interest import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading open_interest: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "math", "Octane-Default-Tentacles"):
    try:
        from .math import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading math: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )
