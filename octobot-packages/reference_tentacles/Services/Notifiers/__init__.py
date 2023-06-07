from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('1.2.0', 'telegram_notifier', 'OctoBot-Default-Tentacles'):
    try:
        from .telegram_notifier import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading telegram_notifier: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'twitter_notifier', 'OctoBot-Default-Tentacles'):
    try:
        from .twitter_notifier import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading twitter_notifier: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'web_notifier', 'OctoBot-Default-Tentacles'):
    try:
        from .web_notifier import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading web_notifier: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
