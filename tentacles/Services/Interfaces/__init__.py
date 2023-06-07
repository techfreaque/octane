from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('1.2.0', 'telegram_bot_interface', 'OctoBot-Default-Tentacles'):
    try:
        from .telegram_bot_interface import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading telegram_bot_interface: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'web_interface', 'OctoBot-Default-Tentacles'):
    try:
        from .web_interface import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading web_interface: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('0.6.2', 'run_analysis_mode', 'Matrix-O-UI'):
    try:
        from .run_analysis_mode import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading run_analysis_mode: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('0.9.8', 'octo_ui2_pro', 'Matrix-O-UI-Pro'):
    try:
        from .octo_ui2_pro import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading octo_ui2_pro: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('0.9.20', 'octo_ui2', 'Matrix-O-UI'):
    try:
        from .octo_ui2 import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading octo_ui2: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
