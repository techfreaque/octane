from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('1.2.0', 'signal_trading_mode', 'OctoBot-Default-Tentacles'):
    try:
        from .signal_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading signal_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'grid_trading_mode', 'OctoBot-Default-Tentacles'):
    try:
        from .grid_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading grid_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'staggered_orders_trading_mode', 'OctoBot-Default-Tentacles'):
    try:
        from .staggered_orders_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading staggered_orders_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'daily_trading_mode', 'OctoBot-Default-Tentacles'):
    try:
        from .daily_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading daily_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'arbitrage_trading_mode', 'OctoBot-Default-Tentacles'):
    try:
        from .arbitrage_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading arbitrage_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'dip_analyser_trading_mode', 'OctoBot-Default-Tentacles'):
    try:
        from .dip_analyser_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading dip_analyser_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'trading_view_signals_trading_mode', 'OctoBot-Default-Tentacles'):
    try:
        from .trading_view_signals_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading trading_view_signals_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'remote_trading_signals_trading_mode', 'OctoBot-Default-Tentacles'):
    try:
        from .remote_trading_signals_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading remote_trading_signals_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'dca_trading_mode', 'OctoBot-Default-Tentacles'):
    try:
        from .dca_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading dca_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('0.7.3', 'arbitrage_pro_trading_mode', 'Matrix-Pro-Tentacles'):
    try:
        from .arbitrage_pro_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading arbitrage_pro_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.3.0', 'lorentzian_classification', 'Octane-Default-Tentacles'):
    try:
        from .lorentzian_classification import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading lorentzian_classification: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'blank_trading_mode', 'OctoBot-Default-Tentacles'):
    try:
        from .blank_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading blank_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'scripted_trading_mode', 'OctoBot-Private-Tentacles'):
    try:
        from .scripted_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading scripted_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.7.0', 'strategy_maker_trading_mode', 'Matrix-Pro-Tentacles'):
    try:
        from .strategy_maker_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading strategy_maker_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('0.8.6', 'spot_master_3000_trading_mode', 'Octane-Default-Tentacles'):
    try:
        from .spot_master_3000_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading spot_master_3000_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.0.2', 'semi_auto_trading_mode', 'Semi-Auto-Trading-Mode'):
    try:
        from .semi_auto_trading_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading semi_auto_trading_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.0.0', 'strategy_flow_maker_mode', 'Octane-Strategy-Blocks'):
    try:
        from .strategy_flow_maker_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading strategy_flow_maker_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
