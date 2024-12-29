import flask

import tentacles.Services.Interfaces.web_interface.login as login
import tentacles.Services.Interfaces.web_interface.util as util
from tentacles.Services.Interfaces.octo_ui2.models import config
from tentacles.Services.Interfaces.octo_ui2.utils import basic_utils
from tentacles.Services.Interfaces.octo_ui2_pro import octo_ui2_pro_plugin
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    import_cross_origin_if_enabled,
)


def register_pro_config_routes(plugin):
    route = "/pro_config"
    methods = ["GET", "POST"]
    if cross_origin := import_cross_origin_if_enabled():

        @plugin.blueprint.route(route, methods=methods)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def ui_config():
            return _ui_config()

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def ui_config():
            return _ui_config()

    def _ui_config():
        if flask.request.method == "POST":
            try:
                request_data = flask.request.get_json()
                return util.get_rest_reply(
                    flask.jsonify(
                        config.save_ui_config(
                            request_data,
                            octo_ui2_pro_plugin.O_UI_Pro,
                            keep_existing=True,
                        ),
                    )
                )
            except Exception as e:
                basic_utils.get_octo_ui_2_logger().exception(e)
                return util.get_rest_reply(str(e), 500)
        else:
            return config.get_ui_config(octo_ui2_pro_plugin.O_UI_Pro)
