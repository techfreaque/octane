class NeuralNetClassificationSettings:
    def __init__(
        self,
        selected_indicator_ids,
        training_prediction_target_settings,
        batch_size,
        learning_rate_init,
        n_iter_no_change,
        enable_training,
        generations,
        epochs,
        save_only_improved_models,
        prediction_side,
        prediction_threshold,
        plot_training_predictions,
        plot_neural_net_predictions,
        feature_names,
        plot_opposite_signal_side: bool,
        enable_tensorboard: bool,
    ) -> None:
        self.selected_indicator_ids = selected_indicator_ids
        self.feature_names = feature_names
        self.training_prediction_target_settings = training_prediction_target_settings
        self.batch_size = batch_size
        self.n_iter_no_change = n_iter_no_change
        self.enable_training = enable_training
        self.learning_rate_init = learning_rate_init
        self.generations = generations
        self.epochs = epochs
        self.save_only_improved_models = save_only_improved_models
        self.prediction_side = prediction_side
        self.prediction_threshold = prediction_threshold
        self.plot_training_predictions = plot_training_predictions
        self.plot_neural_net_predictions = plot_neural_net_predictions
        self.plot_opposite_signal_side: bool = plot_opposite_signal_side
        self.enable_tensorboard: bool = enable_tensorboard


class SignalTypes:
    SHORT = "Short"
    NEUTRAL = "Neutral"
    LONG = "Long"
