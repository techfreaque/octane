#  Drakkar-Software OctoBot-Interfaces
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import flask

import octobot_commons.logging as bot_logging
import octobot.constants as constants
import octobot.disclaimer as disclaimer
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    import_cross_origin_if_enabled,
)
import tentacles.Services.Interfaces.web_interface as web_interface
import tentacles.Services.Interfaces.web_interface.login as login
import tentacles.Services.Interfaces.web_interface.models as models

logger = bot_logging.get_logger("ServerInstance Controller")


@web_interface.server_instance.route("/about")
@login.login_required_when_activated
def about():
    return flask.render_template('about.html',
                                 octobot_beta_program_form_url=constants.OCTOBOT_BETA_PROGRAM_FORM_URL,
                                 beta_env_enabled_in_config=models.get_beta_env_enabled_in_config(),
                                 metrics_enabled=models.get_metrics_enabled(),
                                 disclaimer=disclaimer.DISCLAIMER)


route = "/commands/<cmd>"
methods = ["POST", "GET"]
if cross_origin := import_cross_origin_if_enabled():

    @web_interface.server_instance.route(route, methods=methods)
    @cross_origin(origins="*")
    @login.login_required_when_activated
    def commands(cmd=None):
        return _commands(cmd)

else:

    @web_interface.server_instance.route(route, methods=methods)
    @login.login_required_when_activated
    def commands(cmd=None):
        return _commands(cmd)


def _commands(cmd=None):
    if cmd == "restart":
        models.schedule_delayed_command(models.restart_bot, delay=0.1)
        return flask.jsonify("Success")

    elif cmd == "stop":
        models.schedule_delayed_command(models.stop_bot, delay=0.1)
        return flask.jsonify("Success")

    elif cmd == "update":
        models.schedule_delayed_command(models.update_bot, delay=0.1)
        return flask.jsonify("Update started")

    else:
        raise RuntimeError("Unknown command")
