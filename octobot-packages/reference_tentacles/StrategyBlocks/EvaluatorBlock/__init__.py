from octobot_tentacles_manager.api.inspector import check_tentacle_version
from octobot_commons.logging.logging_util import get_logger

if check_tentacle_version("0.9.52", "data_does_three_peaks", "Matrix-Strategy-Blocks"):
    try:
        from .data_does_three_peaks import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_does_three_peaks: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "data_is_moving", "Matrix-Strategy-Blocks"):
    try:
        from .data_is_moving import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_is_moving: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "neural_net_classification", "Matrix-Strategy-Blocks"
):
    try:
        from .neural_net_classification import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading neural_net_classification: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "data_is_the_same_as_data", "Matrix-Strategy-Blocks"
):
    try:
        from .data_is_the_same_as_data import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_is_the_same_as_data: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "time_signals", "Matrix-Strategy-Blocks"):
    try:
        from .time_signals import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading time_signals: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "data_was_not_below_data", "Matrix-Strategy-Blocks"
):
    try:
        from .data_was_not_below_data import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_was_not_below_data: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "data_was_not_above_data", "Matrix-Strategy-Blocks"
):
    try:
        from .data_was_not_above_data import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_was_not_above_data: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version(
    "0.9.52", "divergence_between_data", "Matrix-Strategy-Blocks"
):
    try:
        from .divergence_between_data import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading divergence_between_data: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "data_is_rising", "Matrix-Strategy-Blocks"):
    try:
        from .data_is_rising import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_is_rising: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "data_was_below_data", "Matrix-Strategy-Blocks"):
    try:
        from .data_was_below_data import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_was_below_data: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "data_is_falling", "Matrix-Strategy-Blocks"):
    try:
        from .data_is_falling import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_is_falling: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "data_is_below_data", "Matrix-Strategy-Blocks"):
    try:
        from .data_is_below_data import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_is_below_data: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "data_is_above_data", "Matrix-Strategy-Blocks"):
    try:
        from .data_is_above_data import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_is_above_data: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "data_is_crossing_data", "Matrix-Strategy-Blocks"):
    try:
        from .data_is_crossing_data import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_is_crossing_data: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )

if check_tentacle_version("0.9.52", "data_was_above_data", "Matrix-Strategy-Blocks"):
    try:
        from .data_was_above_data import *
    except Exception as e:
        get_logger("TentacleLoader").error(
            f"Error when loading data_was_above_data: "
            f'{e.__class__.__name__}{f" ({e})" if f"{e}" else ""}. If this '
            f"error persists, try reinstalling your tentacles via "
            f'"python start.py tentacles --install --all".'
        )
