import typing
import flask
import octobot_tentacles_manager.loaders as loaders
import octobot_commons.enums as commons_enums
import tentacles.Services.Interfaces.web_interface.models as models

try:
    from tentacles.Meta.Keywords import block_factory
except (ModuleNotFoundError, ImportError):
    block_factory = None


CATEGORY_STRATEGY = "Strategy"
CATEGORY_TRADING_MODE = "Strategy Mode"
CATEGORY_LEGACY_STRATEGY = "Legacy Strategy"
CATEGORY_TA_EVALUATOR = "Technical Analysis Evaluator"
CATEGORY_SOCIAL_EVALUATOR = "Social Analysis Evaluator"
CATEGORY_REALTIME_EVALUATOR = "Realtime Analysis Evaluator"
CATEGORY_SCRIPTED_EVALUATOR = "Scripted Evaluator"
CATEGORY_EXCHANGE = "Exchange"
CATEGORY_AUTOMATION_ACTIONS = "Automation Action"
CATEGORY_AUTOMATION_CONDITIONS = "Automation Condition"
CATEGORY_AUTOMATION_TRIGGER_EVENTS = "Automation Event"
CATEGORY_EVALUATOR_UTIL = "Evaluator Util"
CATEGORY_LIBRARY = "Library"
CATEGORY_SERVICES_INTERFACES = "Interface"
CATEGORY_SERVICES_FEEDS = "Service Feed"
CATEGORY_SERVICES_BASES = "Service Base"
CATEGORY_SERVICES_NOTIFIERS = "Service Notifier"
CATEGORY_BACKTESTING_IMPORTERS = "Data Importer"
CATEGORY_BACKTESTING_CONVERTERS = "Data Converter"
CATEGORY_BACKTESTING_COLLECTORS = "Data Collector"
CATEGORY_EVALUATOR_BLOCK = "Evaluator Block"
CATEGORY_STRATEGY_BLOCK = "Strategy Block"
CATEGORY_ACTION_BLOCK = "Action Block"
CATEGORY_INDICATOR_BLOCK = "Indicator Block"
CATEGORY_KEY_TO_TITLE = {
    # "tentacles/Evaluator/Strategies": CATEGORY_LEGACY_STRATEGY,
    "tentacles/Trading/Mode": CATEGORY_TRADING_MODE,
    # "tentacles/Evaluator/TA": CATEGORY_TA_EVALUATOR,
    # "tentacles/Evaluator/Social": CATEGORY_SOCIAL_EVALUATOR,
    # "tentacles/Evaluator/RealTime": CATEGORY_REALTIME_EVALUATOR,
    # "tentacles/Evaluator/Scripted": CATEGORY_SCRIPTED_EVALUATOR,
    # "tentacles/Evaluator/Util": CATEGORY_EVALUATOR_UTIL,
    "tentacles/StrategyBlocks/EvaluatorBlock": CATEGORY_STRATEGY_BLOCK,
    "tentacles/StrategyBlocks/StrategyBlock": CATEGORY_STRATEGY_BLOCK,
    "tentacles/StrategyBlocks/ActionBlock": CATEGORY_STRATEGY_BLOCK,
    "tentacles/StrategyBlocks/IndicatorBlock": CATEGORY_STRATEGY_BLOCK,
    # "tentacles/Trading/Exchange": CATEGORY_EXCHANGE,
    # "tentacles/Automation/actions": CATEGORY_AUTOMATION_ACTIONS,
    # "tentacles/Automation/conditions": CATEGORY_AUTOMATION_CONDITIONS,
    # "tentacles/Automation/trigger_events": CATEGORY_AUTOMATION_TRIGGER_EVENTS,
    # "tentacles/Meta/Keywords": CATEGORY_LIBRARY,
    "tentacles/Services/Interfaces": CATEGORY_SERVICES_INTERFACES,
    # "tentacles/Services/Services_feeds": CATEGORY_SERVICES_FEEDS,
    # "tentacles/Services/Services_bases": CATEGORY_SERVICES_BASES,
    "tentacles/Services/Notifiers": CATEGORY_SERVICES_NOTIFIERS,
    # "tentacles/Backtesting/converters/exchanges": CATEGORY_BACKTESTING_CONVERTERS,
    # "tentacles/Backtesting/importers/exchanges": CATEGORY_BACKTESTING_IMPORTERS,
    # "tentacles/Backtesting/collectors/exchanges": CATEGORY_BACKTESTING_COLLECTORS,
}

DISTRO_UPDATED_PACKAGES = (
    "OctoBot-Default-Tentacles",
    "Octane-Default-Tentacles",
    "Octane-Pro-Tentacles-Keywords",
)
DISTRO_UPDATED_APPS = (
    "arbitrage_trading",
    "copy_trading",
    "daily_trading",
    "dip_analyser",
    "gpt_trading",
    "grid_trading",
    "default",
    "signal_trading",
    "simple_dca",
    "tradingview_trading",
    "staggered_orders_trading",
    "basic_tentacles",
    "LorentzianClassificationMode",
)


