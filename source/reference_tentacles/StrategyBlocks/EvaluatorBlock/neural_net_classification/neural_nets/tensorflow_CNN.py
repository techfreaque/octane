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

from tensorflow import keras
from keras import layers, regularizers
from tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets import (
    abstract_tensorflow_neural_net,
)
from tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.abstract_neural_net import (
    NETWORK_SIZE_SUPER_DEEP,
)
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.network_utils as network_utils


class TensorflowCNN(abstract_tensorflow_neural_net.AbstractTensorflowNeuralNet):
    NEURAL_NET_TITLE = "TensorFlow CNN (Convolutional Neural Network)"
    MESSAGE_PRINT_PREFIX = f" {NEURAL_NET_TITLE} - "
    NEURAL_NETS_FOLDER_NAME = "tensorflow_CNN"

    def create_model(
        self,
        batch_size: int,
        learning_rate_init: float,
        n_iter_no_change: int,
        features_count: int,
    ) -> None:
        input_shape = (self.max_bars_back, features_count)
        input_layer = layers.Input(shape=input_shape)

        model_layers = layers.Conv1D(
            filters=32,
            kernel_size=2,
            strides=2,
            activation="relu",
            padding="same",
        )(input_layer)
        model_layers = layers.BatchNormalization()(model_layers)

        model_layers = layers.Conv1D(
            filters=64,
            kernel_size=3,
            strides=2,
            activation="relu",
            padding="same",
        )(model_layers)
        model_layers = layers.BatchNormalization()(model_layers)

        model_layers = layers.Conv1D(
            filters=128,
            kernel_size=5,
            strides=2,
            activation="relu",
            padding="same",
        )(model_layers)
        model_layers = layers.BatchNormalization()(model_layers)

        model_layers = layers.Conv1D(
            filters=256,
            kernel_size=5,
            strides=2,
            activation="relu",
            padding="same",
        )(model_layers)

        if self.network_size == NETWORK_SIZE_SUPER_DEEP:
            model_layers = layers.BatchNormalization()(model_layers)

            model_layers = layers.Conv1D(
                filters=512,
                kernel_size=7,
                strides=2,
                activation="relu",
                padding="same",
            )(model_layers)
            model_layers = layers.BatchNormalization()(model_layers)

            model_layers = layers.Conv1D(
                filters=1024,
                kernel_size=7,
                strides=2,
                activation="relu",
                padding="same",
            )(model_layers)

        model_layers = layers.BatchNormalization()(model_layers)
        model_layers = layers.Dropout(0.2)(model_layers)

        model_layers = layers.Flatten()(model_layers)

        if self.network_size == NETWORK_SIZE_SUPER_DEEP:
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
            activation=network_utils.custom_activation,
        )(model_layers)

        self.model = keras.Model(inputs=input_layer, outputs=output_layer)
