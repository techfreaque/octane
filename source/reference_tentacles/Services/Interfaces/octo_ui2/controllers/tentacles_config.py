import flask
from flask import Response
import re
import os
import shutil

import octobot.constants as octobot_constants
import octobot_tentacles_manager.api as tentacles_manager_api
import octobot_tentacles_manager.constants as constants
import tentacles.Services.Interfaces.web_interface.login as login
import tentacles.Services.Interfaces.web_interface.util as util
import tentacles.Services.Interfaces.web_interface.models.tentacles as tentacles_models
import tentacles.Services.Interfaces.web_interface.models as models

import tentacles.Services.Interfaces.octo_ui2.models.config as config
import tentacles.Services.Interfaces.octo_ui2.utils.basic_utils as basic_utils
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import SHARE_YOUR_OCOBOT
from tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 import (
    import_cross_origin_if_enabled,
)
import tentacles.Services.Interfaces.octo_ui2.models.config as models_config


def register_tentacles_config_routes(plugin):
    route = "/tentacles_config"
    methods = ["POST"]

    cross_origin = import_cross_origin_if_enabled()
    if SHARE_YOUR_OCOBOT:
        _cross_origin = import_cross_origin_if_enabled(True)

        @plugin.blueprint.route(route, methods=methods)
        @_cross_origin(origins="*")
        def tentacles_config():
            return _tentacles_config()

    elif cross_origin:

        @plugin.blueprint.route(route, methods=methods)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def tentacles_config():
            return _tentacles_config()

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def tentacles_config():
            return _tentacles_config()

    def _tentacles_config():
        request_data = flask.request.get_json()
        tentacle_configs = {}
        error = ""
        for dirty_tentacle_name in request_data.get("tentacles", []):
            clean_tentacle_name = re.sub(
                r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", dirty_tentacle_name
            )
            try:
                this_tentacle = models.get_tentacle_config_and_edit_display(
                    clean_tentacle_name
                )
                tentacle_configs[clean_tentacle_name] = this_tentacle[
                    "displayed_elements"
                ]["data"]["elements"][0]
                if not tentacle_configs[clean_tentacle_name]["config"]:
                    tentacle_configs[clean_tentacle_name]["config"] = this_tentacle[
                        "config"
                    ]
            except IndexError:
                if clean_tentacle_name != "BlankTradingMode":
                    basic_utils.get_octo_ui_2_logger().error(
                        f"{clean_tentacle_name} doesnt seem to have a config"
                    )
            except Exception as error:
                basic_utils.get_octo_ui_2_logger().exception(
                    error, True, f"Failed to load config for {clean_tentacle_name}"
                )
        return basic_utils.get_response(
            success=True,
            data=tentacle_configs,
            message="Successfully fetched tentacles config",
        )

    route = "/update_profile_info"
    methods = ["POST"]
    if cross_origin := import_cross_origin_if_enabled():

        @plugin.blueprint.route(route, methods=methods)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def update_profiles_info():
            return _update_profiles_info()

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def update_profiles_info():
            return _update_profiles_info()

    def _update_profiles_info():
        data = flask.request.get_json()
        success, err = config.update_profile(flask.request.get_json()["id"], data)
        if not success:
            return util.get_rest_reply(flask.jsonify(str(err)), code=400)
        return util.get_rest_reply(flask.jsonify(data))

    route = "/update_profile/<action>"
    methods = ["GET", "POST"]
    if cross_origin := import_cross_origin_if_enabled():

        @plugin.blueprint.route(route, methods=methods)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def select_profile(action):
            return _select_profile(action)

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def select_profile(action):
            return _select_profile(action)

    def _select_profile(action):
        if action == "select":
            profile_id = flask.request.args.get("profile_id")
            models_config.select_profile(profile_id)
            return {
                "success": True,
                "message": "Profile successfully selected.",
            }
        if action == "duplicate":
            profile_id = flask.request.args.get("profile_id")
            request_data = flask.request.get_json()
            new_profile_name = request_data.get("new_profile_name")
            select_new_profile = request_data.get("select_new_profile")

            new_profile = models.duplicate_profile(profile_id)
            models_config.update_profile(
                new_profile.profile_id, {"name": new_profile_name}
            )
            if select_new_profile:
                models_config.select_profile(new_profile.profile_id)
                return {
                    "success": True,
                    "message": "Profile successfully duplicated & selected.",
                }

            return {
                "success": True,
                "message": "Profile successfully duplicated.",
            }

    route = "/export_tentacle/<package_name>"
    methods = ["GET"]
    if cross_origin := import_cross_origin_if_enabled():

        @plugin.blueprint.route(route, methods=methods)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def export_tentacle(package_name):
            return _export_tentacle(package_name)

    else:

        @plugin.blueprint.route(route, methods=methods)
        @login.login_required_when_activated
        def export_tentacle(package_name):
            return _export_tentacle(package_name)

    def _export_tentacle(package_name):
        root_dir = os.path.dirname(os.path.abspath(octobot_constants.OCTOBOT_FOLDER))
        export_path = os.path.join(root_dir, constants.DEFAULT_EXPORT_DIR)
        # clear first
        try:
            shutil.rmtree(export_path)
        except FileNotFoundError:
            pass
        success = tentacles_models.call_tentacle_manager(
            tentacles_manager_api.create_tentacles_package,
            package_name=package_name,
            output_dir=export_path,
            tentacles_folder=constants.TENTACLES_PATH,
            exported_tentacles_package=package_name,
            in_zip=True,
            with_dev_mode=False,
            cythonize=False,
            use_package_as_file_name=True,
        )
        if success:
            zip_name: str = f"{package_name}.zip"
            with open(os.path.join(export_path, zip_name), "rb") as f:
                data = f.readlines()
                shutil.rmtree(export_path)
                return Response(
                    data,
                    headers={
                        "Content-Type": "application/zip",
                        "Content-Disposition": "attachment; filename=%s;" % zip_name,
                    },
                )
        raise RuntimeError("Failed to export tentacle package")


# create_tentacles_package
# package_name: str,
#                                    tentacles_folder: str = constants.TENTACLES_PATH,
#                                    output_dir: str = constants.DEFAULT_EXPORT_DIR,
#                                    exported_tentacles_package: str = None,
#                                    uploader_type: str = enums.UploaderTypes.S3.value,
#                                    in_zip: bool = True,
#                                    with_dev_mode: bool = False,
#                                    use_package_as_file_name: bool = False,
#                                    upload_details: list = None,
#                                    metadata_file: str = None,
#                                    cythonize: bool = False
