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

import asyncio
import copy
import numpy
import threading
import typing
import octobot_commons.enums as common_enums
import octobot.constants as constants
import tentacles.Meta.Keywords.scripting_library.data.writing.plotting as plotting

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.ml_utils.utils as utils
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities

import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_evaluator_block as abstract_evaluator_block
from tentacles.Services.Interfaces.octo_ui2.models import neural_net_helper
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.available_neural_nets as available_neural_nets
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_net_settings_class as neural_net_settings_class
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.abstract_neural_net as abstract_neural_net


class NeuralNetClassificationEvaluator(abstract_evaluator_block.EvaluatorBlock):
    NAME = "neural_net_classification"
    TITLE = "Neural Net Classification"
    TITLE_SHORT = "Neural Net Classification"
    DESCRIPTION = (
        "Neural Net Classification offers multiple deep neural net architectures. "
        "The input layer of any network consists of multiple indicator data sources. "
        "The output layer tries to predict the state of the candle, "
        "which is a number between -1 and 1. 0 is neutral, 1 is long and -1 is short"
    )

    NeuralNetworkClass: abstract_neural_net.AbstractNeuralNetwork
    MESSAGE_PRINT_PREFIX: str
    neuralnet_settings: neural_net_settings_class.NeuralNetClassificationSettings

    def init_block_settings(self) -> None:
        network_types_list = list(available_neural_nets.NEURAL_NETS.keys())
        network_type = self.user_input(
            name="network_type",
            input_type=common_enums.UserInputTypes.OPTIONS.value,
            def_val=network_types_list[0],
            options=network_types_list,
            title="Neural Net Type",
        )
        self.NeuralNetworkClass: abstract_neural_net.AbstractNeuralNetwork = (
            available_neural_nets.NEURAL_NETS.get(
                network_type, available_neural_nets.NEURAL_NETS[network_types_list[0]]
            )
        )
        self.MESSAGE_PRINT_PREFIX = f" {network_type} - "
        training_settings_name = "training_settings"
        self.user_input(
            name=training_settings_name,
            input_type=common_enums.UserInputTypes.OBJECT.value,
            def_val=None,
            title="Training Settings",
            grid_columns=12,
            editor_options={
                common_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
                common_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
            },
        )
        training_settings_parent_input_name = (
            f"{training_settings_name}_{self.node_parent_input}"
        )
        prediction_settings_name = "prediction_settings"
        self.user_input(
            name=prediction_settings_name,
            input_type=common_enums.UserInputTypes.OBJECT.value,
            def_val=None,
            title="Prediction Settings",
            grid_columns=12,
            editor_options={
                common_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
                common_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
            },
        )
        prediction_settings_parent_input_name = (
            f"{prediction_settings_name}_{self.node_parent_input}"
        )
        display_settings_name = "display_settings"
        self.user_input(
            name=display_settings_name,
            input_type=common_enums.UserInputTypes.OBJECT.value,
            def_val=None,
            title="Display Settings",
            grid_columns=12,
            editor_options={
                common_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
                common_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
            },
        )
        display_settings_parent_input_name = (
            f"{display_settings_name}_{self.node_parent_input}"
        )
        prediction_side = self.user_input(
            name="prediction_side",
            input_type=common_enums.UserInputTypes.OPTIONS.value,
            def_val=neural_net_settings_class.SignalTypes.LONG,
            options=[
                neural_net_settings_class.SignalTypes.LONG,
                neural_net_settings_class.SignalTypes.SHORT,
            ],
            title="Prediction side",
            parent_input_name=prediction_settings_parent_input_name,
        )
        plot_opposite_signal_side = self.user_input(
            name="plot_opposite_signal_side",
            input_type=common_enums.UserInputTypes.BOOLEAN.value,
            def_val=False,
            title="also Enable other sides signals",
            parent_input_name=display_settings_parent_input_name,
        )
        enable_training = self.user_input(
            name="enable_training",
            input_type=common_enums.UserInputTypes.BOOLEAN.value,
            def_val=True,
            title="Enable neural net training in backtesting mode",
            parent_input_name=training_settings_parent_input_name,
        )
        symbols: typing.Optional[typing.Set[str]] = None
        time_frames: typing.Optional[typing.Set[str]] = None
        enable_backtest_while_trainig: bool = True
        if enable_training:
            enable_backtest_while_trainig = self.user_input(
                name="enable_backtest_while_trainig",
                input_type=common_enums.UserInputTypes.BOOLEAN.value,
                def_val=False,
                title="Enable backtesting when training starts",
                parent_input_name=training_settings_parent_input_name,
            )
            available_pairs = self.get_available_pairs()
            symbols = set(
                self.user_input(
                    name="symbols_to_train",
                    input_type=common_enums.UserInputTypes.MULTIPLE_OPTIONS.value,
                    def_val=available_pairs,
                    options=available_pairs,
                    title="Symbols to train on",
                    parent_input_name=training_settings_parent_input_name,
                )
            )
            symbols.add(self.block_factory.trading_mode.symbol)
            available_time_frames = self.get_available_time_frames()
            time_frames = set(
                self.user_input(
                    name="time_frames_to_train",
                    input_type=common_enums.UserInputTypes.MULTIPLE_OPTIONS.value,
                    def_val=available_time_frames,
                    options=available_time_frames,
                    title="time_frames to train on",
                    parent_input_name=training_settings_parent_input_name,
                )
            )
        network_size = self.user_input(
            name="network_size",
            input_type=common_enums.UserInputTypes.OPTIONS.value,
            def_val=abstract_neural_net.NETWORK_SIZE_DEEP,
            title="Network size",
            description="Note that the very and super deep network requires powerful hardware and a lot of training",
            options=self.NeuralNetworkClass.NETWORK_SIZES,
            parent_input_name=training_settings_parent_input_name,
        )
        max_bars_back = self.user_input(
            name="max_bars_back",
            input_type=common_enums.UserInputTypes.INT.value,
            def_val=20,
            title="Avaliable bars back for each prediction",
            description=(
                "Note that changing the available bars back, will result in changing the model and requires retraining. "
                "The more history the model uses, the slower training and predicting will be."
            ),
            parent_input_name=training_settings_parent_input_name,
        )

        prediction_threshold: float = self.user_input(
            name="prediction_threshold",
            input_type=common_enums.UserInputTypes.FLOAT.value,
            def_val=80,
            min_val=0,
            max_val=100,
            title="Prediction threshold",
            description=(
                "A prediction will have a certianty that ranges from 0 - 100. "
                "If you set this threshold to 80, the prediction must be at least 80%."
            ),
            parent_input_name=prediction_settings_parent_input_name,
        )
        batch_size: float = self.user_input(
            name="batch_size",
            input_type=common_enums.UserInputTypes.INT.value,
            def_val=10,
            min_val=0,
            title="Batch size",
            description=(
                "We divide the training set into batches (number of samples). The "
                "batch_size is the sample size (number of training instances "
                "each batch contains)"
            ),
            parent_input_name=training_settings_parent_input_name,
        )
        learning_rate_init: float = self.user_input(
            name="learning_rate_init",
            input_type=common_enums.UserInputTypes.FLOAT.value,
            def_val=0.001,
            min_val=0,
            title="Learning Rate",
            parent_input_name=training_settings_parent_input_name,
        )
        generations: float = self.user_input(
            name="generations",
            input_type=common_enums.UserInputTypes.INT.value,
            def_val=1,
            min_val=1,
            title="Generations to train",
            description=(
                "A generation consists of multiple epochs and marks as a "
                "checkpoint for the model. If the accuracy improved, the model will "
                "get saved after each generation"
            ),
            # description="A generation takes ~1 minutes to train, depending on the amount of historical data selected",
            grid_columns=6,
            parent_input_name=training_settings_parent_input_name,
        )
        epochs: float = self.user_input(
            name="epochs",
            input_type=common_enums.UserInputTypes.INT.value,
            def_val=5,
            min_val=1,
            title="Epochs to train in each generation",
            parent_input_name=training_settings_parent_input_name,
        )
        losses = {
            "Loss improved on training data": neural_net_settings_class.SaveModelBasedOn.LOSS,
            "Loss improved on validation data": neural_net_settings_class.SaveModelBasedOn.VAL_LOSS,
            "Save model on every epoch": neural_net_settings_class.SaveModelBasedOn.SAVE_ALL,
        }
        _save_model_based_on: str = self.user_input(
            name="save_model_based_on",
            input_type=common_enums.UserInputTypes.OPTIONS.value,
            def_val=next(iter(losses.keys())),
            options=list(losses.keys()),
            title="Auto save model based on",
            parent_input_name=training_settings_parent_input_name,
        )
        save_model_based_on: str = losses[_save_model_based_on]
        evaluate_model_before: bool = False
        if save_model_based_on != neural_net_settings_class.SaveModelBasedOn.SAVE_ALL:
            evaluate_model_before = self.user_input(
                name="evaluate_model_before",
                input_type=common_enums.UserInputTypes.BOOLEAN.value,
                def_val=False,
                title="Evaluate model before training",
                description=(
                    "Models get only saved when loss improves, but without an "
                    "initial loss evaluation, the first epoch of the first generation "
                    "will get saved if there is no loss computed. If enabled it will add "
                    "extra time before the training starts."
                ),
                parent_input_name=training_settings_parent_input_name,
            )
        # save_only_improved_models = self.user_input(
        #     name="save_only_improved_models",
        #     input_type=common_enums.UserInputTypes.BOOLEAN.value,
        #     def_val=False,
        #     title="Only save models for generations that improved in accuracy",
        #     parent_input_name=training_settings_parent_input_name,
        # )
        # n_iter_no_change: typing.Optional[int] = None
        # if save_only_improved_models:
        #     n_iter_no_change = self.user_input(
        #         name="n_iter_no_change",
        #         input_type=common_enums.UserInputTypes.INT.value,
        #         def_val=3,
        #         min_val=0,
        #         max_val=100,
        #         title="Stop training after n generations without accuracy improvement",
        #         parent_input_name=training_settings_parent_input_name,
        #     )
        training_prediction_target_settings = utils.YTrainSettings(
            training_data_type=utils.YTrainTypes.IS_WINNING_TRADE,
            percent_for_a_win=self.user_input(
                name="percent_target_for_win",
                input_type=common_enums.UserInputTypes.FLOAT.value,
                def_val=3,
                min_val=0,
                max_val=100,
                title="Percent target to count as a win",
                parent_input_name=training_settings_parent_input_name,
            ),
            percent_for_a_loss=self.user_input(
                name="percent_target_for_loss",
                input_type=common_enums.UserInputTypes.FLOAT.value,
                def_val=1.5,
                min_val=0,
                max_val=100,
                title="Percent target to count as a loss",
                parent_input_name=training_settings_parent_input_name,
            ),
        )
        plot_training_predictions = self.user_input(
            name="plot_training_predictions",
            input_type=common_enums.UserInputTypes.BOOLEAN.value,
            def_val=False,
            title="Plot training predictions",
            parent_input_name=display_settings_parent_input_name,
        )
        plot_neural_net_predictions = self.user_input(
            name="plot_neural_net_predictions",
            input_type=common_enums.UserInputTypes.BOOLEAN.value,
            def_val=False,
            title="Plot neural net predictions",
            parent_input_name=display_settings_parent_input_name,
        )
        enable_tensorboard = self.user_input(
            name="enable_tensorboard",
            input_type=common_enums.UserInputTypes.BOOLEAN.value,
            def_val=False,
            title="Enable tensorboard logging",
            description=(
                "Execute the following to start the tensorboard dashboard: \n"
                "tensorboard --logdir user/profiles/Profile-Name/specific_config"
                "/neural_net_models/tensorflow_CNN_LSTM"
            ),
            parent_input_name=display_settings_parent_input_name,
        )
        self.activate_multiple_input_data_nodes(
            data_source_name="Model Input Features", def_val=["rsi", "mfi"]
        )
        self.neuralnet_settings: (
            neural_net_settings_class.NeuralNetClassificationSettings
        ) = neural_net_settings_class.NeuralNetClassificationSettings(
            training_prediction_target_settings=training_prediction_target_settings,
            batch_size=batch_size,
            learning_rate_init=learning_rate_init,
            # n_iter_no_change=n_iter_no_change,
            enable_training=enable_training,
            generations=generations,
            epochs=epochs,
            max_bars_back=max_bars_back,
            enable_backtest_while_trainig=enable_backtest_while_trainig,
            # save_only_improved_models=save_only_improved_models,
            prediction_side=prediction_side,
            prediction_threshold=prediction_threshold,
            plot_training_predictions=plot_training_predictions,
            plot_neural_net_predictions=plot_neural_net_predictions,
            plot_opposite_signal_side=plot_opposite_signal_side,
            enable_tensorboard=enable_tensorboard,
            symbols=symbols,
            time_frames=time_frames,
            network_size=network_size,
            evaluate_model_before=evaluate_model_before,
            save_model_based_on=save_model_based_on,
        )
        self.register_evaluator_data_output(
            title=f"Neural {prediction_side} Net Signals",
            plot_switch_text=f"Plot {prediction_side} signals",
            plot_color_switch_title=f"Signals {prediction_side} plot color",
            default_plot_color=block_factory_enums.Colors.GREEN,
            parent_input_name=display_settings_parent_input_name,
        )
        opposite_signal = (
            neural_net_settings_class.SignalTypes.LONG
            if prediction_side == neural_net_settings_class.SignalTypes.SHORT
            else neural_net_settings_class.SignalTypes.SHORT
        )
        if plot_opposite_signal_side:
            self.register_evaluator_data_output(
                title=f"Neural {opposite_signal} Net Signals",
                plot_switch_text=f"Plot {opposite_signal} signals",
                plot_color_switch_title=f"Signals {opposite_signal} plot color",
                default_plot_color=block_factory_enums.Colors.PURPLE,
                parent_input_name=display_settings_parent_input_name,
            )

    async def execute_block(
        self,
    ) -> None:
        should_train_now = (
            self.block_factory.ctx.exchange_manager.is_backtesting
            and self.neuralnet_settings.enable_training
            and not neural_net_helper.ANY_NEURAL_NET_ACTIVE
        )
        if should_train_now:
            neural_net_helper.ANY_NEURAL_NET_ACTIVE = True
        if (
            self.block_factory.ctx.exchange_manager.is_backtesting
            and not self.neuralnet_settings.enable_backtest_while_trainig
        ):
            # store empty signal so it doesnt raise an error
            await self._store_signals(
                signals=[],
                this_pairs_candle_closes=[],
                second_signals=[],
            )
            if not should_train_now:
                return
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}Loading indicators"
        )
        indicators_data = await self.get_multi_input_node_data(
            symbols=(
                self.neuralnet_settings.symbols
                if should_train_now
                else (self.block_factory.ctx.symbol,)
            ),
            time_frames=(
                self.neuralnet_settings.time_frames
                if should_train_now
                else (self.block_factory.ctx.time_frame,)
            ),
        )
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}Loading indicators",
        )
        feature_names = [
            indicator_data[2] for indicator_data in next(iter(indicators_data.values()))
        ]
        symbols_info = [key for key in indicators_data.keys()]
        neural_net: abstract_neural_net.AbstractNeuralNetwork = self.NeuralNetworkClass(
            batch_size=self.neuralnet_settings.batch_size,
            feature_names=feature_names,
            learning_rate_init=self.neuralnet_settings.learning_rate_init,
            # n_iter_no_change=self.neuralnet_settings.n_iter_no_change,
            max_bars_back=self.neuralnet_settings.max_bars_back,
            tentacles_setup_config=self.block_factory.ctx.exchange_manager.tentacles_setup_config,
            network_size=self.neuralnet_settings.network_size,
            symbols_info=symbols_info,
        )
        (
            training_indicator_data,
            training_prediction_data,
            testing_indicator_data,
            testing_prediction_data,
            this_pairs_full_indicator_data,
            this_pairs_training_prediction_labels,
            this_pairs_candle_closes,
        ) = await neural_net.get_formatted_features_and_training_predictions(
            neural_net_block=self,
            training_prediction_target_settings=self.neuralnet_settings.training_prediction_target_settings,
            indicators_data=indicators_data,
            percent_to_use_as_training_data=70,
        )

        if should_train_now:
            neural_net_helper.SHOULD_STOP_TRAINING = False
            neural_net_helper.CURRENT_GENERATION_ID = 0
            training_net: abstract_neural_net.AbstractNeuralNetwork = (
                self.NeuralNetworkClass(
                    batch_size=self.neuralnet_settings.batch_size,
                    feature_names=feature_names,
                    learning_rate_init=self.neuralnet_settings.learning_rate_init,
                    # n_iter_no_change=self.neuralnet_settings.n_iter_no_change,
                    max_bars_back=self.neuralnet_settings.max_bars_back,
                    tentacles_setup_config=self.block_factory.ctx.exchange_manager.tentacles_setup_config,
                    network_size=self.neuralnet_settings.network_size,
                    symbols_info=symbols_info,
                )
            )
            if constants.RUN_IN_MAIN_THREAD:
                training_net.train_model(
                    tentacles_setup_config=copy.deepcopy(
                        self.block_factory.ctx.exchange_manager.tentacles_setup_config
                    ),
                    training_indicator_data=training_indicator_data,
                    training_prediction_data=training_prediction_data,
                    testing_indicator_data=testing_indicator_data,
                    testing_prediction_data=testing_prediction_data,
                    batch_size=self.neuralnet_settings.batch_size,
                    learning_rate_init=self.neuralnet_settings.learning_rate_init,
                    generations=self.neuralnet_settings.generations,
                    epochs=self.neuralnet_settings.epochs,
                    enable_tensorboard=self.neuralnet_settings.enable_tensorboard,
                    features_count=len(feature_names),
                    network_size=self.neuralnet_settings.network_size,
                    evaluate_model_before=self.neuralnet_settings.evaluate_model_before,
                    save_model_based_on=self.neuralnet_settings.save_model_based_on,
                )
            else:
                thread = threading.Thread(
                    target=training_net.train_model,
                    name="neural_net_training",
                    kwargs={
                        "tentacles_setup_config": copy.deepcopy(
                            self.block_factory.ctx.exchange_manager.tentacles_setup_config
                        ),
                        "training_indicator_data": training_indicator_data,
                        "training_prediction_data": training_prediction_data,
                        "testing_indicator_data": testing_indicator_data,
                        "testing_prediction_data": testing_prediction_data,
                        "batch_size": self.neuralnet_settings.batch_size,
                        "learning_rate_init": self.neuralnet_settings.learning_rate_init,
                        "generations": self.neuralnet_settings.generations,
                        "epochs": self.neuralnet_settings.epochs,
                        "enable_tensorboard": self.neuralnet_settings.enable_tensorboard,
                        "features_count": len(feature_names),
                        "network_size": self.neuralnet_settings.network_size,
                        "evaluate_model_before": self.neuralnet_settings.evaluate_model_before,
                        "save_model_based_on": self.neuralnet_settings.save_model_based_on,
                    },
                )
                thread.start()
        elif neural_net.is_new_model:
            raise utils.ModelNeedToBeTrainedFirstException(
                "The model needs to be trained before it can be used!"
            )
        if this_pairs_full_indicator_data is None:
            self.block_factory.logger.error(
                "Not enough indicator data to prredict on "
                f"{self.block_factory.ctx.symbol} / {self.block_factory.ctx.symbol}, "
                "this pair will be skipped"
            )
        else:
            if (
                self.neuralnet_settings.enable_backtest_while_trainig
                or not self.block_factory.ctx.exchange_manager.is_backtesting
            ):
                prediction_thread = threading.Thread(
                    target=self.predict_trades,
                    name="neural_net_predictions",
                    kwargs={
                        "neural_net": neural_net,
                        "this_pairs_full_indicator_data": this_pairs_full_indicator_data,
                        "this_pairs_training_prediction_labels": this_pairs_training_prediction_labels,
                        "this_pairs_candle_closes": this_pairs_candle_closes,
                    },
                )
                prediction_thread.start()
                prediction_thread.join()
            elif self.block_factory.ctx.exchange_manager.is_backtesting:
                self.block_factory.handle_backtesting_timestamp_whitelist(
                    list(
                        await self.get_candles(matrix_enums.PriceDataSources.TIME.value)
                    )
                )

    def predict_trades(
        self,
        neural_net: abstract_neural_net.AbstractNeuralNetwork,
        this_pairs_full_indicator_data,
        this_pairs_training_prediction_labels,
        this_pairs_candle_closes,
    ):
        async def _predict_trades():
            (
                model_predictions,
                signals,
                second_signals,
            ) = neural_net.predict_on_historical_candles(
                full_indicator_data=(
                    [this_pairs_full_indicator_data[-1]]
                    if self.block_factory.live_recording_mode
                    else this_pairs_full_indicator_data
                ),
                prediction_side=self.neuralnet_settings.prediction_side,
                prediction_threshold=self.neuralnet_settings.prediction_threshold,
            )

            await handle_additional_plots(
                neural_net_block=self,
                plot_training_predictions=self.neuralnet_settings.plot_training_predictions,
                plot_neural_net_predictions=self.neuralnet_settings.plot_neural_net_predictions,
                prediction_data=(
                    [this_pairs_training_prediction_labels[-1]]
                    if self.block_factory.live_recording_mode
                    else this_pairs_training_prediction_labels
                ),
                model_predictions=[
                    0 if numpy.isnan(prediction) else prediction
                    for prediction in model_predictions
                ],
            )
            await self._store_signals(
                signals,
                this_pairs_candle_closes,
                second_signals,
            )

        asyncio.run(_predict_trades())

    async def _store_signals(
        self,
        signals,
        this_pairs_candle_closes,
        second_signals,
    ):
        await self.store_evaluator_signals(
            title=f"{self.neuralnet_settings.prediction_side} Signals {self.NeuralNetworkClass.NEURAL_NET_TITLE}",
            signals=signals,
            signal_values=this_pairs_candle_closes,
            chart_location="main-chart",
            reset_cache_before_writing=True,
            allow_signal_extension=True,
        )
        if self.neuralnet_settings.plot_opposite_signal_side:
            oher_signal_side = (
                neural_net_settings_class.SignalTypes.SHORT
                if self.neuralnet_settings.prediction_side
                == neural_net_settings_class.SignalTypes.LONG
                else neural_net_settings_class.SignalTypes.LONG
            )
            await self.store_evaluator_signals(
                title=f"{oher_signal_side} Signals {self.NeuralNetworkClass.NEURAL_NET_TITLE}",
                signals=second_signals,
                signal_values=this_pairs_candle_closes,
                chart_location="main-chart",
                reset_cache_before_writing=True,
                allow_signal_extension=True,
            )


