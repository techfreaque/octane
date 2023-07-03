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

import octobot_commons.enums as commons_enums

from tentacles.Meta.Keywords.pro_tentacles import (
    evaluators as evaluators,
)  # needed for evaluators
from octobot_trading.modes.script_keywords.basic_keywords import user_inputs


class Evaluator_:
    def __init__(
        self,
        maker,
        input_name_root,
        input_path_short_root="",
        supported_evaluators=None,
    ):
        if supported_evaluators is None:
            supported_evaluators = []
        self.evaluator_id = 0
        self.name = ""
        self.class_name = ""
        self.enabled = True
        self.supported_evaluators = supported_evaluators
        self.plot = False
        self.candle_source = "none"
        self.indicators = {}

        self.input_parent_name_root = input_name_root
        self.input_path_short_root = input_path_short_root
        self.base_config_path_short: str = None

        self.config_name = "none"
        self.config_path = ""
        self.cache_path = ""
        self.config_path_short = ""
        self.value_key = "v"
        self.values = []
        self.second_values = None
        self.second_signals = None
        self.signals = []
        self.data = {}

    async def evaluate_and_get_data(self, maker, ctx):
        if self.enabled:
            try:
                self.data = await eval(f"evaluators.get_{self.class_name}(maker, self)")
            except Exception as error:
                evaluator_error_message(self, ctx, maker, error)
                return []

            if not self.data[self.value_key] and self.data[self.value_key] != 0:
                evaluator_error_message(self, ctx, maker)
                return []
            return self.data[self.value_key]

    def init_paths(self, maker):
        self.config_path = (
            f"{self.input_parent_name_root}/Evaluator "
            f"{self.evaluator_id} - {self.name}"
        )
        self.cache_path = (
            f"Strategy {maker.current_strategy_id + 1}/Evaluator "
            f"{self.evaluator_id} - {self.name}"
        )
        self.config_path_short = f"{self.input_path_short_root}-e{self.evaluator_id}"
        self.base_config_path_short = self.config_path_short + "base"

    async def init_evaluator(self, maker, ctx, evaluator_id, use_compact_mode=False):
        self.evaluator_id = (
            evaluator_id + 1 if isinstance(evaluator_id, int) else evaluator_id
        )
        if use_compact_mode:
            self.enabled = True
            self.config_path_short = self.input_path_short_root
        else:
            self.init_paths(maker)

            await user_inputs.user_input(
                ctx,
                self.base_config_path_short,
                "object",
                def_val=None,
                title=f"Evaluator {self.evaluator_id}",
                parent_input_name=self.input_path_short_root,
                editor_options={
                    commons_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
                    commons_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
                    commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
                },
            )
            self.enabled = await user_inputs.user_input(
                ctx,
                f"{self.input_path_short_root}_enable_"
                f"evaluator_{self.evaluator_id}",
                "boolean",
                def_val=True,
                title=f"Enable evaluator {self.evaluator_id}",
                parent_input_name=self.base_config_path_short,
                order=101,
            )
            if self.enabled:
                self.class_name = self.name = await user_inputs.user_input(
                    ctx,
                    (
                        f"{self.input_path_short_root}_select_"
                        f"evaluator_{self.evaluator_id}"
                    ),
                    "options",
                    def_val="is_rising",
                    title=f"Select evaluator {self.evaluator_id}",
                    options=self.supported_evaluators,
                    parent_input_name=self.base_config_path_short,
                    order=99,
                )
                await user_inputs.user_input(
                    ctx,
                    self.config_path_short,
                    "object",
                    def_val=None,
                    title=f"Evaluator {self.evaluator_id}",
                    parent_input_name=self.base_config_path_short,
                    editor_options={
                        commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
                    },
                )


def evaluator_error_message(evaluator, ctx, maker, error=None):
    message = (
        f"Strategy Maker: Evaluator has no data {evaluator.evaluator_id} "
        f"{evaluator.name} {evaluator.class_name}: there is probably an issue in your"
        " config. Check the settings."
    )
    if error:
        message += "Error: " + str(error)
    if error and maker.debug_mode:
        ctx.logger.exception(error, True, message)
    else:
        ctx.logger.error(message)
