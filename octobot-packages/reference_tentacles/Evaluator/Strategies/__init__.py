from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('1.2.0', 'mixed_strategies_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .mixed_strategies_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading mixed_strategies_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'blank_strategy_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .blank_strategy_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading blank_strategy_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.4.0', 'time_frame_strategy_evaluator', 'Octane-Default-Tentacles'):
    try:
        from .time_frame_strategy_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading time_frame_strategy_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'move_signals_strategy_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .move_signals_strategy_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading move_signals_strategy_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'dip_analyser_strategy_evaluator', 'OctoBot-Default-Tentacles'):
    try:
        from .dip_analyser_strategy_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading dip_analyser_strategy_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.0.0', 'real_time_strategy_evaluator', 'Matrix-Pro-Tentacles'):
    try:
        from .real_time_strategy_evaluator import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading real_time_strategy_evaluator: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
