from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('1.2.0', 'ai_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .ai_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading ai_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'volatility_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .volatility_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading volatility_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'trend_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .trend_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading trend_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'momentum_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .momentum_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading momentum_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
