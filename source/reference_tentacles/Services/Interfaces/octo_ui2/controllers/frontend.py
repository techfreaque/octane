# from flask_cors import cross_origin
import tentacles.Services.Interfaces.web_interface.login as login
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import SHARE_YOUR_OCOBOT
import os
from flask import send_from_directory
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    import_cross_origin_if_enabled,
)


def register_frontend_route(plugin):
    route = "/<url_path>"
    cross_origin = import_cross_origin_if_enabled()
    if SHARE_YOUR_OCOBOT:
        _cross_origin = import_cross_origin_if_enabled(True)

        @plugin.blueprint.route(route)
        @_cross_origin(origins="*")
        def any_page(url_path=None):
            return _home(url_path)

    elif cross_origin:

        @plugin.blueprint.route(route)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def any_page(url_path=None):
            return _home(url_path)

    else:

        @plugin.blueprint.route(route)
        @login.login_required_when_activated
        def any_page(url_path=None):
            return _home(url_path)

    route = "/home"
    if SHARE_YOUR_OCOBOT:
        _cross_origin = import_cross_origin_if_enabled(True)

        @plugin.blueprint.route(route)
        @_cross_origin(origins="*")
        def home(url_path=None):
            return _home(url_path)

    elif cross_origin:

        @plugin.blueprint.route(route)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def home(url_path=None):
            return _home(url_path)

    else:

        @plugin.blueprint.route(route)
        @login.login_required_when_activated
        def home(url_path=None):
            return _home(url_path)

    def _home(url_path):
        os_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
        return send_from_directory(os.path.join(os_path, "static"), "index.html")