async def handle_additional_plots(
    neural_net_block: NeuralNetClassificationEvaluator,
    plot_training_predictions: bool,
    plot_neural_net_predictions: bool,
    prediction_data,
    model_predictions,
):
    # TODO move to abstract block
    if plot_training_predictions or plot_neural_net_predictions:
        candle_times = await neural_net_block.get_candles(
            matrix_enums.PriceDataSources.TIME.value
        )
        (
            candle_times,
            prediction_data,
            model_predictions,
        ) = utilities.cut_data_to_same_len(
            (candle_times, prediction_data, model_predictions)
        )
        y_train_value_key = neural_net_block._get_next_cache_value_key()
        prediction_value_key = neural_net_block._get_next_cache_value_key()
        await neural_net_block.block_factory.ctx.set_cached_values(
            values=prediction_data,
            cache_keys=candle_times,
            value_key=y_train_value_key,
            additional_values_by_key={prediction_value_key: model_predictions},
        )
        if plot_training_predictions:
            await plotting.plot(
                neural_net_block.block_factory.ctx,
                title="Training Prediction Labels",
                cache_value=y_train_value_key,
                chart="sub-chart",
                own_yaxis=True,
            )
        if plot_neural_net_predictions:
            await plotting.plot(
                neural_net_block.block_factory.ctx,
                title="Neural Net Predictions",
                cache_value=prediction_value_key,
                chart="sub-chart",
                own_yaxis=True,
            )
