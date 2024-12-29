import os
import octobot_commons.logging as logging
import octobot_tentacles_manager.api as tentacles_manager_api
import octobot_services.interfaces.util as interfaces_util
import tentacles.Services.Interfaces.web_interface.plugins as plugins


from .controllers import optimizer_controller, configs


class O_UI_Pro(plugins.AbstractWebInterfacePlugin):
    NAME = "octo_ui2_pro"
    PLUGIN_ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))
    logger: logging.BotLogger = logging.get_logger("OctoUi2ProPlugin")

    def register_routes(self):
        optimizer_controller.register_optimizer_routes(self)
        configs.register_pro_config_routes(self)

    def get_tabs(self):
        return []

    @classmethod
    def get_ui_config(
        cls,
    ):
        return tentacles_manager_api.get_tentacle_config(
            interfaces_util.get_edited_tentacles_config(), cls
        )
