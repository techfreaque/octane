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
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.network_utils import (
    custom_activation,
)
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.tensorflow_RNN import (
    TensorflowRNN,
)


class TensorflowTransformer(TensorflowRNN):
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
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}creating model"
        )

        input_shape = (self.MAX_BARS_BACK, features_count)
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
            activation=custom_activation,
        )(fc_layers)

        self.model = keras.Model(inputs=input_layer, outputs=output_layer)
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}creating model",
        )

    def compile_model(self, learning_rate_init):
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate_init)
        self.model.compile(
            optimizer=optimizer,
            loss=keras.losses.MeanSquaredError(),
            metrics=[
                keras.metrics.CategoricalAccuracy(),
                keras.metrics.AUC(),
                # keras.metrics.Precision(),
                # keras.metrics.Recall(),
            ],
        )
