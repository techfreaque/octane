import octobot_commons.os_util as os_util
import tentacles.Services.Interfaces.web_interface.login as login


CORS_ENABLED = os_util.parse_boolean_environment_var("CORS_MODE_ENABLED", "False")
DEV_MODE_ENABLED = os_util.parse_boolean_environment_var(
    "API_DEV_MODE_ENABLED", "False"
)
SHARE_YOUR_OCOBOT = os_util.parse_boolean_environment_var("SHARE_YOUR_OCOBOT", "False")


def dev_mode_is_on():
    return DEV_MODE_ENABLED


def import_cross_origin_if_enabled(get_anyway: bool = False):
    if CORS_ENABLED or get_anyway:
        from flask_cors import cross_origin

        return cross_origin


def create_env_dependent_route(
    plugin, route: str, route_method, can_be_shared=False, **kwargs
):
    cross_origin = import_cross_origin_if_enabled()
    __func_name__ = f"_{route_method.__name__}"
    if can_be_shared and SHARE_YOUR_OCOBOT:
        _cross_origin = import_cross_origin_if_enabled(True)

        @plugin.route(route)
        @_cross_origin(origins="*")
        def __func_name__(**kwargs):
            return route_method(**kwargs)

    elif cross_origin:

        @plugin.route(route)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def __func_name__(**kwargs):
            return route_method(**kwargs)

    else:

        @plugin.route(route)
        @login.login_required_when_activated
        def __func_name__(**kwargs):
            return route_method(**kwargs)