def get_installed_tentacles_modules_dict() -> dict:
    tentacles_info = {
        _tentacle.name: {
            "name": _tentacle.name,
            "in_dev_mode": _tentacle.in_dev_mode,
            "ARTIFACT_NAME": _tentacle.ARTIFACT_NAME,
            "metadata": _tentacle.metadata,
            "origin_package": _tentacle.origin_package,
            "origin_repository": _tentacle.origin_repository,
            "tentacle_class_names": _tentacle.tentacle_class_names,
            "tentacle_group": _tentacle.tentacle_group,
            "tentacle_module_path": _tentacle.tentacle_module_path,
            "tentacle_path": _tentacle.tentacle_path,
            "tentacle_root_path": _tentacle.tentacle_root_path,
            "tentacle_root_type": _tentacle.tentacle_root_type,
            # "tentacle_type": _tentacle.tentacle_type,
            "tentacles_requirements": _tentacle.tentacles_requirements,
            "version": _tentacle.version,
        }
        for _tentacle in loaders.get_tentacle_classes().values()
    }
    all_apps: dict = {}
    all_apps[CATEGORY_STRATEGY] = {}
    profiles = {
        profile.profile_id: profile.as_dict()
        for profile in models.get_profiles(commons_enums.ProfileType.LIVE).values()
    }
    current_profile = models.get_current_profile().as_dict()
    for profile_id, profile in profiles.items():
        app_dict = all_apps[CATEGORY_STRATEGY][profile_id] = convert_profile_into_app(
            current_profile, profile, profile_id
        )
    installed_blocks_info: typing.Optional[dict] = None
    if block_factory:
        (
            _,
            installed_blocks_info,
        ) = block_factory.BlockFactory.get_installed_blocks_by_type()
    for app_key, app in tentacles_info.items():
        category_title = CATEGORY_KEY_TO_TITLE.get(
            app["tentacle_path"].replace("\\", "/")
        )
        if category_title:
            if category_title not in all_apps:
                all_apps[category_title] = {}
            package_id = app["tentacle_class_names"][0]
            app_dict = all_apps[category_title][package_id] = {}
            app_dict["origin_package"] = app["origin_package"]
            app_dict["package_id"] = package_id
            app_dict["title"] = package_id
            app_dict["requirements"] = app["tentacles_requirements"]
            app_dict["is_installed"] = True
            app_dict["is_shared"] = False
            app_dict["tentacle_name"] = app_key
            app_dict["updated_by_distro"] = (
                app["origin_package"] in DISTRO_UPDATED_PACKAGES
                or package_id in DISTRO_UPDATED_APPS
            )
            app_dict["is_owner"] = not app_dict["updated_by_distro"]
            app_dict["categories"] = [category_title]
            tentacle_folder = app["tentacle_path"].split("/")[-1]
            if installed_blocks_info:
                block_info = installed_blocks_info.get(tentacle_folder, {}).get(
                    package_id
                )
                if block_info:
                    app_dict["title"] = block_info["title"]
                    app_dict["description"] = block_info["description"]

    if CATEGORY_TRADING_MODE not in all_apps:
        print(f"no trading mode found in installedTentaclesInfo ({tentacles_info})")
        all_apps[CATEGORY_TRADING_MODE] = {}

    missing_tentacles = set()
    media_url = flask.url_for("tentacle_media", _external=True)
    strategy_config: dict = models.get_strategy_config(media_url, missing_tentacles)
    for trading_mode_id, trading_mode in strategy_config["trading-modes"].items():
        user_app_data = all_apps[CATEGORY_TRADING_MODE].get(trading_mode_id, {})
        app_dict = all_apps[CATEGORY_TRADING_MODE][trading_mode_id] = {
            **trading_mode,
            **user_app_data,
        }
        app_dict["package_id"] = trading_mode_id
        app_dict["title"] = trading_mode_id
        app_dict["is_selected"] = trading_mode["activation"]
        app_dict["is_from_store"] = False
        # all_apps[cls.CATEGORY_TRADING_MODE][trading_mode_id]["tentacle_package_name"] = octobot_info['installedTentaclesInfo'][trading_mode_id]['origin_package']
        app_dict["is_installed"] = True
        app_dict["is_shared"] = False
        app_dict["is_owner"] = not app_dict.get("updated_by_distro")
        app_dict["categories"] = [CATEGORY_TRADING_MODE]
    # all_apps[CATEGORY_LEGACY_STRATEGY] = {}
    # for legacy_strategy_id, legacy_strategy in octobot_info["botInfo"][
    #     "strategy_config"
    # ]["strategies"].items():
    #     all_apps[CATEGORY_LEGACY_STRATEGY][legacy_strategy_id] = {
    #         "is_installed": True,
    #         "categories": [CATEGORY_LEGACY_STRATEGY],
    #     }
    #     # all_apps[legacy_strategy_id] = legacy_strategy
    return all_apps


def convert_profile_into_app(current_profile: dict, profile: dict, profile_id: str):
    updated_by_distro: bool = profile_id in DISTRO_UPDATED_APPS
    return {
        "package_id": profile_id,
        "origin_package": profile_id,
        "is_selected": (profile_id == current_profile["profile"]["id"]),
        "title": profile["profile"]["name"],
        "description": profile["profile"]["description"],
        "requirements": profile["profile"].get("required_trading_tentacles", []),
        "categories": [CATEGORY_STRATEGY],
        "avatar_url": profile["profile"]["avatar"],
        "updated_by_distro": updated_by_distro,
        "is_from_store": False,
        "is_installed": True,
        "is_shared": False,
        "is_owner": not updated_by_distro
        # all_apps[profile_id]["image_url"] =
    }
