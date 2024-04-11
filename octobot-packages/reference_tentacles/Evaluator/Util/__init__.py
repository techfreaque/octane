from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('1.2.0', 'candles_util', 'OctoBot-Default-Tentacles'):
    try:
        from .candles_util import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading candles_util: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'overall_state_analysis', 'OctoBot-Default-Tentacles'):
    try:
        from .overall_state_analysis import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading overall_state_analysis: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'pattern_analysis', 'OctoBot-Default-Tentacles'):
    try:
        from .pattern_analysis import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading pattern_analysis: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'statistics_analysis', 'OctoBot-Default-Tentacles'):
    try:
        from .statistics_analysis import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading statistics_analysis: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'text_analysis', 'OctoBot-Default-Tentacles'):
    try:
        from .text_analysis import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading text_analysis: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'trend_analysis', 'OctoBot-Default-Tentacles'):
    try:
        from .trend_analysis import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading trend_analysis: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
