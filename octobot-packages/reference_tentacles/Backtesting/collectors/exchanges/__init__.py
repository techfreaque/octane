from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('1.2.0', 'exchange_bot_snapshot_data_collector', 'OctoBot-Default-Tentacles'):
    try:
        from .exchange_bot_snapshot_data_collector import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading exchange_bot_snapshot_data_collector: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'exchange_history_collector', 'OctoBot-Default-Tentacles'):
    try:
        from .exchange_history_collector import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading exchange_history_collector: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'exchange_live_collector', 'OctoBot-Default-Tentacles'):
    try:
        from .exchange_live_collector import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading exchange_live_collector: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
