from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('1.2.0', 'trends_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .trends_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading trends_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'forum_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .forum_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading forum_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'signal_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .signal_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading signal_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'news_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .news_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading news_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
