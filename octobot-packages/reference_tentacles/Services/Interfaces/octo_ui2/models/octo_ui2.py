import octobot_commons.os_util as os_util
import tentacles.Services.Interfaces.web_interface.login as login


CORS_ENABLED = os_util.parse_boolean_environment_var("CORS_MODE_ENABLED", "False")
DEV_MODE_ENABLED = os_util.parse_boolean_environment_var(
    "API_DEV_MODE_ENABLED", "False"
)
SHARE_YOUR_OCOBOT = os_util.parse_boolean_environment_var("SHARE_YOUR_OCOBOT", "False")


def dev_mode_is_on():
    return DEV_MODE_ENABLED


def import_cross_origin_if_enabled():
    if CORS_ENABLED:
        from flask_cors import cross_origin

        return cross_origin


def create_env_dependent_route(
    plugin, route: str, route_method, can_be_shared=False, **kwargs
):
    cross_origin = import_cross_origin_if_enabled()
    if can_be_shared and SHARE_YOUR_OCOBOT:

        @plugin.route(route)
        @cross_origin(origins="*")
        def bot_info(**kwargs):
            return route_method(**kwargs)

    elif cross_origin:

        @plugin.route(route)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def bot_info(**kwargs):
            return route_method(**kwargs)

    else:

        @plugin.route(route)
        @login.login_required_when_activated
        def bot_info(**kwargs):
            return route_method(**kwargs)
