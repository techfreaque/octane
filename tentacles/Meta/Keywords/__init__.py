from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version('1.0.0', 'block_factory', 'Matrix-Strategy-Blocks'):
    try:
        from .block_factory import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading block_factory: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.2.0', 'scripting_library', 'OctoBot-Default-Tentacles'):
    try:
        from .scripting_library import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading scripting_library: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.1.0', 'basic_tentacles', 'Matrix-Basic-Tentacles'):
    try:
        from .basic_tentacles import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading basic_tentacles: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.1.0', 'pro_tentacles', 'Matrix-Pro-Tentacles'):
    try:
        from .pro_tentacles import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading pro_tentacles: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.1.0', 'RunAnalysis', 'Matrix-O-UI'):
    try:
        from .RunAnalysis import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading RunAnalysis: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')

if check_tentacle_version('1.0.0', 'indicator_keywords', 'Matrix-Strategy-Blocks'):
    try:
        from .indicator_keywords import *
    except Exception as e:
        get_logger('TentacleLoader').error(f'Error when loading indicator_keywords: '
                                           f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
                                           f'error persists, try reinstalling your tentacles via '
                                           f'"python start.py tentacles --install --all".')
