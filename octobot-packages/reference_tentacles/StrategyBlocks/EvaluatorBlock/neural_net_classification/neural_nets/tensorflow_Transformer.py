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
from keras import layers
from tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets import (
    abstract_tensorflow_neural_net,
)

import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.network_utils as network_utils


class TensorflowTransformer(abstract_tensorflow_neural_net.AbstractTensorflowNeuralNet):
    NEURAL_NET_TITLE = "TensorFlow TNN (Transformer Neural Network)"
    MESSAGE_PRINT_PREFIX = f" {NEURAL_NET_TITLE} - "
    NEURAL_NETS_FOLDER_NAME = "tensorflow_Transformer"

    NUM_ENCODER_LAYERS: int = 4  # 2 - 6
    NUM_HEADS: int = 8  # 4, 8, 16
    KEY_DIM: int = 256  # 64 to 512
    FFN_UNITS: int = 512  # 256 to 1024

    def create_model(
        self,
        batch_size: int,
        learning_rate_init: float,
        n_iter_no_change: int,
        features_count: int,
    ) -> None:
        input_shape = (self.max_bars_back, features_count)
        input_layer = layers.Input(shape=input_shape)

        # LSTM layers
        lstm_layers = layers.LSTM(units=64, return_sequences=True)(input_layer)
        lstm_layers = layers.BatchNormalization()(lstm_layers)

        lstm_layers = layers.LSTM(units=64, return_sequences=True)(lstm_layers)
        lstm_layers = layers.BatchNormalization()(lstm_layers)

        # Transformer implementation using self-attention mechanism
        transformer_layers = layers.MultiHeadAttention(
            num_heads=2, key_dim=64, dropout=0.2
        )(lstm_layers, lstm_layers)
        transformer_layers = layers.BatchNormalization()(transformer_layers)

        transformer_layers = layers.GlobalAveragePooling1D()(transformer_layers)

        # Fully connected layers
        fc_layers = layers.Dense(128, activation="relu")(transformer_layers)
        fc_layers = layers.Dense(64, activation="relu")(fc_layers)

        # Output layer
        output_layer = layers.Dense(
            3,
            activation=network_utils.custom_activation,
        )(fc_layers)

        self.model = keras.Model(inputs=input_layer, outputs=output_layer)
