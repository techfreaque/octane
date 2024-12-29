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

import random
from keras import layers, regularizers, Model, backend, utils

from tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets import (
    abstract_tensorflow_neural_net,
    network_utils,
)
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.abstract_neural_net as abstract_neural_net


class TensorflowCnnLstm2(abstract_tensorflow_neural_net.AbstractTensorflowNeuralNet):
    NEURAL_NET_TITLE = "TensorFlow CNN + LSTM V2 (Convolutional Neural Network + Long Short-Term Memory V2)"
    MESSAGE_PRINT_PREFIX = f" {NEURAL_NET_TITLE} - "
    NEURAL_NETS_FOLDER_NAME = "tensorflow_CNN_LSTM2"
    model: Model

    NETWORK_SIZES: list = [
        abstract_neural_net.NETWORK_SIZE_DEEP,
        abstract_neural_net.NETWORK_SIZE_VERY_DEEP,
        abstract_neural_net.NETWORK_SIZE_SUPER_DEEP,
    ]

    def create_model(
        self,
        batch_size: int,
        learning_rate_init: float,
        n_iter_no_change: int,
        features_count: int,
    ) -> None:
        input_shape = (self.max_bars_back, features_count)
        input_layer = layers.Input(shape=input_shape)

        # Convolutional Layers
        conv_layers = layers.Conv1D(filters=32, kernel_size=3, activation="relu")(
            input_layer
        )
        conv_layers = layers.BatchNormalization()(conv_layers)

        # Residual LSTM Layers
        lstm_layers = layers.LSTM(units=32, return_sequences=True)(conv_layers)
        lstm_layers = layers.BatchNormalization()(lstm_layers)

        residual_lstm = layers.LSTM(units=32, return_sequences=True)(lstm_layers)
        residual_lstm = layers.add([lstm_layers, residual_lstm])

        lstm_layers = layers.LSTM(units=64, return_sequences=True)(residual_lstm)
        lstm_layers = layers.BatchNormalization()(lstm_layers)

        residual_lstm = layers.LSTM(units=64, return_sequences=True)(lstm_layers)
        residual_lstm = layers.add([lstm_layers, residual_lstm])

        if self.network_size == abstract_neural_net.NETWORK_SIZE_SUPER_DEEP:
            lstm_layers = layers.LSTM(units=128, return_sequences=True)(residual_lstm)
            lstm_layers = layers.BatchNormalization()(lstm_layers)

            residual_lstm = layers.LSTM(units=128, return_sequences=True)(lstm_layers)
            residual_lstm = layers.add([lstm_layers, residual_lstm])

            lstm_layers = layers.LSTM(units=256, return_sequences=True)(residual_lstm)
            lstm_layers = layers.BatchNormalization()(lstm_layers)

            residual_lstm = layers.LSTM(units=256, return_sequences=True)(lstm_layers)
            residual_lstm = layers.add([lstm_layers, residual_lstm])

            lstm_layers = layers.LSTM(units=512, return_sequences=True)(residual_lstm)
            lstm_layers = layers.BatchNormalization()(lstm_layers)

            lstm_layers = layers.LSTM(units=1024)(lstm_layers)
        elif self.network_size == abstract_neural_net.NETWORK_SIZE_VERY_DEEP:
            lstm_layers = layers.LSTM(units=128, return_sequences=True)(residual_lstm)
            lstm_layers = layers.BatchNormalization()(lstm_layers)

            residual_lstm = layers.LSTM(units=128, return_sequences=True)(lstm_layers)
            residual_lstm = layers.add([lstm_layers, residual_lstm])

            lstm_layers = layers.LSTM(units=256, return_sequences=True)(residual_lstm)
            lstm_layers = layers.BatchNormalization()(lstm_layers)

            lstm_layers = layers.LSTM(units=512)(lstm_layers)
        else:
            lstm_layers = layers.LSTM(units=128, return_sequences=True)(residual_lstm)
            lstm_layers = layers.BatchNormalization()(lstm_layers)

            lstm_layers = layers.LSTM(units=256)(lstm_layers)

        # Attention Mechanism
        attention = layers.Attention()([lstm_layers, lstm_layers])
        attended_lstm = layers.Concatenate()([lstm_layers, attention])

        lstm_layers = layers.BatchNormalization()(attended_lstm)
        lstm_layers = layers.Dropout(0.2)(lstm_layers)

        # Fully Connected Layers
        if self.network_size == abstract_neural_net.NETWORK_SIZE_SUPER_DEEP:
            fc_layers = layers.Dense(512, activation="relu")(lstm_layers)
        elif self.network_size == abstract_neural_net.NETWORK_SIZE_VERY_DEEP:
            fc_layers = layers.Dense(256, activation="relu")(lstm_layers)
        else:
            fc_layers = layers.Dense(128, activation="relu")(lstm_layers)
            fc_layers = layers.Dense(
                128, activation="relu", kernel_regularizer=regularizers.L2()
            )(fc_layers)
        output_layer = layers.Dense(
            3,
            # activation="softmax",
            activation=custom_activation,
        )(fc_layers)

        self.model = Model(inputs=input_layer, outputs=output_layer)


def custom_activation(x):
    # Adjust the output layer activation function
    # randomize long/short/neutral weights
    random_number = random.uniform(0, 1)
    if random_number <= 0.25:
        weights = [1.5, 1, 1.5]  # Higher weight for long/short
    elif random_number <= 0.5:
        weights = [2, 1, 2]  # Higher weight for long/short
    elif random_number <= 0.75:
        weights = [1, 1, 1]  # same weight
    else:
        weights = [1, 1.5, 1]  # Higher weight for neutral
    x = backend.exp(x) * weights
    return x / backend.sum(x, axis=-1, keepdims=True)


utils.get_custom_objects()["custom_activation"] = custom_activation
