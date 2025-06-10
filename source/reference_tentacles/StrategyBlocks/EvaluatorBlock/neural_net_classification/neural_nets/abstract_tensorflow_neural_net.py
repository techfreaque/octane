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
import keras as keras

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities
from tentacles.Services.Interfaces.octo_ui2.models import neural_net_helper
from tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_net_settings_class import (
    SaveModelBasedOn,
)
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.abstract_neural_net as abstract_neural_net


class AbstractTensorflowNeuralNet(abstract_neural_net.AbstractNeuralNetwork):
    NEURAL_NET_TITLE = "Your model doesnt have a title"
    MESSAGE_PRINT_PREFIX = f" {NEURAL_NET_TITLE} - "
    NEURAL_NETS_FOLDER_NAME = "define_a_folder_name"
    model: keras.Model
    max_bars_back = 20
    network_size: str

    def save_model(self, current_model_filename, tentacles_setup_config):
        # save the model to disk
        self.model.save_weights(
            self.get_model_file_path(current_model_filename, tentacles_setup_config)
        )

    def load_model(
        self,
        tentacles_setup_config,
        features_count: int,
        max_bars_back: int,
        network_size: str,
    ) -> None:
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}loading model"
        )
        self.network_size = network_size
        self.current_model_filename: str = self.get_model_file_name(
            features_count, max_bars_back, network_size
        )
        self.create_model(
            batch_size=None,
            learning_rate_init=None,
            n_iter_no_change=None,
            features_count=features_count,
        )
        try:
            # load the model from disk
            self.model.load_weights(
                self.get_model_file_path(
                    self.current_model_filename, tentacles_setup_config
                )
            )
            self.is_new_model = False
            utilities.end_measure_time(
                m_time,
                f"{self.MESSAGE_PRINT_PREFIX}loading model",
            )
        except FileNotFoundError:
            try:
                # load the model legacy model without .weights.h5
                self.current_model_filename: str = (
                    f"model_for_{features_count}_features__{self.max_bars_back}_bars_back_{self.network_size.replace(' ', '_')}.h5"
                )

                self.model.load_weights(
                    self.get_model_file_path(
                        self.current_model_filename, tentacles_setup_config
                    )
                )
                self.is_new_model = False
                utilities.end_measure_time(
                    m_time,
                    f"{self.MESSAGE_PRINT_PREFIX}loading model",
                )
            except FileNotFoundError:
                try:
                    # load the legacy model from disk
                    # TODO remove this after a few releases
                    if self.network_size != abstract_neural_net.NETWORK_SIZE_DEEP:
                        raise FileNotFoundError
                    current_model_filename: str = (
                        f"model_for_{features_count}_features__{self.max_bars_back}_bars_back.sav.h5"
                    )
                    self.model.load_weights(
                        self.get_model_file_path(
                            current_model_filename, tentacles_setup_config
                        )
                    )
                    self.is_new_model = False

                    utilities.end_measure_time(
                        m_time,
                        f"{self.MESSAGE_PRINT_PREFIX}loading model",
                    )
                except FileNotFoundError:
                    self.is_new_model = True
                    utilities.end_measure_time(
                        m_time,
                        f"{self.MESSAGE_PRINT_PREFIX}creating model",
                    )
        self.current_model_filename: str = self.get_model_file_name(
            features_count, max_bars_back, network_size
        )

    @staticmethod
    def get_model_file_name(features_count, max_bars_back, network_size):
        return f"model_for_{features_count}_features__{max_bars_back}_bars_back_{network_size.replace(' ', '_')}.weights.h5"

    def create_model(
        self,
        batch_size: int,
        learning_rate_init: float,
        n_iter_no_change: int,
        features_count: int,
    ) -> None:
        """
        create the model and store it to self.model
        """

    def compile_model(self, learning_rate_init):
        optimizer = keras.optimizers.Adam(
            amsgrad=True, learning_rate=learning_rate_init
        )
        self.model.compile(
            optimizer=optimizer,
            loss=keras.losses.CategoricalCrossentropy(),
            metrics=[
                keras.metrics.CategoricalAccuracy(),
                # keras.metrics.AUC(),
                # keras.metrics.Precision(),
                # keras.metrics.Recall(),
            ],
        )

    def train_model(
        self,
        tentacles_setup_config,
        training_indicator_data,
        training_prediction_data,
        testing_indicator_data,
        testing_prediction_data,
        batch_size: int,
        learning_rate_init: float,
        generations: int,
        epochs: int,
        enable_tensorboard: bool,
        features_count: int,
        network_size: str,
        evaluate_model_before: bool,
        save_model_based_on: str,
    ):
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}Training model "
            f"with {generations} generations & {epochs} epochs each"
        )
        print(self.model.summary())
        print(
            f"{self.MESSAGE_PRINT_PREFIX}Training with batch size = "
            + str(batch_size)
            + " learning rate = "
            + str(learning_rate_init)
            + " "
        )
        self.compile_model(learning_rate_init)

        current_loss_train = 100
        current_loss_test = 100
        if not self.is_new_model and evaluate_model_before:
            current_loss_train, current_loss_test = self.evaluate_model(
                training_indicator_data=training_indicator_data,
                training_prediction_data=training_prediction_data,
                testing_indicator_data=testing_indicator_data,
                testing_prediction_data=testing_prediction_data,
                epoch_print_prefix="",
                test_evaluation_only=(
                    True if save_model_based_on == SaveModelBasedOn.VAL_LOSS else False
                ),
                train_evaluation_only=(
                    True if save_model_based_on == SaveModelBasedOn.LOSS else False
                ),
            )
        callbacks = self.get_training_callbacks(
            learning_rate_init,
            tentacles_setup_config,
            enable_tensorboard,
            epochs,
            prev_val_loss=(
                current_loss_train
                if save_model_based_on == SaveModelBasedOn.LOSS
                else current_loss_test
            ),
            save_model_based_on=save_model_based_on,
        )
        for neural_net_helper.CURRENT_GENERATION_ID in range(generations):
            if neural_net_helper.SHOULD_STOP_TRAINING:
                break
            generation_print_prefix = (
                f"Generation {neural_net_helper.CURRENT_GENERATION_ID} - "
            )
            if neural_net_helper.CURRENT_GENERATION_ID > 0:
                self.load_model(
                    tentacles_setup_config=tentacles_setup_config,
                    features_count=features_count,
                    max_bars_back=self.max_bars_back,
                    network_size=network_size,
                )
                self.compile_model(learning_rate_init)
            self.train_model_epoch(
                training_indicator_data=training_indicator_data,
                training_predictions=training_prediction_data,
                testing_indicator_data=testing_indicator_data,
                testing_prediction_data=testing_prediction_data,
                epoch_print_prefix=generation_print_prefix,
                batch_size=batch_size,
                epochs=epochs,
                callbacks=callbacks,
            )
        neural_net_helper.ANY_NEURAL_NET_ACTIVE = False
        neural_net_helper.SHOULD_STOP_TRAINING = False
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}Training model",
        )

    def train_model_epoch(
        self,
        training_indicator_data,
        training_predictions,
        testing_indicator_data,
        testing_prediction_data,
        epoch_print_prefix: str,
        batch_size: int,
        epochs: int,
        callbacks,
    ):
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}Training model"
        )
        self.model.fit(
            training_indicator_data,
            training_predictions,
            epochs=epochs,
            callbacks=callbacks,
            validation_data=(testing_indicator_data, testing_prediction_data),
            batch_size=batch_size,
            use_multiprocessing=True,
        )
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}Training model",
        )

    def evaluate_model(
        self,
        training_indicator_data,
        training_prediction_data,
        testing_indicator_data,
        testing_prediction_data,
        epoch_print_prefix: str,
        test_evaluation_only: bool = False,
        train_evaluation_only: bool = False,
    ) -> typing.Tuple[float, float]:
        accuracy_train = None
        accuracy_test = None
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}Evaluating model"
        )
        if not test_evaluation_only:
            accuracy_train = self.model.evaluate(
                training_indicator_data,
                training_prediction_data,
            )[0]
            print(
                f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}loss on training data: %0.4f "
                % accuracy_train
            )
        if not train_evaluation_only:
            accuracy_test = self.model.evaluate(
                testing_indicator_data,
                testing_prediction_data,
            )[0]
            print(
                f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}loss on testing data: %0.4f "
                % accuracy_test
            )
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}Evaluating model",
        )
        return accuracy_train, accuracy_test

    def predict_on_historical_candles(
        self, full_indicator_data, prediction_side: str, prediction_threshold: float
    ):
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}predicting signals"
        )
        model_signals = []
        model_opposite_signals = []
        model_predictions = []

        unformatted_predictions = self.model.predict(full_indicator_data)

        for prediction_list in unformatted_predictions:
            probability_sum = sum(prediction_list)
            normalized_prediction_list = [
                prediction * probability_sum for prediction in prediction_list
            ]
            prediction = normalized_prediction_list[0] - normalized_prediction_list[2]
            model_predictions.append(prediction)
            signal = False
            opposite_signal = False
            if prediction_side == "Long":
                signal = 1 / 100 * prediction_threshold < prediction
                opposite_signal = -1 / 100 * prediction_threshold > prediction
            else:
                opposite_signal = 1 / 100 * prediction_threshold < prediction
                signal = -1 / 100 * prediction_threshold > prediction
            model_signals.append(signal)
            model_opposite_signals.append(opposite_signal)
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}predicting signals",
        )
        return model_predictions, model_signals, model_opposite_signals

    def get_training_callbacks(
        self,
        learning_rate_init,
        tentacles_setup_config,
        enable_tensorboard,
        epochs,
        prev_val_loss,
        save_model_based_on: str,
    ):
        final_lr = learning_rate_init * 1000
        num_samples = epochs

        def lr_schedule(epoch, lr):
            if epoch < num_samples:
                return (final_lr / learning_rate_init) ** (
                    epoch / num_samples
                ) * learning_rate_init
            return final_lr

        should_save_all = SaveModelBasedOn.SAVE_ALL == save_model_based_on
        callbacks = [
            keras.callbacks.ModelCheckpoint(
                self.get_model_file_path(
                    self.current_model_filename, tentacles_setup_config
                ),
                save_best_only=not should_save_all,
                monitor=(
                    SaveModelBasedOn.VAL_LOSS
                    if should_save_all
                    else save_model_based_on
                ),
                verbose=1,
                initial_value_threshold=None if should_save_all else prev_val_loss,
                save_weights_only=True,
            ),
            # keras.callbacks.ReduceLROnPlateau(
            #     monitor="val_loss",
            #     factor=0.1,
            #     patience=1,
            #     verbose=0,
            #     mode="auto",
            #     min_delta=0.0001,
            #     cooldown=0,
            #     min_lr=learning_rate_init,
            # )
            keras.callbacks.LearningRateScheduler(lr_schedule, verbose=0),
            keras.callbacks.TerminateOnNaN(),
        ]
        if enable_tensorboard:
            callbacks.append(
                keras.callbacks.TensorBoard(
                    log_dir=self.get_models_folder(tentacles_setup_config),
                    histogram_freq=4,
                )
            )
        return callbacks
