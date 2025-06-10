import typing

import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.ml_utils.utils as utils


class NeuralNetClassificationSettings:
    def __init__(
        self,
        training_prediction_target_settings: utils.YTrainSettings,
        batch_size: int,
        learning_rate_init: float,
        generations: int,
        epochs: int,
        max_bars_back: int,
        # save_only_improved_models: bool,
        prediction_side: str,
        enable_backtest_while_trainig: bool,
        prediction_threshold: float,
        plot_training_predictions: bool,
        plot_neural_net_predictions: bool,
        enable_training: bool,
        plot_opposite_signal_side: bool,
        enable_tensorboard: bool,
        network_size: str,
        evaluate_model_before: bool,
        save_model_based_on: str,
        # n_iter_no_change: typing.Optional[int] = None,
        symbols: typing.Optional[typing.Set[str]] = None,
        time_frames: typing.Optional[typing.Set[str]] = None,
    ) -> None:
        self.training_prediction_target_settings: utils.YTrainSettings = (
            training_prediction_target_settings
        )
        self.enable_backtest_while_trainig = enable_backtest_while_trainig
        self.save_model_based_on: int = save_model_based_on
        self.batch_size: int = batch_size
        self.max_bars_back: int = max_bars_back
        # self.n_iter_no_change: typing.Optional[int] = n_iter_no_change
        self.enable_training: bool = enable_training
        self.learning_rate_init: float = learning_rate_init
        self.generations: int = generations
        self.epochs: int = epochs
        # self.save_only_improved_models: bool = save_only_improved_models
        self.network_size: str = network_size
        self.prediction_side: str = prediction_side
        self.prediction_threshold: float = prediction_threshold
        self.plot_training_predictions: bool = plot_training_predictions
        self.evaluate_model_before: bool = evaluate_model_before
        self.plot_neural_net_predictions: bool = plot_neural_net_predictions
        self.plot_opposite_signal_side: bool = plot_opposite_signal_side
        self.enable_tensorboard: bool = enable_tensorboard
        self.symbols: typing.Optional[typing.Set[str]] = symbols
        self.time_frames: typing.Optional[typing.Set[str]] = time_frames


class SignalTypes:
    SHORT = "Short"
    NEUTRAL = "Neutral"
    LONG = "Long"


class SaveModelBasedOn:
    LOSS = "loss"
    VAL_LOSS = "val_loss"
    SAVE_ALL = "save_all"
