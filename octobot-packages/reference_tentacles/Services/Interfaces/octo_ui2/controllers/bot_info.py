import asyncio
import os
import time
import flask
import flask_login

import octobot_commons.time_frame_manager as time_frame_manager
import octobot_commons
import octobot_commons.optimization_campaign as optimization_campaign
import octobot_commons.enums as commons_enums
import octobot_commons.symbols.symbol_util as symbol_util
import octobot_services.interfaces as interfaces
import octobot_services.interfaces.util as interfaces_util
import tentacles.Services.Interfaces.octo_ui2.models.neural_net_helper as neural_net_helper
import tentacles.Services.Interfaces.octo_ui2.models.bot_info_models as bot_info_models
import tentacles.Services.Interfaces.web_interface as web_interface

import tentacles.Services.Interfaces.octo_ui2.utils.basic_utils as basic_utils
import tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 as octo_ui2
import tentacles.Services.Interfaces.web_interface.login as login
import tentacles.Services.Interfaces.web_interface.models as models

try:
    import tentacles.Services.Interfaces.octo_ui2_pro.octo_ui2_pro_plugin as octo_ui2_pro_plugin
except (ImportError, ModuleNotFoundError):
    octo_ui2_pro_plugin = None

TIME_TO_START = 100


def register_bot_info_routes(plugin):
    @octo_ui2.octane_route(
        plugin.blueprint, route="/bot-info/<exchange>", can_be_shared_public=True
    )
    def _bot_info(exchange=None, try_counter=0):
        exchange = (
            exchange if (exchange != "null" and exchange != "undefined") else None
        )
        is_starting = False
        try_counter += 1
        trading_mode_name = None
        exchange_name = None
        evaluator_names = []
        exchange_id = None
        available_api_actions = None
        installed_blocks_info = None
        symbols = traded_time_frames = activated_evaluators = []
        available_time_frames = []
        strategy_names = []
        trigger_time_frames = None
        real_time_strategies_active: bool = False
        missing_tentacles = set()
        ui_pro_installed: str = True if octo_ui2_pro_plugin is not None else False
        profiles = {
            profile.profile_id: profile.as_dict()
            for profile in models.get_profiles(commons_enums.ProfileType.LIVE).values()
        }
        media_url = flask.url_for("tentacle_media", _external=True)
        strategy_config: dict = models.get_strategy_config(media_url, missing_tentacles)
        symbols = models.get_enabled_trading_pairs()

        activated_evaluators = models.get_config_activated_evaluators()
        evaluator_names = [
            activated_evaluator.get_name()
            for activated_evaluator in activated_evaluators
        ]
        strategies = models.get_config_activated_strategies()
        if strategies:
            strategy_names = [strategy.get_name() for strategy in strategies]
        available_time_frames = [
            time_frame.value
            for time_frame in time_frame_manager.sort_time_frames(
                [_time_frame.value for _time_frame in commons_enums.TimeFrames]
            )
        ]
        activated_trading_mode = models.get_config_activated_trading_mode()
        trading_mode_name: str = activated_trading_mode.get_name()
        should_stop_training: bool = neural_net_helper.SHOULD_STOP_TRAINING
        any_neural_net_active: bool = neural_net_helper.ANY_NEURAL_NET_ACTIVE
        (
            any_exchange_is_futures,
            exchange_names,
            exchange_ids,
            ids_by_exchange_name,
        ) = bot_info_models.get_multi_exchange_info()
        try:
            (
                exchange_name,
                exchange_id,
                traded_time_frames,
                trigger_time_frames,
                exchange_manager,
            ) = bot_info_models.get_current_exchange_info(exchange_name, exchange_names)
            (
                installed_blocks_info,
                available_api_actions,
                real_time_strategies_active,
            ) = bot_info_models.get_trading_mode_info(exchange_manager)
        except bot_info_models.NoSingleExchangeDataException:
            if activated_trading_mode is None:
                basic_utils.get_octo_ui_2_logger().error(
                    "No trading/strategy mode is activated. Please activate at least one trading/strategy mode."
                )
            elif not models.get_active_exchanges():
                basic_utils.get_octo_ui_2_logger().error(
                    "No exchange is activated. Please activate at least one exchange."
                )
            else:
                is_starting = True
                running_seconds = (
                    time.time() - interfaces.get_bot_api().get_start_time()
                )
                if running_seconds < TIME_TO_START:
                    interfaces_util.run_in_bot_async_executor(asyncio.sleep(2))
                    return _bot_info(exchange=exchange, try_counter=try_counter)
                basic_utils.get_octo_ui_2_logger().error(
                    "Failed to exchange info - Seems like there is an issue with your exchange or exchange settings",
                )
        return {
            "success": True,
            "message": "Successfully fetched bot base data",
            "data": {
                "is_starting": is_starting,
                "trading_mode_name": trading_mode_name,
                "exchange_id": exchange_id,
                "live_id": 1,  # todo
                "exchange_name": exchange_name,
                "exchange_names": exchange_names,
                "exchange_ids": exchange_ids,
                "current_profile": models.get_current_profile().as_dict(),
                "ids_by_exchange_name": ids_by_exchange_name,
                "symbols": sorted(
                    [
                        symbol_util.convert_symbol(
                            s, octobot_commons.MARKET_SEPARATOR, "|"
                        )
                        for s in symbols
                    ]
                ),
                "ui_pro_installed": ui_pro_installed,
                "installed_blocks_info": installed_blocks_info,
                "should_stop_training": should_stop_training,
                "any_neural_net_active": any_neural_net_active,
                "profiles": profiles,
                "can_logout": flask_login.current_user.is_authenticated,
                "is_owner": not octo_ui2.SHARE_YOUR_OCOBOT
                or (
                    octo_ui2.SHARE_YOUR_OCOBOT
                    and flask_login.current_user.is_authenticated
                ),
                "any_exchange_is_futures": any_exchange_is_futures,
                "evaluator_names": evaluator_names,
                "time_frames": available_time_frames,
                # "enabled_time_frames": enabled_time_frames,
                "traded_time_frames": traded_time_frames,
                "trigger_time_frames": trigger_time_frames,
                "strategy_names": strategy_names,
                "optimization_campaign": optimization_campaign.OptimizationCampaign.get_campaign_name(),
                # "activated_evaluators": activated_evaluators,
                # "activated_strategy": activated_strategy,
                # "config_candles_count": config_candles_count,
                "strategy_config": strategy_config,
                "real_time_strategies_active": real_time_strategies_active,
                "available_api_actions": available_api_actions,
                "data_files": models.get_data_files_with_description(),
                "octobot_project": interfaces.AbstractInterface.project_name,
                "octobot_version": interfaces.AbstractInterface.project_version,
            },
        }

    route = "/logout"
    if cross_origin := octo_ui2.import_cross_origin_if_enabled():

        @plugin.blueprint.route(route)
        @cross_origin(origins="*")
        @flask_login.login_required
        def logout():
            return _logout()

    else:

        @plugin.blueprint.route(route)
        @flask_login.login_required
        def logout():
            return _logout()

    def _logout():
        flask_login.logout_user()
        return basic_utils.get_response(
            message="Successfully logged out",
        )

    route = "/profile_media/<path:path>"
    cross_origin = octo_ui2.import_cross_origin_if_enabled()
    if octo_ui2.SHARE_YOUR_OCOBOT:
        _cross_origin = octo_ui2.import_cross_origin_if_enabled(True)

        @plugin.blueprint.route(route)
        @_cross_origin(origins="*")
        def profile_media(path):
            return _profile_media(path)

    elif cross_origin:

        @plugin.blueprint.route(route)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def profile_media(path):
            return _profile_media(path)

    else:

        @plugin.blueprint.route(route)
        @login.login_required_when_activated
        def profile_media(path):
            return _profile_media(path)

    def _profile_media(path):
        # images
        if models.is_valid_profile_image_path(path):
            # reference point is the web interface directory:
            #   use OctoBot root folder as a reference
            return _send_file("../../../..", path)
        # use default profile image
        basic_utils.get_octo_ui_2_logger().error(
            f"Failed to get profile image, path {path} not found"
        )
        return _send_file("../../../..", "daily_trading")

    def _send_file(base_dir, file_path):
        base_path, file_name = os.path.split(file_path)
        return flask.send_from_directory(os.path.join(base_dir, base_path), file_name)

    route = "/logs"
    if cross_origin := octo_ui2.import_cross_origin_if_enabled():

        @plugin.blueprint.route(route)
        @cross_origin(origins="*")
        @login.login_required_when_activated
        def logs():
            return _logs()

    else:

        @plugin.blueprint.route(route)
        @login.login_required_when_activated
        def logs():
            return _logs()

    def _logs():
        web_interface.flush_errors_count()
        return basic_utils.get_response(
            message="Successfully fetched logs",
            data=web_interface.get_logs()
            or {
                1: {
                    "Level": "INFO",
                    "Source": "The logs are empty",
                    "Message": "",
                    "Time": "",
                }
            },
        )
