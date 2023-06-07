# pylint: disable=W0613, W0703, W0719
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
import shutil
import os
import json
import octobot_commons.logging as logging
import octobot_commons.constants as commons_constants
import octobot_commons.configuration.fields_utils as fields_utils
import octobot_commons.json_util as json_util


LOGGER_NAME = "ConfigFileManager"


def get_user_config() -> str:
    """
    Return user config path
    :return: user config path
    """
    return os.path.join(commons_constants.USER_FOLDER, commons_constants.CONFIG_FILE)


def load(config_file, should_raise=True, fill_missing_fields=False) -> dict:
    """
    Load a config from a config_file
    :param config_file: the config file path
    :param should_raise: if error should be raised
    :param fill_missing_fields: if missing fields should be filled
    :return: the loaded config
    """
    logger = logging.get_logger(LOGGER_NAME)
    basic_error = "Error when load config file {0}".format(config_file)
    try:
        config = json_util.read_file(config_file)
        return config
    except ValueError as value_error:
        error_str = f"{basic_error} : json decoding failed ({value_error})"
        if should_raise:
            raise Exception(error_str)
        logger.error(error_str)
    except IOError as io_error:
        error_str = f"{basic_error} : file opening failed ({io_error})"
        if should_raise:
            raise Exception(error_str)
        logger.error(error_str)
    except Exception as global_exception:
        error_str = f"{basic_error} : {global_exception}"
        if should_raise:
            raise Exception(error_str)
        logger.error(error_str)
    return None


def dump(
    config_file,
    config,
    temp_restore_config_file=commons_constants.TEMP_RESTORE_CONFIG_FILE,
    schema_file=None,
) -> None:
    """
    Save a json config
    :param config_file: the config file path
    :param config: the json config
    :param temp_restore_config_file: the temporary config file
    :param schema_file: path to the json schema to validate the updated config
    """
    try:
        # prepare a restoration config file
        prepare_restore_file(temp_restore_config_file, config_file)

    # when failing to create the restore config
    except Exception as err:
        error_details = (
            f"Failed to create the backup configuration file. Is your {commons_constants.USER_FOLDER} "
            f"folder accessible ? : {err} ({err.__class__.__name__})"
        )
        logging.get_logger(LOGGER_NAME).error(error_details)
        raise err.__class__(error_details) from err
    try:
        new_content = jsonify_config(config)

        # edit the config file
        with open(config_file, "w") as cg_file:
            cg_file.write(new_content)

        if schema_file is not None:
            # check if the new config file is correct
            check_config(config_file, schema_file)

        # remove temp file
        remove_restore_file(temp_restore_config_file)

    # when failing to restore the previous config
    except Exception as global_exception:
        logging.get_logger(LOGGER_NAME).error(
            f"Save config failed : {global_exception}"
        )
        restore(temp_restore_config_file, config_file)
        raise global_exception


def check_config(config_file, schema_file) -> None:
    """
    Check a config file
    :param config_file: the config file path
    :param schema_file: path to the json schema to validate the updated config
    """
    try:
        json_util.validate(load(config_file=config_file), schema_file=schema_file)
    except Exception as global_exception:
        raise global_exception


def jsonify_config(config) -> str:
    """
    Jsonify a config
    :param config: the config
    :return: the jsonified config
    """
    # check exchange keys encryption
    for exchange, exchange_config in config[commons_constants.CONFIG_EXCHANGES].items():
        try:
            for key in commons_constants.CONFIG_EXCHANGE_ENCRYPTED_VALUES:
                handle_encrypted_value(key, exchange_config)
        except Exception:
            config[commons_constants.CONFIG_EXCHANGES][exchange] = {
                key: "" for key in commons_constants.CONFIG_EXCHANGE_ENCRYPTED_VALUES
            }

    return dump_formatted_json(config)


def handle_encrypted_value(value_key, config_element, verbose=False) -> bool:
    """
    Handle encrypted value
    :param value_key: the value key
    :param config_element: the config element
    :param verbose: if verbosity is enabled
    :return: True if the value can be decrypted
    """
    if value_key in config_element:
        key = config_element[value_key]
        if not fields_utils.has_invalid_default_config_value(key):
            try:
                fields_utils.decrypt(key, silent_on_invalid_token=True)
                return True
            except Exception:
                config_element[value_key] = fields_utils.encrypt(key).decode()
                if verbose:
                    logging.get_logger(LOGGER_NAME).warning(
                        f"Non encrypted secret info found in config ({value_key}): replaced "
                        f"value with encrypted equivalent."
                    )
                return False
    return True


def prepare_restore_file(restore_file, current_config_file) -> None:
    """
    Prepare a config restoration file
    :param restore_file: the restoration file
    :param current_config_file: the file to be restored
    """
    shutil.copy(current_config_file, restore_file)


def remove_restore_file(restore_file) -> None:
    """
    Remove a restore file
    :param restore_file: the restore file path
    """
    os.remove(restore_file)


def restore(restore_file, target_file) -> None:
    """
    Restore a config file from a saved file
    :param restore_file: the restore file path
    :param target_file: the target file path
    """
    shutil.copy(restore_file, target_file)


def dump_formatted_json(json_data) -> str:
    """
    The dumped json data
    :param json_data: the json data to be dumped
    :return: the dumped json data
    """
    return json.dumps(json_data, indent=4, sort_keys=True)
