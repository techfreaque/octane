from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version("1.0.0", "all_in_one_orders", "Octane-Default-Tentacles"):
    try:
        from .all_in_one_orders import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading all_in_one_orders: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("1.0.0", "send_alert", "Octane-Default-Tentacles"):
    try:
        from .send_alert import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading send_alert: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version('1.0.0', 'all_in_one_orders', 'Octane-Default-Tentacles'):
    try:
        from .all_in_one_orders import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading all_in_one_orders: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.0.0', 'send_alert', 'Octane-Default-Tentacles'):
    try:
        from .send_alert import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading send_alert: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.0.0', 'exit_trades', 'Octane-Default-Tentacles'):
    try:
        from .exit_trades import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading exit_trades: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
