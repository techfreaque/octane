import os
import flask

import octobot_commons.authentication as authentication
import octobot_commons.profiles as profiles
import octobot_commons.constants as constants

import octobot_commons.profiles.profile_sharing as profile_sharing
import octobot_services.interfaces.util as interfaces_util

import tentacles.Services.Interfaces.web_interface.util as util
import tentacles.Services.Interfaces.web_interface.models as models
import tentacles.Services.Interfaces.web_interface.login as login

import tentacles.Services.Interfaces.octo_ui2.models.app_store_models as app_store_models
import tentacles.Services.Interfaces.octo_ui2.utils.basic_utils as basic_utils
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    SHARE_YOUR_OCOBOT,
    import_cross_origin_if_enabled,
    dev_mode_is_on,
)


def register_appstore_routes(plugin):
    route = "/tentacles-info"
    cross_origin = import_cross_origin_if_enabled()
    if SHARE_YOUR_OCOBOT:
        _cross_origin = import_cross_origin_if_enabled(True)

        @plugin.blueprint.route(route)
        @_cross_origin(origins="*")
        def app_store():
            return _app_store()

    elif cross_origin:
        if dev_mode_is_on:

            @plugin.blueprint.route(route)
            @cross_origin(origins="*")
            def app_store():
                return _app_store()

        else:

            @plugin.blueprint.route(route)
            @cross_origin(origins="*")
            @login.login_required_when_activated
            def app_store():
                return _app_store()

    else:

        @plugin.blueprint.route(route)
        @login.login_required_when_activated
        def app_store():
            return _app_store()

    def _app_store():
        return {
            "success": True,
            "message": "Successfully fetched installed tentacles data",
            "data": app_store_models.get_installed_tentacles_modules_dict(),
        }

    tentacles_package_route = "/tentacle_packages"
    methods = ["POST"]
    if cross_origin := import_cross_origin_if_enabled():
        if dev_mode_is_on():

            @plugin.blueprint.route(tentacles_package_route, methods=methods)
            @login.login_required_when_activated
            @cross_origin(origins="*")
            def tentacle_packages():
                return _tentacle_packages()

        else:

            @plugin.blueprint.route(tentacles_package_route, methods=methods)
            @login.login_required_when_activated
            @cross_origin(origins="*")
            def tentacle_packages():
                return _tentacle_packages()

    else:

        @plugin.blueprint.route(tentacles_package_route, methods=methods)
        @login.login_required_when_activated
        def tentacle_packages():
            return _tentacle_packages()

    def _tentacle_packages():
        if flask.request.method == "POST":
            update_type = flask.request.args["update_type"]
            return _handle_tentacles_pages_post(update_type)

    route = "/profiles/<command>"
    methods = ["POST"]
    if cross_origin := import_cross_origin_if_enabled():
        if dev_mode_is_on:

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            def profiles_route(command):
                return _profiles_route(command)

        else:

            @plugin.blueprint.route(route, methods=methods)
            @cross_origin(origins="*")
            @login.login_required_when_activated
            def profiles_route(command):
                return _profiles_route(command)

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def profiles_route(command):
            return _profiles_route(command)

    def _profiles_route(command):
        if command == "import":
            request_data = flask.request.get_json()
            try:
                name = request_data["name"]
                url = request_data["url"]
                file_path = profiles.download_profile(url, name.replace(" ", "_"))
                temp_profile_name = profile_sharing._get_profile_name(name, file_path)
                profile = profile_sharing.install_profile(
                    import_path=file_path,
                    profile_name=temp_profile_name,
                    bot_install_path=".",
                    replace_if_exists=True,
                    is_imported=False,
                    origin_url=url,
                    profile_schema=constants.PROFILE_FILE_SCHEMA,
                )
                if profile.name != temp_profile_name:
                    profile.rename_folder(
                        profile_sharing._get_unique_profile_folder_from_name(
                            profile
                        ).replace(" ", "_"),
                        False,
                    )
                interfaces_util.get_edited_config(dict_only=False).load_profiles()
                if os.path.isfile(file_path):
                    os.remove(file_path)
                return basic_utils.get_response(
                    success=True,
                    message=f"{profile.name} profile successfully imported.",
                )
            except FileNotFoundError:
                return basic_utils.get_response(
                    success=False,
                    message=f"Invalid profile url {url}",
                )
            except Exception as error:
                basic_utils.get_octo_ui_2_logger().exception(
                    error, True, f"Error when importing Strategy: {error}"
                )
                return basic_utils.get_response(
                    success=False,
                    message=f"Error when importing profile: {error}",
                )
        return basic_utils.get_response(
            success=False,
            message="No command provided",
        )


