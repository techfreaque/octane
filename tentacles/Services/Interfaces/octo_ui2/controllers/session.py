import os
import json

from flask import request
import octobot_commons.constants as constants
import octobot_commons.json_util as json_util

import tentacles.Services.Interfaces.web_interface.login as login
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    dev_mode_is_on,
    import_cross_origin_if_enabled,
)
from tentacles.Services.Interfaces.octo_ui2.utils.basic_utils import (
    get_octo_ui_2_logger,
)


def register_semi_auto_trade_routes(plugin):
    route = "/session"
    methods = ["POST", "GET"]
    if cross_origin := import_cross_origin_if_enabled():
        if dev_mode_is_on():

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            def session_route():
                return _session_route()

        else:

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            @login.login_required_when_activated
            def session_route():
                return _session_route()

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def session_route():
            return _session_route()

    def _session_route():
        if request.method == "GET":
            return {}


class Session:
    tokens: dict = None

    def get_tokens(self) -> dict:
        if not self.tokens:
            self._load_saved_data()
        return self.tokens

    def _load_saved_data(self):
        self.tokens = {}
        read_data = {}
        try:
            read_data = json_util.read_file(self._get_file())
            self.tokens.update(read_data)
        except FileNotFoundError:
            pass
        except Exception as err:
            get_octo_ui_2_logger().exception(
                err, True, f"Unexpected error when reading saved session data: {err}"
            )
        if any(key not in read_data for key in self.tokens):
            # save fixed data
            self.dump_saved_data(self.tokens)

    def dump_saved_data(self, dump_data):
        try:
            with open(self._get_file(), "w") as sessions_file:
                return json.dump(dump_data, sessions_file)
        except Exception as err:
            get_octo_ui_2_logger().exception(
                err, True, f"Unexpected error when reading saved session data: {err}"
            )

    def _get_file(self):
        return os.path.join(
            constants.USER_FOLDER, f"{self.__class__.__name__}_data.json"
        )
