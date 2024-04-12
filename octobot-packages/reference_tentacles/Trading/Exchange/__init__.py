from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version("1.2.0", "ascendex", "OctoBot-Default-Tentacles"):
    try:
        from .ascendex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading ascendex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "ascendex_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .ascendex_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading ascendex_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

# if check_tentacle_version('1.2.0', 'binanceusdm_websocket_feed', 'OctoBot-Default-Tentacles'):
#     try:
#         from .binanceusdm_websocket_feed import *
#     except Exception as e:
#         get_logger('TentacleLoader').error(f'Error when loading binanceusdm_websocket_feed: '
#                                            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
#                                            f'error persists, try reinstalling your tentacles via '
#                                            f'"python start.py tentacles --install --all".')

if check_tentacle_version("1.2.0", "binance", "OctoBot-Default-Tentacles"):
    try:
        from .binance import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading binance: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "binanceusdm", "OctoBot-Default-Tentacles"):
    try:
        from .binanceusdm import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading binanceusdm: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "binanceus", "OctoBot-Default-Tentacles"):
    try:
        from .binanceus import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading binanceus: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "binanceus_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .binanceus_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading binanceus_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "binance_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .binance_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading binance_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bitfinex", "OctoBot-Default-Tentacles"):
    try:
        from .bitfinex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitfinex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "bitfinex_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .bitfinex_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitfinex_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bitget", "OctoBot-Default-Tentacles"):
    try:
        from .bitget import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitget: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "bitget_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .bitget_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitget_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bithumb", "OctoBot-Default-Tentacles"):
    try:
        from .bithumb import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bithumb: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bitmex", "OctoBot-Default-Tentacles"):
    try:
        from .bitmex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitmex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bitstamp", "OctoBot-Default-Tentacles"):
    try:
        from .bitstamp import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitstamp: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bittrex", "OctoBot-Default-Tentacles"):
    try:
        from .bittrex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bittrex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "bittrex_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .bittrex_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bittrex_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bybit", "OctoBot-Default-Tentacles"):
    try:
        from .bybit import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bybit: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "coinbase_pro", "OctoBot-Default-Tentacles"):
    try:
        from .coinbase_pro import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading coinbase_pro: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "coinbase_pro_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .coinbase_pro_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading coinbase_pro_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "coinex", "OctoBot-Default-Tentacles"):
    try:
        from .coinex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading coinex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "gateio", "OctoBot-Default-Tentacles"):
    try:
        from .gateio import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading gateio: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "gateio_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .gateio_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading gateio_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "hitbtc", "OctoBot-Default-Tentacles"):
    try:
        from .hitbtc import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading hitbtc: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "hollaex", "OctoBot-Default-Tentacles"):
    try:
        from .hollaex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading hollaex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "huobi", "OctoBot-Default-Tentacles"):
    try:
        from .huobi import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading huobi: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "huobipro", "OctoBot-Default-Tentacles"):
    try:
        from .huobipro import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading huobipro: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "huobi_websocket_feed", "OctoBot-Default-Tentacles"):
    try:
        from .huobi_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading huobi_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "kraken", "OctoBot-Default-Tentacles"):
    try:
        from .kraken import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading kraken: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "kraken_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .kraken_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading kraken_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "kucoin", "OctoBot-Default-Tentacles"):
    try:
        from .kucoin import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading kucoin: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "kucoin_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .kucoin_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading kucoin_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "okcoin", "OctoBot-Default-Tentacles"):
    try:
        from .okcoin import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading okcoin: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "okx", "OctoBot-Default-Tentacles"):
    try:
        from .okx import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading okx: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "okx_websocket_feed", "OctoBot-Default-Tentacles"):
    try:
        from .okx_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading okx_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "phemex", "OctoBot-Default-Tentacles"):
    try:
        from .phemex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading phemex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "phemex_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .phemex_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading phemex_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "poloniex", "OctoBot-Default-Tentacles"):
    try:
        from .poloniex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading poloniex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "upbitexchange", "OctoBot-Default-Tentacles"):
    try:
        from .upbitexchange import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading upbitexchange: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "wavesexchange", "OctoBot-Default-Tentacles"):
    try:
        from .wavesexchange import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading wavesexchange: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bitso", "OctoBot-Default-Tentacles"):
    try:
        from .bitso import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitso: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "ndax", "OctoBot-Default-Tentacles"):
    try:
        from .ndax import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading ndax: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

# if check_tentacle_version('1.2.0', 'binancecoinm', 'OctoBot-Default-Tentacles'):
#     try:
#         from .binancecoinm import *
#     except Exception as e:
#         get_logger('TentacleLoader').error(f'Error when loading binancecoinm: '
#                                            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
#                                            f'error persists, try reinstalling your tentacles via '
#                                            f'"python start.py tentacles --install --all".')