# class TentacleInstallAuthenticator(authentication.Authenticator):
#     AUTHORIZATION_HEADER = "Authorization"
#     _authenticated_session: aiohttp.ClientSession = None

#     def add_authentication_token(self, password_token):
#         self.password_token = password_token

#     @abc.abstractmethod
#     def is_logged_in(self):
#         """
#         :return: True when authenticated
#         """
#         return True if self.password_token else False

#     @abc.abstractmethod
#     def logout(self):
#         self._authenticated_session.close()

#     @abc.abstractmethod
#     def get_aiohttp_session(self):
#         if self.password_token:
#             self._authenticated_session = aiohttp.ClientSession(
#                 headers={self.AUTHORIZATION_HEADER: f"token {self.password_token}"}
#             )
#             return self._authenticated_session
#         return None

#     @abc.abstractmethod
#     def must_be_authenticated_through_authenticator(self):
#         """
#         :return: True when this authenticator has to be validated
#         """
#         return True


def _handle_package_operation(update_type):
    if update_type == "add_package":
        request_data = flask.request.get_json()
        success = False
        if request_data:
            version = None
            url_key = "url"
            if url_key in request_data:
                path_or_url = request_data[url_key]
                version = request_data.get("version", None)
                action = "register_and_install"
            else:
                path_or_url, action = next(iter(request_data.items()))
                path_or_url = path_or_url.strip()
            if action == "register_and_install":
                authenticator = authentication.Authenticator.instance()
                installation_result = models.install_packages(
                    path_or_url, version, authenticator=authenticator
                )
                if installation_result:
                    return util.get_rest_reply(flask.jsonify(installation_result))
                else:
                    return util.get_rest_reply(
                        "Impossible to install the given tentacles package. "
                        "Please see logs for more details.",
                        500,
                    )

        if not success:
            return util.get_rest_reply('{"operation": "ko"}', 500)
    elif update_type in ["install_packages", "update_packages", "reset_packages"]:
        packages_operation_result = {}
        if update_type == "install_packages":
            packages_operation_result = models.install_packages()
        elif update_type == "update_packages":
            packages_operation_result = models.update_packages()
        elif update_type == "reset_packages":
            packages_operation_result = models.reset_packages()

        if packages_operation_result:
            return util.get_rest_reply(flask.jsonify(packages_operation_result))
        else:
            action = update_type.split("_")[0]
            return util.get_rest_reply(
                f"Impossible to {action} packages, check the logs for more information.",
                500,
            )


def _handle_module_operation(update_type):
    request_data = flask.request.get_json()
    if request_data:
        packages_operation_result = {}
        if update_type == "update_modules":
            packages_operation_result = models.update_modules(request_data)
        elif update_type == "uninstall_modules":
            packages_operation_result = models.uninstall_modules(request_data)

        if packages_operation_result is not None:
            return util.get_rest_reply(flask.jsonify(packages_operation_result))
        else:
            action = update_type.split("_")[0]
            return util.get_rest_reply(
                f"Impossible to {action} module(s), check the logs for more information.",
                500,
            )
    else:
        return util.get_rest_reply(
            '{"Need at least one element be selected": "ko"}', 500
        )


def _handle_tentacles_pages_post(update_type):
    if update_type in [
        "add_package",
        "install_packages",
        "update_packages",
        "reset_packages",
    ]:
        return _handle_package_operation(update_type)

    elif update_type in ["update_modules", "uninstall_modules"]:
        return _handle_module_operation(update_type)
