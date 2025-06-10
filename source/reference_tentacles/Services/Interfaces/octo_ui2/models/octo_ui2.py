import functools
from flask_cors import cross_origin
import octobot_commons.os_util as os_util
import tentacles.Services.Interfaces.web_interface.login as login
import tentacles.Services.Interfaces.web_interface.flask_util.cors as cors_util


CORS_ENABLED = os_util.parse_boolean_environment_var("CORS_MODE_ENABLED", "False")
DEV_MODE_ENABLED = os_util.parse_boolean_environment_var(
    "API_DEV_MODE_ENABLED", "False"
)
SHARE_YOUR_OCOBOT = os_util.parse_boolean_environment_var("SHARE_YOUR_OCOBOT", "False")


def dev_mode_is_on():
    return DEV_MODE_ENABLED


def import_cross_origin_if_enabled(get_anyway: bool = False):
    if CORS_ENABLED or get_anyway:
        return cross_origin


def octane_route(
    blueprint,
    route: str,
    methods: list[str] = None,
    login_always_required: bool = False,
    can_be_shared_public: bool = False,
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        route_decorator = blueprint.route(route, methods=methods)
        if can_be_shared_public and SHARE_YOUR_OCOBOT:
            # no authentication
            return route_decorator(wrapper)
        if CORS_ENABLED:
            # cors and auth if enabled
            return route_decorator(cross_origin(origins="*")(wrapper))
        if login_always_required:
            if dev_mode_is_on():
                # force no login required
                return route_decorator(login.login_required_when_activated(wrapper))
            else:
                return route_decorator(login.active_login_required(wrapper))
        else:
            return route_decorator(login.login_required_when_activated(wrapper))

    return decorator
