from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('1.2.0', 'google_service_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .google_service_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading google_service_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'reddit_service_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .reddit_service_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading reddit_service_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'telegram_api_service_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .telegram_api_service_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading telegram_api_service_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'telegram_service_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .telegram_service_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading telegram_service_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'trading_view_service_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .trading_view_service_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading trading_view_service_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'twitter_service_feed', 'OctoBot-Default-Tentacles'):
    try:
        from .twitter_service_feed import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading twitter_service_feed: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
