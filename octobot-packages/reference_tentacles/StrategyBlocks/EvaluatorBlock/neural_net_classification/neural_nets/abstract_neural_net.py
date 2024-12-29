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

from __future__ import annotations
import typing
import os
import numpy

import octobot_tentacles_manager.configuration as configuration
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.ml_utils.utils as utils
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.ml_utils.classification_functions.classification_utils as classification_utils
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_net_classification as neural_net_classification
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_net_settings_class as neural_net_settings_class


NETWORK_SIZE_DEEP: str = "Deep"
NETWORK_SIZE_VERY_DEEP: str = "Very deep"
NETWORK_SIZE_SUPER_DEEP: str = "Super deep"


class AbstractNeuralNetwork:
    # override this
    NEURAL_NET_TITLE = "Generic Neural Network"
    MESSAGE_PRINT_PREFIX = f" {NEURAL_NET_TITLE} - "
    NEURAL_NETS_FOLDER_NAME = "generic_net_models"
    NEURAL_NETS_ROOT_FOLDER_NAME = "neural_net_models"
    max_bars_back: int = 1
    is_new_model: bool
    model_folder_path: str
    model_file_path: str
    settings: neural_net_settings_class.NeuralNetClassificationSettings

    NETWORK_SIZES: list = [NETWORK_SIZE_DEEP, NETWORK_SIZE_SUPER_DEEP]

    def __init__(
        self,
        batch_size: int,
        learning_rate_init: float,
        # n_iter_no_change: int,
        tentacles_setup_config,
        feature_names: list,
        max_bars_back: int,
        network_size: str,
        symbols_info: list[str],
    ):
        features_count = len(feature_names)
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"

        print(
            f"{self.MESSAGE_PRINT_PREFIX}Predict singals from {features_count} features"
            f" {feature_names} - with {max_bars_back} bars back for each candle on: {symbols_info}"
        )

        self.load_model(
            tentacles_setup_config=tentacles_setup_config,
            features_count=features_count,
            max_bars_back=max_bars_back,
            network_size=network_size,
        )

    def get_models_folder(self, tentacles_setup_config) -> str:
        user_tentacles_config_folder = configuration.get_user_tentacles_config_folder(
            tentacles_setup_config
        )
        models_root_folder = os.path.join(
            user_tentacles_config_folder, self.NEURAL_NETS_ROOT_FOLDER_NAME
        )
        if not os.path.exists(models_root_folder):
            os.mkdir(models_root_folder)
        self.model_folder_path = os.path.join(
            models_root_folder, self.NEURAL_NETS_FOLDER_NAME
        )
        if not os.path.exists(self.model_folder_path):
            os.mkdir(self.model_folder_path)
        return self.model_folder_path

    def get_model_file_path(
        self, current_model_filename, tentacles_setup_config
    ) -> str:
        self.model_file_path = os.path.join(
            self.get_models_folder(tentacles_setup_config), current_model_filename
        )
        return self.model_file_path

    def save_model(self, current_model_filename, tentacles_setup_config):
        """
        save the model to the disk
        """

    def load_model(
        self,
        tentacles_setup_config,
        features_count: int,
        max_bars_back: int,
        network_size: str,
    ) -> None:
        """
        load an existing model from disk
        """

    def create_model(
        self,
        batch_size: int,
        learning_rate_init: float,
        n_iter_no_change: int,
        features_count: int,
    ) -> None:
        # input shape is (self.max_bars_back, features_count)
        # output shape is (3,)   [long_probability, neutral_probability,short_probability]

        """
        create the model and set to self.model
        """

    async def get_formatted_features_and_training_predictions(
        self,
        neural_net_block: neural_net_classification.NeuralNetClassificationEvaluator,
        training_prediction_target_settings: utils.YTrainSettings,
        indicators_data,
        percent_to_use_as_training_data: int,
    ) -> tuple:
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}formatting data for the network"
        )
        numpy.random.seed(1)
        numpy.set_printoptions(precision=4, suppress=True)
        this_pairs_full_indicator_data = None
        this_pairs_training_prediction_labels = None
        this_pairs_candle_closes = None
        training_indicator_data = []
        training_prediction_data = []
        testing_indicator_data = []
        testing_prediction_data = []
        original_symbol = f"{neural_net_block.block_factory.ctx.symbol}"
        original_time_frame = f"{neural_net_block.block_factory.ctx.time_frame}"
        for key in indicators_data.keys():
            symbol, time_frame = key.split("-")
            neural_net_block.block_factory.ctx.symbol = symbol
            neural_net_block.block_factory.ctx.time_frame = time_frame
            candle_closes = await neural_net_block.get_candles(
                matrix_enums.PriceDataSources.CLOSE.value
            )
            lows = await neural_net_block.get_candles(
                matrix_enums.PriceDataSources.LOW.value
            )
            highs = await neural_net_block.get_candles(
                matrix_enums.PriceDataSources.HIGH.value
            )
            try:
                training_prediction_labels = classification_utils.get_y_train_series(
                    candle_closes,
                    lows,
                    highs,
                    training_prediction_target_settings,
                    raise_missing_data=neural_net_block.block_factory.ctx.exchange_manager.is_backtesting,
                )
            except RuntimeError as error:
                if (
                    not neural_net_block.block_factory.ctx.exchange_manager.is_backtesting
                    and symbol == original_symbol
                    and time_frame == original_time_frame
                ):
                    raise error
                print(
                    f"{self.MESSAGE_PRINT_PREFIX}not enough data for {key}, it will be skipped"
                )
                continue
            (
                _training_indicator_data,
                _training_prediction_data,
                _testing_indicator_data,
                _testing_prediction_data,
                full_indicator_data,
            ) = self.get_training_and_testing_data(
                indicators_data=indicators_data[key],
                prediction_data=training_prediction_labels,
                percent_to_use_as_training_data=percent_to_use_as_training_data,
            )
            training_indicator_data += _training_indicator_data
            training_prediction_data += _training_prediction_data
            testing_indicator_data += _testing_indicator_data
            testing_prediction_data += _testing_prediction_data
            if symbol == original_symbol and time_frame == original_time_frame:
                this_pairs_full_indicator_data = full_indicator_data
                this_pairs_training_prediction_labels = training_prediction_labels
                this_pairs_candle_closes = candle_closes
        neural_net_block.block_factory.ctx.symbol = original_symbol
        neural_net_block.block_factory.ctx.time_frame = original_time_frame
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}formatting data for the network",
        )
        return (
            training_indicator_data,
            training_prediction_data,
            testing_indicator_data,
            testing_prediction_data,
            this_pairs_full_indicator_data,
            this_pairs_training_prediction_labels,
            this_pairs_candle_closes,
        )

    def get_training_and_testing_data(
        self,
        indicators_data: typing.List[tuple],
        prediction_data,
        percent_to_use_as_training_data: float = 60,
    ) -> tuple:
        feature_arrays = [indicator_data[0] for indicator_data in indicators_data]
        cutted_feature_arrays = utilities.cut_data_to_same_len(feature_arrays)
        formatted_data = []
        features_data_length = len(cutted_feature_arrays[0])
        for candle_index in range(features_data_length):
            data_row = []
            for feature_array in cutted_feature_arrays:
                data_row.append(feature_array[candle_index])
            formatted_data.append(data_row)
        cutted_prediction_data, _ = utilities.cut_data_to_same_len(
            (prediction_data, cutted_feature_arrays[0])
        )
        if self.max_bars_back > 1:
            (
                formatted_data,
                cutted_prediction_data,
            ) = _format_as_timeseries_data(
                formatted_data,
                cutted_prediction_data,
                max_bars_back=self.max_bars_back,
            )
        training_data_length = int(
            features_data_length / 100 * percent_to_use_as_training_data
        )
        training_data = formatted_data[:training_data_length]
        testing_data = formatted_data[training_data_length:]

        training_prediction_data = cutted_prediction_data[:training_data_length]
        testing_prediction_data = cutted_prediction_data[training_data_length:]
        return (
            training_data,
            training_prediction_data,
            testing_data,
            testing_prediction_data,
            formatted_data,
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
    ):
        """
        train the model
        """

    def evaluate_model(
        self,
        training_indicator_data,
        training_prediction_data,
        testing_indicator_data,
        testing_prediction_data,
    ):
        """
        score your model
        """

    def predict_on_historical_candles(
        self, full_indicator_data, prediction_side: str, prediction_threshold: float
    ) -> typing.Tuple[list, list]:
        """
        predict and return historical data
        """

    def predict_on_single_candle(self, indicators_current_data):
        """
        predict and return for a single candle
        """


def _format_as_timeseries_data(indicator_data, prediction_data, max_bars_back) -> tuple:
    return utilities.cut_data_to_same_len(
        (
            _add_max_bars_back_history_to_each_bar(indicator_data, max_bars_back),
            _format_prediciton_data_into_tuple(prediction_data),
        )
    )


def _add_max_bars_back_history_to_each_bar(idicators_data, max_bars_back) -> list:
    # TODO improve speed here
    max_bars_back: int = max_bars_back
    return [
        idicators_data[bar - max_bars_back : bar]
        for bar in range(len(idicators_data))
        if bar > max_bars_back
    ]


def _format_prediciton_data_into_tuple(predicitons_data) -> list:
    # TODO improve speed here
    return [
        (
            utils.SignalDirection.tuple_neutral
            if prediction == utils.SignalDirection.neutral
            else utils.SignalDirection.tuple_long
            if prediction == utils.SignalDirection.long
            else utils.SignalDirection.tuple_short
        )
        for prediction in predicitons_data
    ]