if check_tentacle_version("1.2.0", "bybit_websocket_feed", "OctoBot-Default-Tentacles"):
    try:
        from .bybit_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bybit_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "configurable_default_ccxt_rest", "OctoBot-Default-Tentacles"
):
    try:
        from .configurable_default_ccxt_rest import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading configurable_default_ccxt_rest: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "huobipro_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .huobipro_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading huobipro_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "ascendex", "OctoBot-Default-Tentacles"):
    try:
        from .ascendex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading ascendex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "ascendex_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .ascendex_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading ascendex_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "binance", "OctoBot-Default-Tentacles"):
    try:
        from .binance import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading binance: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "binanceus", "OctoBot-Default-Tentacles"):
    try:
        from .binanceus import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading binanceus: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "binanceusdm", "OctoBot-Default-Tentacles"):
    try:
        from .binanceusdm import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading binanceusdm: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "binanceus_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .binanceus_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading binanceus_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "binance_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .binance_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading binance_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bitfinex", "OctoBot-Default-Tentacles"):
    try:
        from .bitfinex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitfinex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "bitfinex_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .bitfinex_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitfinex_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bitget", "OctoBot-Default-Tentacles"):
    try:
        from .bitget import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitget: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "bitget_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .bitget_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitget_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bithumb", "OctoBot-Default-Tentacles"):
    try:
        from .bithumb import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bithumb: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bitmex", "OctoBot-Default-Tentacles"):
    try:
        from .bitmex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitmex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bitso", "OctoBot-Default-Tentacles"):
    try:
        from .bitso import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitso: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bitstamp", "OctoBot-Default-Tentacles"):
    try:
        from .bitstamp import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bitstamp: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bittrex", "OctoBot-Default-Tentacles"):
    try:
        from .bittrex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bittrex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "bittrex_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .bittrex_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bittrex_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bybit", "OctoBot-Default-Tentacles"):
    try:
        from .bybit import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bybit: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "bybit_websocket_feed", "OctoBot-Default-Tentacles"):
    try:
        from .bybit_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading bybit_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "coinbase_pro", "OctoBot-Default-Tentacles"):
    try:
        from .coinbase_pro import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading coinbase_pro: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "coinbase_pro_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .coinbase_pro_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading coinbase_pro_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "coinex", "OctoBot-Default-Tentacles"):
    try:
        from .coinex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading coinex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "gateio", "OctoBot-Default-Tentacles"):
    try:
        from .gateio import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading gateio: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "gateio_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .gateio_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading gateio_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "hitbtc", "OctoBot-Default-Tentacles"):
    try:
        from .hitbtc import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading hitbtc: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "hollaex", "OctoBot-Default-Tentacles"):
    try:
        from .hollaex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading hollaex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "huobi", "OctoBot-Default-Tentacles"):
    try:
        from .huobi import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading huobi: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "huobipro", "OctoBot-Default-Tentacles"):
    try:
        from .huobipro import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading huobipro: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "huobipro_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .huobipro_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading huobipro_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "huobi_websocket_feed", "OctoBot-Default-Tentacles"):
    try:
        from .huobi_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading huobi_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "kraken", "OctoBot-Default-Tentacles"):
    try:
        from .kraken import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading kraken: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "kraken_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .kraken_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading kraken_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "kucoin", "OctoBot-Default-Tentacles"):
    try:
        from .kucoin import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading kucoin: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "kucoin_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .kucoin_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading kucoin_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "ndax", "OctoBot-Default-Tentacles"):
    try:
        from .ndax import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading ndax: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "okcoin", "OctoBot-Default-Tentacles"):
    try:
        from .okcoin import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading okcoin: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "okx", "OctoBot-Default-Tentacles"):
    try:
        from .okx import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading okx: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "okx_websocket_feed", "OctoBot-Default-Tentacles"):
    try:
        from .okx_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading okx_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "phemex", "OctoBot-Default-Tentacles"):
    try:
        from .phemex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading phemex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "1.2.0", "phemex_websocket_feed", "OctoBot-Default-Tentacles"
):
    try:
        from .phemex_websocket_feed import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading phemex_websocket_feed: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "poloniex", "OctoBot-Default-Tentacles"):
    try:
        from .poloniex import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading poloniex: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "upbitexchange", "OctoBot-Default-Tentacles"):
    try:
        from .upbitexchange import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading upbitexchange: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.2.0", "wavesexchange", "OctoBot-Default-Tentacles"):
    try:
        from .wavesexchange import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading wavesexchange: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version('1.2.0', 'ascendex', 'OctoBot-Default-Tentacles'):
    try:
        from .ascendex import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading ascendex: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'ascendex_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .ascendex_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading ascendex_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'binance', 'OctoBot-Default-Tentacles'):
    try:
        from .binance import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading binance: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'binanceus', 'OctoBot-Default-Tentacles'):
    try:
        from .binanceus import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading binanceus: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'binanceusdm', 'OctoBot-Default-Tentacles'):
    try:
        from .binanceusdm import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading binanceusdm: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'binanceus_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .binanceus_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading binanceus_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'binance_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .binance_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading binance_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bitfinex', 'OctoBot-Default-Tentacles'):
    try:
        from .bitfinex import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bitfinex: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bitfinex_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .bitfinex_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bitfinex_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bitget', 'OctoBot-Default-Tentacles'):
    try:
        from .bitget import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bitget: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bitget_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .bitget_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bitget_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bithumb', 'OctoBot-Default-Tentacles'):
    try:
        from .bithumb import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bithumb: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bitmex', 'OctoBot-Default-Tentacles'):
    try:
        from .bitmex import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bitmex: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bitso', 'OctoBot-Default-Tentacles'):
    try:
        from .bitso import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bitso: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bitstamp', 'OctoBot-Default-Tentacles'):
    try:
        from .bitstamp import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bitstamp: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bittrex', 'OctoBot-Default-Tentacles'):
    try:
        from .bittrex import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bittrex: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bittrex_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .bittrex_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bittrex_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bybit', 'OctoBot-Default-Tentacles'):
    try:
        from .bybit import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bybit: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bybit_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .bybit_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bybit_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'coinbase_pro', 'OctoBot-Default-Tentacles'):
    try:
        from .coinbase_pro import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading coinbase_pro: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'coinbase_pro_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .coinbase_pro_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading coinbase_pro_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'coinex', 'OctoBot-Default-Tentacles'):
    try:
        from .coinex import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading coinex: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'gateio', 'OctoBot-Default-Tentacles'):
    try:
        from .gateio import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading gateio: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'gateio_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .gateio_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading gateio_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'hitbtc', 'OctoBot-Default-Tentacles'):
    try:
        from .hitbtc import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading hitbtc: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'hollaex', 'OctoBot-Default-Tentacles'):
    try:
        from .hollaex import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading hollaex: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'huobi', 'OctoBot-Default-Tentacles'):
    try:
        from .huobi import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading huobi: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'huobipro', 'OctoBot-Default-Tentacles'):
    try:
        from .huobipro import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading huobipro: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'huobipro_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .huobipro_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading huobipro_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'huobi_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .huobi_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading huobi_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'kraken', 'OctoBot-Default-Tentacles'):
    try:
        from .kraken import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading kraken: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'kraken_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .kraken_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading kraken_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'kucoin', 'OctoBot-Default-Tentacles'):
    try:
        from .kucoin import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading kucoin: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'kucoin_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .kucoin_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading kucoin_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'ndax', 'OctoBot-Default-Tentacles'):
    try:
        from .ndax import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading ndax: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'okcoin', 'OctoBot-Default-Tentacles'):
    try:
        from .okcoin import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading okcoin: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'okx', 'OctoBot-Default-Tentacles'):
    try:
        from .okx import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading okx: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'okx_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .okx_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading okx_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'phemex', 'OctoBot-Default-Tentacles'):
    try:
        from .phemex import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading phemex: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'phemex_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .phemex_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading phemex_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'poloniex', 'OctoBot-Default-Tentacles'):
    try:
        from .poloniex import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading poloniex: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'upbitexchange', 'OctoBot-Default-Tentacles'):
    try:
        from .upbitexchange import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading upbitexchange: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'wavesexchange', 'OctoBot-Default-Tentacles'):
    try:
        from .wavesexchange import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading wavesexchange: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'configurable_default_ccxt_rest', 'OctoBot-Default-Tentacles'):
    try:
        from .configurable_default_ccxt_rest import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading configurable_default_ccxt_rest: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('unknown_version', 'hollaex_websocket_feed', 'Unknown package location'):
    try:
        from .hollaex_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading hollaex_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'cryptocom', 'OctoBot-Default-Tentacles'):
    try:
        from .cryptocom import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading cryptocom: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'cryptocom_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .cryptocom_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading cryptocom_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'coinbase', 'OctoBot-Default-Tentacles'):
    try:
        from .coinbase import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading coinbase: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.0.0', 'yahoo_finance', 'Octane-Default-Tentacles'):
    try:
        from .yahoo_finance import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading yahoo_finance: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'hollaex_autofilled', 'OctoBot-Default-Tentacles'):
    try:
        from .hollaex_autofilled import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading hollaex_autofilled: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'hollaex_autofilled_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .hollaex_autofilled_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading hollaex_autofilled_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'mexc', 'OctoBot-Default-Tentacles'):
    try:
        from .mexc import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading mexc: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'mexc_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .mexc_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading mexc_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'coinex_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .coinex_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading coinex_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bingx', 'OctoBot-Default-Tentacles'):
    try:
        from .bingx import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bingx: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'htx', 'OctoBot-Default-Tentacles'):
    try:
        from .htx import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading htx: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'htx_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .htx_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading htx_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'bingx_websocket_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .bingx_websocket_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading bingx_websocket_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'yahoo_finance_autofilled', 'OctoBot-Default-Tentacles'):
    try:
        from .yahoo_finance_autofilled import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading yahoo_finance_autofilled: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
