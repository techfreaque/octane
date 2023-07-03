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

import typing
import octobot_trading.modes.script_keywords.basic_keywords as basic_keywords
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.pro_tentacles.indicators.supported_indicators as supported_indicators
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 as user_inputs2
import octobot_commons.enums as commons_enums

# required
import tentacles.Meta.Keywords.pro_tentacles.indicators as indicators_module


class Indicator:
    def __init__(self):
        self.indicator_id = 0
        self.value_key = commons_enums.CacheDatabaseColumns.VALUE.value
        self.is_evaluator = True
        self.indicator_class_name = "none"
        self.indicator_name = "none"
        self.config_name = "none"
        self.config_path = "none"
        self.candle_source = None
        self.trigger = True
        self.enable_volume = True
        self.cache_path = "none"
        self.config_path_short = "none"
        self.chart_location = "none"
        self.shared_cache_path = None
        self.indicators: dict = {}
        self.time_frame: str = None
        self.plot: bool = (None,)

    async def init_indicator(
        self,
        maker,
        evaluator,
        data_source_name="Data Source",
        def_val="EMA",
        indicator_id=1,
        enable_oscillators=True,
        enable_price_indicators=True,
        enable_price_data=True,
        enable_volume=True,
        enable_multi_data_indicators=False,
        enable_static_value=True,
        enable_force_def_val=False,
        supports_shared_sources: bool = True,
        parent_input_name: str = None,
    ):
        self.indicator_id = indicator_id
        self.enable_volume = enable_volume
        if enable_force_def_val:
            self.indicator_name = def_val
        else:
            available_sources = supported_indicators.get_supported_indicators_(
                enable_oscillators=enable_oscillators,
                enable_price_indicators=enable_price_indicators,
                enable_static_value=enable_static_value,
                enable_price_data=enable_price_data,
                enable_multi_data_indicators=enable_multi_data_indicators,
            )
            self.indicator_name = await user_inputs2.user_input2(
                maker,
                evaluator,
                f"select_{data_source_name}",
                "options",
                def_val=def_val,
                title=f"Select {data_source_name}",
                options=available_sources,
            )
        self.config_path = (
            evaluator.config_path + f"/Indicator {indicator_id} - {data_source_name}"
        )
        self.cache_path = (
            evaluator.cache_path + f"/Indicator {indicator_id} - {data_source_name}"
        )
        self.config_path_short = (
            parent_input_name or f"{evaluator.config_path_short}-i{indicator_id}"
        )
        await self.get_shared_indicator_config(
            maker,
            evaluator,
            data_source_name,
            supports_shared_sources,
            parent_input_name=parent_input_name,
        )

    async def get_shared_indicator_config(
        self,
        maker,
        parent_evaluator,
        data_source_name,
        supports_shared_sources: bool,
        parent_input_name: typing.Optional[str] = None,
    ):
        supported_indicators.get_supported_indicator_config(self)
        sources_list, sources_available = maker.get_supported_shared_conf_indicators(
            self
        )
        # TODO add again with better usability
        # if sources_available and supports_shared_sources:
        #     new_evaluator_id = await user_inputs2.user_input2(
        #         maker,
        #         parent_evaluator,
        #         f"use_{data_source_name}_{self.indicator_name}_config_from",
        #         "options",
        #         def_val="this indicator",
        #         title=f"use {data_source_name}-{self.indicator_name} config from",
        #         show_in_summary=False,
        #         options=sources_list,
        #         parent_input_name=parent_input_name or self.config_path_short,
        #     )
        # else:
        new_evaluator_id = sources_list[0]
        self.trigger = False
        if new_evaluator_id == "this indicator":
            if not parent_input_name:
                await basic_keywords.user_input(
                    maker.ctx,
                    self.config_path_short,
                    "object",
                    def_val=None,
                    title=f"{self.indicator_name} - {data_source_name} {self.indicator_id}",
                    parent_input_name=parent_evaluator.config_path_short,
                    editor_options={
                        commons_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
                        commons_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
                        commons_enums.UserInputEditorOptionsTypes.GRID_COLUMNS.value: 12,
                    },
                )
            available_timeframes = [
                timeframe.value
                for timeframe in maker.ctx.exchange_manager.exchange_config.get_relevant_time_frames()
            ]
            if len(available_timeframes) > 1:
                available_timeframes.insert(0, matrix_enums.CURRENT_TIME_FRAME)
                self.time_frame = await user_inputs2.user_input2(
                    maker,
                    parent_evaluator,
                    f"select_time_frame_for_{data_source_name}",
                    "options",
                    def_val=matrix_enums.CURRENT_TIME_FRAME,
                    title=f"Select the time frame for {data_source_name}",
                    options=available_timeframes,
                    parent_input_name=parent_input_name or self.config_path_short,
                )
                if self.time_frame == matrix_enums.CURRENT_TIME_FRAME:
                    self.time_frame = maker.ctx.time_frame
                elif (
                    commons_enums.TimeFramesMinutes[
                        commons_enums.TimeFrames(self.time_frame)
                    ]
                    < commons_enums.TimeFramesMinutes[
                        commons_enums.TimeFrames(maker.ctx.time_frame)
                    ]
                ):
                    raise NotImplementedError(
                        "Not able to set a smaller timeframe for indicator"
                        f" ({data_source_name}) as the trigger timeframe"
                    )
            else:
                self.time_frame = maker.ctx.time_frame

            self.chart_location = "sub-chart"
            self.trigger = True
        else:
            self.shared_cache_path = new_evaluator_id

    async def get_indicator_data(self, maker, evaluator):
        cache_path = self.shared_cache_path or self.cache_path
        indicator: Indicator = maker.indicators[cache_path]
        try:
            return (
                indicator.data[self.value_key]["data"],
                indicator.data[self.value_key]["chart_location"],
                indicator.data[self.value_key]["title"],
            )
        except (KeyError, AttributeError):
            maker.current_indicator_time_frame = indicator.time_frame
            if self.indicator_name == "current price":
                self.indicator_name = "price_data"
            try:
                m_time = utilities.start_measure_time()
                await eval(
                    f"indicators_module.get_{indicator.indicator_class_name}"
                    "(maker, self, evaluator)"
                )
                utilities.end_measure_live_time(
                    maker.ctx,
                    m_time,
                    f" strategy maker - calculating {indicator.indicator_class_name}",
                    min_duration=9,
                )
            except Exception as error:
                message = (
                    f"Indicator {indicator.indicator_class_name} "
                    f"failed to compute data. error: {error}"
                )
                if maker.debug_mode:
                    maker.ctx.logger.exception(
                        error,
                        True,
                        message,
                    )
                else:
                    maker.ctx.logger.error(message)
                maker.current_indicator_time_frame = None
                return [], "", ""
            maker.current_indicator_time_frame = None
            return (
                indicator.data[indicator.value_key]["data"],
                indicator.data[indicator.value_key]["chart_location"],
                indicator.data[indicator.value_key]["title"],
            )
