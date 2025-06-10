from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('0.9.52', 'candle_strategy', 'Matrix-Strategy-Blocks'):
    try:
        from .candle_strategy import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading candle_strategy: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('0.9.52', 'trading_view_webhook_strategy', 'Matrix-Strategy-Blocks'):
    try:
        from .trading_view_webhook_strategy import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading trading_view_webhook_strategy: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('0.9.52', 'real_time_strategy', 'Octane-Default-Tentacles'):
    try:
        from .real_time_strategy import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading real_time_strategy: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
