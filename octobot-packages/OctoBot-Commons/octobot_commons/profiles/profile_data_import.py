# pylint: disable=R0913,W0718,W0706,C0415
#  Drakkar-Software OctoBot-Commons
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import os
import uuid

import octobot_commons.profiles.profile_data as profile_data_import
import octobot_commons.logging as bot_logging
import octobot_commons.json_util as json_util
import octobot_commons.constants as constants
import octobot_commons.aiohttp_util as aiohttp_util
import octobot_commons.enums as enums

IMPORTED_AVATAR = "avatar"
IMPORTED_PROFILES_DEFAULT_EXTRA_BACKTESTING_TIMEFRAME = (
    enums.TimeFrames.FIFTEEN_MINUTES.value
)


async def convert_profile_data_to_profile_directory(
    profile_data: profile_data_import.ProfileData,
    description: str,
    risk: enums.ProfileRisk,
    avatar_url: str,
    output_path: str,
    aiohttp_session,
):
    """
    Creates a profile folder from the given ProfileData
    :param profile_data: path to the profile zipped archive
    :param description: profile description
    :param risk: profile risk
    :param avatar_url: profile avatar_url
    :param output_path: profile folder path
    :param aiohttp_session: session to use
    """
    logger = bot_logging.get_logger(__name__)
    if os.path.exists(output_path):
        raise OSError(f"{output_path} already exists")
    os.mkdir(output_path)
    profile = _get_profile(profile_data, description, risk, output_path)
    # tentacles_config.json
    tentacles_setup_config = _get_tentacles_setup_config(profile_data, output_path)
    tentacles_setup_config.save_config()
    # specific_config
    _save_specific_config(profile_data, output_path)
    # avatar file
    try:
        await _download_and_set_avatar(
            profile, avatar_url, output_path, aiohttp_session
        )
    except Exception as err:
        logger.exception(err, True, f"Error when downloading profile avatar: {err}")
    # finish with profile.json to include edits from previous methods
    profile.save()


def _get_profile(
    profile_data: profile_data_import.ProfileData,
    description: str,
    risk: enums.ProfileRisk,
    output_path: str,
):
    profile = profile_data.to_profile(output_path)
    # use trading simulator by default
    profile.config[constants.CONFIG_TRADER][constants.CONFIG_ENABLED_OPTION] = False
    profile.config[constants.CONFIG_SIMULATOR][constants.CONFIG_ENABLED_OPTION] = True
    profile.description = description
    profile.risk = risk
    profile.profile_id = str(uuid.uuid4().hex)
    profile.read_only = True
    profile.extra_backtesting_time_frames = [
        IMPORTED_PROFILES_DEFAULT_EXTRA_BACKTESTING_TIMEFRAME
    ]
    return profile


def _get_tentacles_setup_config(
    profile_data: profile_data_import.ProfileData, output_path: str
):
    try:
        import octobot_tentacles_manager.api

        classes = [
            octobot_tentacles_manager.api.get_tentacle_class_from_string(
                tentacle_data.name
            ).get_name()
            for tentacle_data in profile_data.tentacles
        ]
        config_path = os.path.join(output_path, constants.CONFIG_TENTACLES_FILE)
        tentacles_setup_config = (
            octobot_tentacles_manager.api.create_tentacles_setup_config_with_tentacles(
                *classes, config_path=config_path
            )
        )
        octobot_tentacles_manager.api.fill_with_installed_tentacles(
            tentacles_setup_config
        )
        return tentacles_setup_config
    except ImportError:
        raise


def _save_specific_config(
    profile_data: profile_data_import.ProfileData, output_path: str
):
    try:
        import octobot_tentacles_manager.constants

        specific_config_dir = os.path.join(
            output_path,
            octobot_tentacles_manager.constants.TENTACLES_SPECIFIC_CONFIG_FOLDER,
        )
        os.mkdir(specific_config_dir)
        for tentacle_config in profile_data.tentacles:
            json_util.safe_dump(
                tentacle_config.config,
                os.path.join(
                    specific_config_dir,
                    f"{tentacle_config.name}{octobot_tentacles_manager.constants.CONFIG_EXT}",
                ),
            )
    except ImportError:
        raise


async def _download_and_set_avatar(
    profile, avatar_url, output_path: str, aiohttp_session
):
    profile.avatar = _get_avatar_name(avatar_url)
    try:
        import aiofiles

        async with aiofiles.open(
            os.path.join(output_path, profile.avatar), "wb+"
        ) as downloaded_file:
            await aiohttp_util.download_stream_file(
                downloaded_file,
                avatar_url,
                aiohttp_session,
                is_aiofiles_output_file=True,
            )
    except ImportError:
        raise


def _get_avatar_name(avatar_url: str):
    # remove params and get file name with ext
    return avatar_url.split("?")[0].split("/")[-1]
