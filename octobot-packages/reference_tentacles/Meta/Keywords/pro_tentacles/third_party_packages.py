# a42.ch CONFIDENTIAL
# __________________
#
#  [2021] - [∞] a42.ch Incorporated
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of a42.ch Incorporated and its suppliers,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to a42.ch Incorporated
# and its suppliers and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from a42.ch Incorporated.
#
# If you want to use any code for commercial purposes,
# or you want your own custom solution,
# please contact me at max@a42.ch

import subprocess
import sys
import typing

import octobot_services.interfaces.util as interfaces_util


PACKAGE_NAME = "package_name"
PYTHON_39_PACKAGE_NAME = "python_39_package_name"
REQUIRED_PACKAGES = [
    {PACKAGE_NAME: "pandas"},
    {PACKAGE_NAME: "pandas_ta"},
    {PACKAGE_NAME: "finta"},
    {PACKAGE_NAME: "tulipy", PYTHON_39_PACKAGE_NAME: "newtulipy"},
    {PACKAGE_NAME: "statistics"},
    {PACKAGE_NAME: "scikit-neuralnetwork"},
    {PACKAGE_NAME: "tensorflow"},
]


class MissingThirdPartyPackageError(Exception):
    pass


def raise_missing_third_party_package_missing_error(module_name, error):
    raise MissingThirdPartyPackageError(
        f"failed to install {module_name} - "
        "install it manually to use Matrix-Pro-Tentacles"
    ) from error


def install_missing_packages(required_packages: typing.List[typing.Dict[str, str]]):
    try:
        package_name = ""
        for package in required_packages:
            package_name = package[PACKAGE_NAME]
            if sys.version_info >= (3, 8):
                package_name = package.get(PYTHON_39_PACKAGE_NAME, package_name)
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    package_name,
                ]
            )
        interfaces_util.get_bot_api().restart_bot()
    except Exception as error:
        raise_missing_third_party_package_missing_error(package_name, error)


try:
    import pandas as _
    import pandas_ta as _
    import finta as _
    import tulipy as _
    import statistics as _
    import sklearn as _
    import tensorflow as _
except (ImportError, ModuleNotFoundError):
    install_missing_packages(REQUIRED_PACKAGES)
