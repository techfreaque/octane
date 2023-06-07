from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('1.0.0', 'entry_limit_order', 'Matrix-Strategy-Blocks'):
    try:
        from .entry_limit_order import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading entry_limit_order: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.0.0', 'percent_take_profit_order', 'Matrix-Strategy-Blocks'):
    try:
        from .percent_take_profit_order import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading percent_take_profit_order: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.0.0', 'static_stop_loss_order', 'Matrix-Strategy-Blocks'):
    try:
        from .static_stop_loss_order import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading static_stop_loss_order: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.0.0', 'send_alert', 'Matrix-Strategy-Blocks'):
    try:
        from .send_alert import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading send_alert: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
