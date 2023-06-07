import octobot_tentacles_manager.configuration as configuration
import octobot_tentacles_manager.constants as constants
import octobot_tentacles_manager.util as util


def get_installation_context_octobot_version() -> dict:
    setup_config = configuration.TentaclesSetupConfiguration()
    available_tentacle = util.load_tentacle_with_metadata(constants.TENTACLES_PATH)
    setup_config.fill_tentacle_config(
        available_tentacle, constants.TENTACLE_CONFIG_FILE_NAME
    )
    return setup_config.installation_context
