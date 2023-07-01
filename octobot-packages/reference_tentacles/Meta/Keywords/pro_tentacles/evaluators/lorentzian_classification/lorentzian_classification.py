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
import numpy
import octobot_commons.enums as common_enums
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.ml_utils.classification_functions.classification_utils as classification_utils
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.ml_utils.utils as utils
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.ml_utils.classification_functions.downsampling as downsampling
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as basic_utilities

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)
from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
    user_select_candle_source_name,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_evaluator_data,
    allow_enable_plot,
)
from tentacles.Meta.Keywords.pro_tentacles.indicators.indicator_handling import (
    activate_multiple_configurable_indicators,
    get_configurable_indicators,
)


async def get_lorentzian_classification(maker, evaluator):
    # TODO cache training data
    # training data stop / tp settings
    (
        values_to_cross_titles,
        selected_indicator_ids,
    ) = await activate_multiple_configurable_indicators(
        maker,
        evaluator,
        data_source_name="classification",
        def_val=["EMA"],
        indicator_group_id=2,
    )
    PREDICTION_LONG = "Long"
    PREDICTION_SHORT = "Short"
    prediction_side = await user_input2(
        maker,
        evaluator,
        name="prediction_side",
        input_type=common_enums.UserInputTypes.OPTIONS.value,
        def_val=PREDICTION_LONG,
        options=[PREDICTION_LONG, PREDICTION_SHORT],
        title="Signal side",
        grid_columns=6,
        order=3,
    )
    neighbors_count = await user_input2(
        maker,
        evaluator,
        name="neighbors_count",
        input_type=common_enums.UserInputTypes.INT.value,
        def_val=8,
        min_val=1,
        max_val=100,
        title="Neighbors Count",
        # parent_input_name=GENERAL_SETTINGS_NAME,
        grid_columns=6,
        description="Number of similar neighbors to consider " "for the prediction.",
        order=1,
    )
    prediction_threshold_percent = await user_input2(
        maker,
        evaluator,
        name="prediction_threshold",
        input_type=common_enums.UserInputTypes.INT.value,
        def_val=50,
        min_val=0,
        max_val=100,
        title="Prediction Threshold",
        # parent_input_name=GENERAL_SETTINGS_NAME,
        grid_columns=6,
        description="% of similar neighbors with a winning prediction",
        order=1,
    )
    prediction_threshold = neighbors_count / 100 * prediction_threshold_percent

    config_candles = classification_utils.get_config_candles(maker.trading_mode.config)
    default_max_bars_back = 2000 if config_candles >= 2000 else config_candles
    max_bars_back = await user_input2(
        maker,
        evaluator,
        name="max_bars_back",
        input_type=common_enums.UserInputTypes.INT.value,
        def_val=default_max_bars_back,
        min_val=1,
        max_val=config_candles,
        title="Max Bars Back",
        description="Amount of historical candles to use as training data. "
        "To increase the max allowed bars back, change 'Amount of historical "
        "candles' in the TimeFrameStrategyEvaluator settings.",
        grid_columns=6,
        order=2,
    )
    down_sampling_mode = await user_input2(
        maker,
        evaluator,
        name="down_sampler",
        input_type=common_enums.UserInputTypes.OPTIONS.value,
        def_val=downsampling.DownSamplers.DEFAULT_DOWN_SAMPLER,
        options=downsampling.DownSamplers.AVAILABLE_DOWN_SAMPLERS,
        title="Down Sampling Mode",
        description="When enabled, the strategy will skip candles of the "
        "training data, within the max bars back. This will speed up "
        "classification and allows you to use a higher max bars back instead, "
        "which will result in a more diverse training data.",
        grid_columns=6,
        order=3,
    )
    only_train_on_every_x_bars = None
    this_down_sampler: typing.Callable[
        [int, int], bool
    ] = downsampling.DownSamplers.DOWN_SAMPLERS_BY_TITLES.get(
        down_sampling_mode, downsampling.DownSamplers.NO_DOWN_SAMPLER
    )
    if down_sampling_mode in (
        downsampling.DownSamplers.SKIP_EVERY_X_DOWN_SAMPLER,
        downsampling.DownSamplers.USE_EVERY_X_DOWN_SAMPLER,
    ):
        title: str = None
        description: str = None
        if down_sampling_mode == downsampling.DownSamplers.SKIP_EVERY_X_DOWN_SAMPLER:
            title = "Skip every X bars of training data"
            description = (
                "Instead of using every bar as training data, "
                "you can instead skip candles and only train on the non skipped "
                "bars. This will speed up classification and allows you to "
                "increase the max bars back instead."
            )
        elif down_sampling_mode == downsampling.DownSamplers.USE_EVERY_X_DOWN_SAMPLER:
            title = "Only train on every X bars"
            description = (
                "Instead of using every bar as training data, "
                "you can instead skip candles and only train on every X bars. "
                "This will speed up classification and allows you to increase the "
                "max bars back instead."
            )

        only_train_on_every_x_bars = await user_input2(
            maker,
            evaluator,
            name="only_train_on_x_bars",
            input_type=common_enums.UserInputTypes.INT.value,
            def_val=4,
            min_val=2,
            title=title,
            description=description,
            grid_columns=6,
            order=4,
        )
    # candle_source = await user_select_candle_source_name(
    #     maker,
    #     evaluator,
    #     "Select the candle source for the training data",
    #     enable_volume=False,
    # )
    await allow_enable_plot(maker, evaluator, "Plot lorentzian classification signals")
    classification_settings = utils.ClassificationSettings(
        neighbors_count=neighbors_count,
        use_remote_fractals=False,
        only_train_on_every_x_bars=only_train_on_every_x_bars,
        live_history_size=config_candles,
        max_bars_back=max_bars_back,
        color_compression=None,
        down_sampler=this_down_sampler,
        training_data_settings=utils.YTrainSettings(
            training_data_type=utils.YTrainTypes.IS_IN_PROFIT_AFTER_4_BARS,
            percent_for_a_win=2,
            percent_for_a_loss=1,
        ),
    )

    values_to_cross_indicators_data = await get_configurable_indicators(
        maker, evaluator, indicator_ids=selected_indicator_ids
    )
    feature_arrays: utils.FeatureArrays = utils.FeatureArrays()
    for feature_array in values_to_cross_indicators_data:
        feature_arrays.add_feature_array(feature_array[0])
    closes = await get_candles_(maker, matrix_enums.PriceDataSources.CLOSE.value)
    lows = await get_candles_(maker, matrix_enums.PriceDataSources.LOW.value)
    highs = await get_candles_(maker, matrix_enums.PriceDataSources.HIGH.value)
    y_train_series = classification_utils.get_y_train_series(
        closes, lows, highs, classification_settings.training_data_settings
    )

    (
        y_train_series,
        closes,
    ) = basic_utilities.cut_data_to_same_len(
        (
            y_train_series,
            closes,
        ),
        reference_length=feature_arrays.cut_data_to_same_len(),
    )

    cutted_data_length: int = feature_arrays.cut_data_to_same_len(
        reference_length=len(closes)
    )

    historical_predictions: list = []
    for candle_index in range(cutted_data_length):
        historical_predictions.append(
            classification_utils.get_classification_predictions(
                candle_index,
                classification_settings,
                feature_arrays,
                y_train_series,
            )
        )
    historical_predictions_array = numpy.array(historical_predictions)
    evaluator.values = await get_candles_(
        maker, matrix_enums.PriceDataSources.LOW.value
    )
    if PREDICTION_SHORT == prediction_side:
        evaluator.signals = numpy.where(
            historical_predictions_array <= -prediction_threshold, 1, 0
        )
    else:
        evaluator.signals = numpy.where(
            historical_predictions_array >= prediction_threshold, 1, 0
        )

    evaluator.title = f"Lorentzian Classification {prediction_side} Signals"

    #     crossing_direction = await user_input2(
    #         maker,
    #         evaluator,
    #         "max_bars_back",
    #         common_common_enums.UserInputTypes.INT,
    #         2000,
    # title="Max bars "    )
    #     crossing_delay = await user_input2(
    #         maker, evaluator, "crossing signal delay", "int", 0
    #     )
    #     max_crossing_lookback = await user_input2(
    #         maker,
    #         evaluator,
    #         "history length for maximum dump/pump (0 = disabled)",
    #         "int",
    #         0,
    #         0,
    #     )
    #     max_crossing = 0
    #     if int(max_crossing_lookback) != 0:
    #         max_crossing = await user_input2(
    #             maker,
    #             evaluator,
    #             "maximum % dump/pump before cross up/down (0 = disabled)",
    #             "float",
    #             0,
    #         )
    #     max_crossing_count = 50
    #     max_crossing = (
    #         None
    #         if int(max_crossing_lookback) == 0 or int(max_crossing) == 0
    #         else str(max_crossing) + "%"
    #     )
    #     max_crossing_count_lookback = await user_input2(
    #         maker,
    #         evaluator,
    #         "history length for nearby signals (0 = disabled)",
    #         "int",
    #         0,
    #         0,
    #     )
    #     if int(max_crossing_count_lookback) != 0:
    #         max_crossing_count = await user_input2(
    #             maker, evaluator, "maximum nearby signals", "int", 1, min_val=1
    #         )
    #         max_crossing_count = max_crossing_count if int(max_crossing_count) != 0 else 50

    #     evaluator.title = (
    #         f"{crossing_values_title} is {crossing_direction} {values_to_cross_titles}"
    #     )
    #     await allow_enable_plot(maker, evaluator, f"Plot when {evaluator.title}")
    #     max_crossing_count_lookback = (
    #         max_crossing_count_lookback if max_crossing_count_lookback != 0 else 1
    #     )

    #     (
    #         data_crossing_values,
    #         evaluator.chart_location,
    #         crossing_values_title,
    #     ) = await get_configurable_indicator(maker, evaluator)
    #     # evaluator.values, _, values_to_cross_title
    #     all_values_to_cross = []
    #     for indicator_data, _, indicator_title in values_to_cross_indicators_data:
    #         all_values_to_cross.append(indicator_data)
    #     all_values_to_cross = cut_data_to_same_len(all_values_to_cross, get_list=True)
    #     stacked_values_to_cross = numpy.dstack(all_values_to_cross)

    #     if crossing_direction == "crossing up":
    #         evaluator.values = stacked_values_to_cross.max(axis=2)[0]
    #         evaluator.signals = await crossing_up_(
    #             maker=maker,
    #             values_to_cross=evaluator.values,
    #             crossing_values=data_crossing_values,
    #             delay=crossing_delay,
    #             max_cross_down=max_crossing,
    #             max_cross_down_lookback=max_crossing_lookback,
    #             max_history=not maker.live_recording_mode,
    #         )

    #     elif crossing_direction == "crossing down":
    #         evaluator.values = stacked_values_to_cross.min(axis=2)[0]
    #         evaluator.signals = await crossing_down_(
    #             maker=maker,
    #             values_to_cross=evaluator.values,
    #             crossing_values=data_crossing_values,
    #             delay=crossing_delay,
    #             max_cross_up=max_crossing,
    #             max_cross_up_lookback=max_crossing_lookback,
    #             max_history=not maker.live_recording_mode,
    #         )
    #     else:  # crossing up or down
    #         evaluator.values = values_to_cross_indicators_data[0][0]
    #         evaluator.signals = await crossing_(
    #             maker=maker,
    #             values_to_cross=evaluator.values,
    #             crossing_values=data_crossing_values,
    #             delay=crossing_delay,
    #             max_cross=max_crossing,
    #             max_cross_lookback=max_crossing_lookback,
    #             max_history=not maker.live_recording_mode,
    #         )
    evaluator.chart_location = "main-chart"

    return await store_evaluator_data(maker, evaluator, allow_signal_extension=True)
