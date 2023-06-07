#  Drakkar-Software OctoBot-Tentacles-Manager
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
import typing
import octobot_commons.logging.logging_util as logging_util


class DebuggingReporter:
    REPORT_TITLE: str = "Debugging Report"
    THIS_WILL_HELP_US_WITH_MESSAGE: str = "This will help us to fix your issue"
    ERROR_TITLE_MESSAGE: str = "OctoBot detected the following issues:"
    debugging_report_dict: dict = {}

    def __init__(self, logger):
        self.logger: logging_util.BotLogger = logger

    def add_to_debugging_report(
        self,
        key_to_set: str,
        error_description: str,
        additional_message: str = "",
        error=None,
        method=None,
    ) -> None:
        method_message: str = (
            f"with method: {type(method).__name__}\n" if method else ""
        )
        additional_message: str = (
            f"{additional_message}\n" if additional_message else ""
        )
        message: str = (
            f"> Error with: {key_to_set} - error description: {error_description}\n"
            f"{additional_message}"
            f"{method_message}{' - Error: '+repr(error) if error else ''}\n"
        )
        self._add_to_debugging_report(key_to_set, message)

    def _add_to_debugging_report(
        self,
        key_to_set,
        message,
    ) -> None:
        if key_to_set in self.debugging_report_dict:
            self.debugging_report_dict[key_to_set].append(message)
        else:
            self.debugging_report_dict[key_to_set] = [message]

    def create_debugging_report(self) -> None:
        if self.debugging_report_dict:
            (
                attributes_with_all_errors,
                attributes_with_errors,
            ) = self.remove_duplicated_errors_and_format()

            self._finalize_debugging_report(
                f"Attributes with errors: {attributes_with_errors}\n"
                "\n"
                # f"Used exchange: {self.exchange}\n\n"  # todo add exchange name
                f"Debugging report: \n"
                "\n"
                f"{attributes_with_all_errors}\n"
            )

    def _finalize_debugging_report(self, report) -> None:
        self.clear_reporter()
        self.logger.error(self.debugging_report_main_template(report))
        raise NotImplementedError

    def clear_reporter(self):
        self.debugging_report_dict = {}

    def remove_duplicated_errors_and_format(self) -> typing.Tuple[str, str]:
        attributes_with_all_errors: str = ""
        attributes_with_errors: str = ""
        for (
            attribute_name,
            error_messages_list,
        ) in self.debugging_report_dict.items():
            for index in range(len(error_messages_list)):
                if not error_messages_list[index] in error_messages_list[:index]:
                    attributes_with_all_errors += error_messages_list[index]
            attributes_with_errors += f"{attribute_name}, "
        return attributes_with_all_errors, attributes_with_errors

    def debugging_report_main_template(self, report) -> str:
        return (
            f"\n!!!!!!!!!!!!  DEBUGGING REPORT {self.REPORT_TITLE.upper()} START  !!!!!!!!!!!!\n"
            "\n"
            f"Post this report into OctoBot discord -> bug_report\n"
            "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"
            f"{self.THIS_WILL_HELP_US_WITH_MESSAGE}\n"
            "\n"
            f"{self.ERROR_TITLE_MESSAGE}\n"
            f"{report}"
            "\n"
            f"!!!!!!!!!!!!  DEBUGGING REPORT {self.REPORT_TITLE.upper()} END  !!!!!!!!!!!!"
        )
