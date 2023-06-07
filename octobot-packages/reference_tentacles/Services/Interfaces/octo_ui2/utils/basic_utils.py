import octobot_commons.logging as bot_logging


def get_octo_ui_2_logger(_=None):
    return bot_logging.get_logger("OctoUi2Plugin")


def get_response(success=True, data=None, message=None):
    respones = {"success": success}
    if data:
        respones["data"] = data
    if message:
        respones["message"] = message
    return respones
