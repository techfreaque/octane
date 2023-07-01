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

import pickle
import typing
from tensorflow import keras
from keras import layers, regularizers

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities
import tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.abstract_neural_net as abstract_neural_net
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.network_utils import (
    custom_activation,
)
import tentacles.Services.Interfaces.octo_ui2.models.neural_net_helper as neural_net_helper


class TensorflowRNN(abstract_neural_net.AbstractNeuralNetwork):
    NEURAL_NET_TITLE = "TensorFlow RNN (Recurrent Neural Network)"
    MESSAGE_PRINT_PREFIX = f" {NEURAL_NET_TITLE} - "
    NEURAL_NETS_FOLDER_NAME = "tensorflow_RNN"
    model: keras.Model
    MAX_BARS_BACK = 20
    super_deep_network: bool = False

    def save_model(self, current_model_filename, tentacles_setup_config):
        # save the model to disk
        with open(
            self.get_model_file_path(current_model_filename, tentacles_setup_config),
            "w+b",
        ) as file:
            pickle.dump(self.model, file)

    def load_model(self, current_model_filename, tentacles_setup_config) -> None:
        # load the model from disk
        m_time = utilities.start_measure_time()
        # try:
        #     self.model = load_model(
        #         self.get_model_file_path(current_model_filename, tentacles_setup_config)
        #         + ".h5"
        #     )
        # except Exception as e:
        # TODO remove this
        with open(
            self.get_model_file_path(current_model_filename, tentacles_setup_config),
            "rb",
        ) as file:
            self.model = pickle.load(file)
            utilities.end_measure_time(
                m_time,
                f"{self.MESSAGE_PRINT_PREFIX}loading model from storage",
            )

    def create_model(
        self,
        batch_size: int,
        learning_rate_init: float,
        n_iter_no_change: int,
        features_count: int,
    ) -> None:
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}creating model"
        )
        input_shape = (self.MAX_BARS_BACK, features_count)
        input_layer = layers.Input(shape=input_shape)

        model_layers = layers.SimpleRNN(
            units=32,
            activation="relu",
            return_sequences=True,
        )(input_layer)
        model_layers = layers.BatchNormalization()(model_layers)

        model_layers = layers.SimpleRNN(
            units=64,
            activation="relu",
            return_sequences=True,
        )(model_layers)
        model_layers = layers.BatchNormalization()(model_layers)

        model_layers = layers.SimpleRNN(
            units=128,
            activation="relu",
            return_sequences=True,
        )(model_layers)
        model_layers = layers.BatchNormalization()(model_layers)

        model_layers = layers.SimpleRNN(
            units=256,
            activation="relu",
            return_sequences=False,
        )(model_layers)

        if self.super_deep_network:
            model_layers = layers.BatchNormalization()(model_layers)

            model_layers = layers.SimpleRNN(
                units=512,
                activation="relu",
                return_sequences=True,
            )(model_layers)
            model_layers = layers.BatchNormalization()(model_layers)

            model_layers = layers.SimpleRNN(
                units=1024,
                activation="relu",
                return_sequences=False,
            )(model_layers)

        model_layers = layers.BatchNormalization()(model_layers)
        model_layers = layers.Dropout(0.2)(model_layers)

        model_layers = layers.Dense(128, activation="relu")(model_layers)

        if self.super_deep_network:
            model_layers = layers.Dense(4096, activation="relu")(model_layers)
            model_layers = layers.Dropout(0.2)(model_layers)

            model_layers = layers.Dense(
                2048, activation="relu", kernel_regularizer=regularizers.L2()
            )(model_layers)
            model_layers = layers.Dropout(0.2)(model_layers)

            model_layers = layers.Dense(
                1024, activation="relu", kernel_regularizer=regularizers.L2()
            )(model_layers)
            model_layers = layers.Dropout(0.2)(model_layers)

        model_layers = layers.Dense(
            128, activation="relu", kernel_regularizer=regularizers.L2()
        )(model_layers)
        output_layer = layers.Dense(
            3,
            # activation="softmax"
            activation=custom_activation,
        )(model_layers)

        self.model = keras.Model(inputs=input_layer, outputs=output_layer)
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}creating model",
        )

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
        n_iter_no_change: int,
        generations: int,
        epochs: int,
        enable_tensorboard: bool,
        save_only_improved_models: bool,
    ):
        print(self.model.summary())

        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}Training model "
            f"with {generations} generations & {epochs} epochs each"
        )

        print(
            f"{self.MESSAGE_PRINT_PREFIX}Training with batch size = "
            + str(batch_size)
            + " learning rate = "
            + str(learning_rate_init)
            + " "
        )
        print(
            f"{self.MESSAGE_PRINT_PREFIX}Stopping if no improvement for "
            + str(n_iter_no_change)
            + " iterations "
        )

        current_loss_test = 0
        if not self.is_new_model and save_only_improved_models:
            _, current_loss_test = self.evaluate_model(
                training_indicator_data=training_indicator_data,
                training_prediction_data=training_prediction_data,
                testing_indicator_data=testing_indicator_data,
                testing_prediction_data=testing_prediction_data,
                epoch_print_prefix="Current Model - ",
                test_evaluation_only=True,
            )

        self.compile_model(learning_rate_init)

        didnt_improve_since_generations = 0
        for neural_net_helper.CURRENT_GENERATION_ID in range(generations):
            if neural_net_helper.SHOULD_STOP_TRAINING:
                break
            generation_print_prefix = (
                f"Generation {neural_net_helper.CURRENT_GENERATION_ID} - "
            )
            if didnt_improve_since_generations > n_iter_no_change:
                if save_only_improved_models:
                    # load last saved model and stop training
                    self.load_model(self.current_model_filename, tentacles_setup_config)
                break
            self.train_model_epoch(
                training_indicator_data=training_indicator_data,
                training_predictions=training_prediction_data,
                testing_indicator_data=testing_indicator_data,
                testing_prediction_data=testing_prediction_data,
                epoch_print_prefix=generation_print_prefix,
                batch_size=batch_size,
                epochs=epochs,
                learning_rate_init=learning_rate_init,
                tentacles_setup_config=tentacles_setup_config,
                enable_tensorboard=enable_tensorboard,
            )
            if save_only_improved_models:
                _, loss_test = self.evaluate_model(
                    training_indicator_data=training_indicator_data,
                    training_prediction_data=training_prediction_data,
                    testing_indicator_data=testing_indicator_data,
                    testing_prediction_data=testing_prediction_data,
                    test_evaluation_only=True,
                    epoch_print_prefix=generation_print_prefix,
                )
                if current_loss_test >= loss_test:
                    didnt_improve_since_generations = 0
                    self.save_model(
                        current_model_filename=self.current_model_filename,
                        tentacles_setup_config=tentacles_setup_config,
                    )
                    print(
                        f"{self.MESSAGE_PRINT_PREFIX}{generation_print_prefix}loss improved on testing data by %0.4f "
                        % (loss_test - current_loss_test)
                    )
                    print(
                        f"{self.MESSAGE_PRINT_PREFIX}{generation_print_prefix}Saving model done"
                    )
                    current_loss_test = loss_test
                else:
                    didnt_improve_since_generations += 1
                    print(
                        f"{self.MESSAGE_PRINT_PREFIX}{generation_print_prefix}loss didnt improve on testing data by %0.4f "
                        % (loss_test - current_loss_test)
                    )
                    print(
                        f"{self.MESSAGE_PRINT_PREFIX}{generation_print_prefix}Skip saving model"
                    )

            else:
                self.save_model(
                    current_model_filename=self.current_model_filename,
                    tentacles_setup_config=tentacles_setup_config,
                )
                print(
                    f"{self.MESSAGE_PRINT_PREFIX}{generation_print_prefix}Saving model done"
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
        learning_rate_init: float,
        enable_tensorboard: bool,
        tentacles_setup_config,
    ):
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}Training model"
        )
        callbacks = [
            keras.callbacks.ModelCheckpoint(
                self.get_model_file_path(
                    self.current_model_filename, tentacles_setup_config
                )
                + ".h5",
                save_best_only=True,
                monitor="loss",
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor="loss",
                factor=0.2,
                patience=2,
                min_lr=learning_rate_init,
            ),
        ]
        if enable_tensorboard:
            callbacks.append(
                keras.callbacks.TensorBoard(
                    log_dir=self.get_models_folder(tentacles_setup_config),
                    histogram_freq=4,
                )
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
    ) -> typing.Tuple[float, float]:
        accuracy_train = None
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
                prediction / probability_sum for prediction in prediction_list
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
