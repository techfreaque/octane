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


class TensorflowCnnLstm(TensorflowRNN):
    NEURAL_NET_TITLE = (
        "TensorFlow CNN + LSTM (Convolutional Neural Network + Long Short-Term Memory)"
    )
    MESSAGE_PRINT_PREFIX = f" {NEURAL_NET_TITLE} - "
    NEURAL_NETS_FOLDER_NAME = "tensorflow_CNN_LSTM"
    super_deep_network: bool = False

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

        # CNN Layers
        conv1 = layers.Conv1D(64, kernel_size=3, activation="relu")(input_layer)
        conv2 = layers.Conv1D(128, kernel_size=3, activation="relu")(conv1)
        conv3 = layers.Conv1D(256, kernel_size=3, activation="relu")(conv2)
        pool1 = layers.MaxPooling1D(pool_size=2)(conv3)

        # LSTM Layers
        lstm1 = layers.LSTM(128, return_sequences=True)(pool1)
        lstm2 = layers.LSTM(128, return_sequences=True)(lstm1)
        lstm3 = layers.LSTM(128)(lstm2)

        # Fully Connected Layers
        dense1 = layers.Dense(256, activation="relu")(lstm3)
        dense2 = layers.Dense(128, activation="relu")(dense1)

        # Output Layer
        output_layer = layers.Dense(
            3,
            # activation='softmax'
            activation=custom_activation,
        )(dense2)

        self.model = keras.Model(inputs=input_layer, outputs=output_layer)
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}creating model",
        )
