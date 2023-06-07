# pylint: disable=W0718
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
import json
import jsonschema
import octobot_commons.logging


LOGGER_NAME = "json_util"


def validate(config, schema_file) -> None:
    """
    Validate a config file, raise upon validation error
    :param config: the config
    :param schema_file: the config schema
    :return: None
    """
    with open(schema_file) as json_schema:
        loaded_schema = json.load(json_schema)
    jsonschema.validate(instance=config, schema=loaded_schema)


def read_file(
    file_path: str,
    raise_errors: bool = True,
    on_error_value: dict = None,
    open_mode="r",
) -> dict:
    """
    Read a load the given file with json.load()
    :param file_path: file to read
    :param raise_errors: when True will forward errors. Will just log errors otherwise
    :param on_error_value: return this value when raise_errors is False and an error occurs
    :param open_mode: the file open mode to give to open()
    :return: the parsed file or default value on error if possible
    """
    try:
        with open(file_path, open_mode) as open_file:
            return json.load(open_file)
    except PermissionError as err:
        if raise_errors:
            raise
        octobot_commons.logging.get_logger(LOGGER_NAME).error(
            f"Permission error when reading {file_path} file: {err}."
        )
    except Exception as err:
        if raise_errors:
            raise
        octobot_commons.logging.get_logger(LOGGER_NAME).exception(
            f"Unexpected error when reading {file_path} file: {err}."
        )
    if on_error_value is None:
        raise ValueError("on_error_value is unset")
    return on_error_value
