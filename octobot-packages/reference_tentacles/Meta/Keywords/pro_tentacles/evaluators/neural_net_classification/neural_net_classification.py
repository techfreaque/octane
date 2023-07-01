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

from copy import deepcopy
from threading import Thread

from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_net_settings import (
    get_neural_network_with_config,
)
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_net_settings_class import (
    NeuralNetClassificationSettings,
    SignalTypes,
)
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets import (
    abstract_neural_net,
)

import tentacles.Meta.Keywords.scripting_library.data.writing.plotting as plotting
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_evaluator_data,
)
from tentacles.Meta.Keywords.pro_tentacles.indicators.indicator_handling import (
    get_configurable_indicators,
)

import tentacles.Services.Interfaces.octo_ui2.models.neural_net_helper as neural_net_helper


async def get_neural_net_classification(maker, evaluator):
    neuralnet_and_settings = await get_neural_network_with_config(maker, evaluator)
    NeuralNetworkClass: abstract_neural_net.AbstractNeuralNetwork = (
        neuralnet_and_settings[0]
    )
    neuralnet_settings: NeuralNetClassificationSettings = neuralnet_and_settings[1]

    neural_net: abstract_neural_net.AbstractNeuralNetwork = NeuralNetworkClass(
        batch_size=neuralnet_settings.batch_size,
        feature_names=neuralnet_settings.feature_names,
        learning_rate_init=neuralnet_settings.learning_rate_init,
        n_iter_no_change=neuralnet_settings.n_iter_no_change,
        tentacles_setup_config=maker.exchange_manager.tentacles_setup_config,
    )
    m_time = utilities.start_measure_time(
        f"{neural_net.MESSAGE_PRINT_PREFIX}Loading indicators"
    )
    indicators_data = await get_configurable_indicators(
        maker, evaluator, indicator_ids=neuralnet_settings.selected_indicator_ids
    )
    utilities.end_measure_time(
        m_time,
        f"{neural_net.MESSAGE_PRINT_PREFIX}Loading indicators",
    )
    (
        training_indicator_data,
        training_prediction_data,
        testing_indicator_data,
        testing_prediction_data,
        full_indicator_data,
        training_prediction_labels,
        candle_closes,
    ) = await neural_net.get_formatted_features_and_training_predictions(
        maker=maker,
        training_prediction_target_settings=neuralnet_settings.training_prediction_target_settings,
        indicators_data=indicators_data,
        percent_to_use_as_training_data=70,
    )
    if maker.exchange_manager.is_backtesting and neuralnet_settings.enable_training:
        if neural_net_helper.ANY_NEURAL_NET_ACTIVE:
            print("Cant train on multiple pairs aborting this run")
        else:
            neural_net_helper.ANY_NEURAL_NET_ACTIVE = True
            neural_net_helper.SHOULD_STOP_TRAINING = False
            neural_net_helper.CURRENT_GENERATION_ID = 0
            training_net = deepcopy(neural_net)
            maker.trading_mode.training_thread = Thread(
                target=training_net.train_model,
                name="neural_net_training",
                kwargs={
                    "tentacles_setup_config": deepcopy(
                        maker.exchange_manager.tentacles_setup_config
                    ),
                    "training_indicator_data": training_indicator_data,
                    "training_prediction_data": training_prediction_data,
                    "testing_indicator_data": testing_indicator_data,
                    "testing_prediction_data": testing_prediction_data,
                    "batch_size": neuralnet_settings.batch_size,
                    "learning_rate_init": neuralnet_settings.learning_rate_init,
                    "n_iter_no_change": neuralnet_settings.n_iter_no_change,
                    "generations": neuralnet_settings.generations,
                    "epochs": neuralnet_settings.epochs,
                    "enable_tensorboard": neuralnet_settings.enable_tensorboard,
                    "save_only_improved_models": neuralnet_settings.save_only_improved_models,
                },
            )
            maker.trading_mode.training_thread.start()
    elif neural_net.is_new_model:
        raise RuntimeError("The model needs to be trained before it can be used!")
    (
        model_predictions,
        evaluator.signals,
        second_signals,
    ) = neural_net.predict_on_historical_candles(
        full_indicator_data=full_indicator_data,
        prediction_side=neuralnet_settings.prediction_side,
        prediction_threshold=neuralnet_settings.prediction_threshold,
    )
    evaluator.values = candle_closes
    evaluator.title = (
        f"{neuralnet_settings.prediction_side} Signals {neural_net.NEURAL_NET_TITLE}"
    )
    evaluator.chart_location = "main-chart"
    if neuralnet_settings.plot_opposite_signal_side:
        evaluator.second_values = candle_closes
        evaluator.second_title = f"{SignalTypes.SHORT if neuralnet_settings.prediction_side == SignalTypes.LONG else SignalTypes.LONG} Signals {neural_net.NEURAL_NET_TITLE}"
        evaluator.second_signals = second_signals
        evaluator.second_chart_location = "main-chart"
    await handle_additional_plots(
        neuralnet_settings.plot_training_predictions,
        neuralnet_settings.plot_neural_net_predictions,
        maker,
        training_prediction_labels,
        model_predictions,
    )
    return await store_evaluator_data(
        maker, evaluator, allow_signal_extension=True, reset_cache_before_writing=True
    )


async def handle_additional_plots(
    plot_training_predictions: bool,
    plot_neural_net_predictions: bool,
    maker,
    prediction_data,
    model_predictions,
):
    if plot_training_predictions or plot_neural_net_predictions:
        candle_times = await get_candles_(
            maker, matrix_enums.PriceDataSources.TIME.value
        )
        (
            candle_times,
            prediction_data,
            model_predictions,
        ) = utilities.cut_data_to_same_len(
            (candle_times, prediction_data, model_predictions)
        )
        await maker.ctx.set_cached_values(
            values=prediction_data,
            cache_keys=candle_times,
            value_key="yt",
            additional_values_by_key={"pred": model_predictions},
        )
        if plot_training_predictions:
            await plotting.plot(
                maker.ctx,
                title="Training Prediction Labels",
                cache_value="yt",
                chart="sub-chart",
                own_yaxis=True,
            )
        if plot_neural_net_predictions:
            await plotting.plot(
                maker.ctx,
                title="Neural Net Predictions",
                cache_value="pred",
                chart="sub-chart",
                own_yaxis=True,
            )
