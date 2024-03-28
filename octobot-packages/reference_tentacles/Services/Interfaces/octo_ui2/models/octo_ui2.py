import functools
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
        from flask_cors import cross_origin

        return cross_origin


def octane_route(
    blueprint,
    route: str,
    methods: list[str] = None,
    login_always_required: bool = False,
    can_be_shared_public: bool = False,
):
    def decorator(func):
        @blueprint.route(route, methods=methods)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if cross_origin := import_cross_origin_if_enabled():
                return cross_origin(
                    origins=cors_util.get_user_defined_cors_allowed_origins()
                )(login.login_required_when_activated(func))(*args, **kwargs)
            elif login_always_required:
                if dev_mode_is_on():
                    return login.login_required_when_activated(func)(*args, **kwargs)
                else:
                    return login.active_login_required(func)(*args, **kwargs)
            else:
                if can_be_shared_public and SHARE_YOUR_OCOBOT:
                    return func(*args, **kwargs)
                return login.login_required_when_activated(func)(*args, **kwargs)

        return wrapper

    return decorator
