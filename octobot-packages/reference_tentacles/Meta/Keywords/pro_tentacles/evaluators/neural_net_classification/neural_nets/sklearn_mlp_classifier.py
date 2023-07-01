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
import numpy
from sklearn.neural_network import MLPClassifier

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities
import tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.abstract_neural_net as abstract_neural_net


class SKLearnMLP(abstract_neural_net.AbstractNeuralNetwork):
    NEURAL_NET_TITLE = "SKLearn Multi Layer Perceptron Classifier"
    MESSAGE_PRINT_PREFIX = f" {NEURAL_NET_TITLE} - "
    NEURAL_NETS_FOLDER_NAME = "sklearn_models"

    model: MLPClassifier

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
        network_layers = [100, 100]
        params = {
            "hidden_layer_sizes": network_layers,
            "activation": "tanh",
            "solver": "sgd",
            "alpha": 0.0,
            "batch_size": batch_size,
            "random_state": 1,
            "tol": 0.0001,
            "nesterovs_momentum": False,
            "learning_rate": "constant",
            "learning_rate_init": learning_rate_init,
            "max_iter": 1000,
            "shuffle": True,
            "n_iter_no_change": n_iter_no_change,
            "verbose": False,
        }

        print(
            f"{self.MESSAGE_PRINT_PREFIX}Creating {features_count}-({network_layers})-3 tanh neural network "
        )
        self.model = MLPClassifier(**params)
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}creating model",
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
        current_generation_id: int,
        should_stop_training: bool,
        generations: int,
        epochs: int,
        enable_tensorboard: bool,
        save_only_improved_models: bool,
    ):
        # TODO update training params
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}Training model"
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

        current_accuracy_train, current_accuracy_test = 0, 0
        if not self.is_new_model:
            current_accuracy_train, current_accuracy_test = self.evaluate_model(
                training_indicator_data=training_indicator_data,
                training_prediction_data=training_prediction_data,
                testing_indicator_data=testing_indicator_data,
                testing_prediction_data=testing_prediction_data,
                epoch_print_prefix="Current Model - ",
            )
        didnt_improve_since_epochs = 0
        for epoch_id in range(epochs):
            if should_stop_training:
                break
            epoch_print_prefix = f"Epoch {epoch_id} - "
            if didnt_improve_since_epochs > n_iter_no_change:
                # load last saved model and stop training
                self.load_model(self.current_model_filename, tentacles_setup_config)
                break
            self.train_model_epoch(
                training_indicator_data=training_indicator_data,
                training_predictions=training_prediction_data,
                epoch_print_prefix=epoch_print_prefix,
                epochs=epochs,
                batch_size=batch_size,
            )
            accuracy_train, accuracy_test = self.evaluate_model(
                training_indicator_data=training_indicator_data,
                training_prediction_data=training_prediction_data,
                testing_indicator_data=testing_indicator_data,
                testing_prediction_data=testing_prediction_data,
                epoch_print_prefix=epoch_print_prefix,
            )
            if current_accuracy_test < accuracy_test:
                didnt_improve_since_epochs = 0
                self.save_model(
                    current_model_filename=self.current_model_filename,
                    tentacles_setup_config=tentacles_setup_config,
                )
                print(
                    f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}Accuracy improve testing data = %0.4f "
                    % current_accuracy_test
                    - accuracy_test
                )
                print(
                    f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}saving model done"
                )
                current_accuracy_test = accuracy_test
            else:
                didnt_improve_since_epochs += 1
                print(
                    f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}Accuracy didnt improve testing data = %0.4f "
                    % accuracy_test
                )
                print(
                    f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}Skip saving model"
                )
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}Training model",
        )

    def train_model_epoch(
        self,
        training_indicator_data,
        training_predictions,
        epoch_print_prefix: str,
        epochs: int,
        batch_size: int,
    ):
        # TODO update training params
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}Training model"
        )
        self.model.fit(
            training_indicator_data,
            training_predictions,
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
    ) -> typing.Tuple[float, float]:
        accuracy_train = self.model.score(
            training_indicator_data, training_prediction_data
        )
        print(
            f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}Accuracy on training data = %0.4f "
            % accuracy_train
        )
        accuracy_test = self.model.score(
            testing_indicator_data, testing_prediction_data
        )
        print(
            f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}Accuracy on testing data = %0.4f "
            % accuracy_test
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
        for indicator_data in full_indicator_data:
            prediction = self.predict_on_single_candle(
                indicators_current_data=indicator_data
            )
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

    def predict_on_single_candle(self, indicators_current_data):
        _indicators_current_data = numpy.array([indicators_current_data])
        probs = self.model.predict_proba(_indicators_current_data)
        prediction = (2 * probs[0][2]) - (2 * probs[0][0])
        # print(f"{self.MESSAGE_PRINT_PREFIX}Prediction pseudo-probs: {probs}")
        return prediction
        # signal = loaded_model.predict(_indicators_current_data)  # -1,0,1
        # print(f"{self.MESSAGE_PRINT_PREFIX}Predicted Signal: {signal}")
        # return signal[0]
