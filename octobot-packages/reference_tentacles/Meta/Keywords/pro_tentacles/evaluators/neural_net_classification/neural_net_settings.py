import octobot_commons.enums as common_enums


from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.ml_utils import (
    utils,
)

from tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.user_inputs2.user_input2_ import (
    user_input2,
)
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.available_neural_nets import (
    NEURAL_NETS,
)

from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_net_settings_class import (
    NeuralNetClassificationSettings,
    SignalTypes,
)
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.abstract_neural_net import (
    AbstractNeuralNetwork,
)
from tentacles.Meta.Keywords.pro_tentacles.indicators.indicator_handling import (
    activate_multiple_configurable_indicators,
)
from tentacles.Meta.Keywords.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    allow_enable_plot,
)


async def get_neural_network_with_config(maker, evaluator) -> AbstractNeuralNetwork:
    network_types_list = list(NEURAL_NETS.keys())
    network_type = await user_input2(
        maker,
        evaluator,
        name="network_type",
        input_type=common_enums.UserInputTypes.OPTIONS.value,
        def_val=network_types_list[0],
        options=network_types_list,
        title="Neural Net Type",
        grid_columns=12,
    )
    NeuralNetwork: AbstractNeuralNetwork = NEURAL_NETS.get(
        network_type, NEURAL_NETS[network_types_list[0]]
    )
    MESSAGE_PRINT_PREFIX = f" {network_type} - "

    training_settings_name = "training_settings"
    await user_input2(
        maker,
        evaluator,
        name=training_settings_name,
        input_type=common_enums.UserInputTypes.OBJECT.value,
        def_val=None,
        title="Training Settings",
        grid_columns=12,
        editor_options={
            common_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
            common_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
        },
    )
    training_settings_parent_input_name = (
        f"{evaluator.config_path_short}_{training_settings_name}"
    )
    prediction_settings_name = "prediction_settings"
    await user_input2(
        maker,
        evaluator,
        name=prediction_settings_name,
        input_type=common_enums.UserInputTypes.OBJECT.value,
        def_val=None,
        title="Prediction Settings",
        grid_columns=12,
        editor_options={
            common_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
            common_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
        },
    )
    prediction_settings_parent_input_name = (
        f"{evaluator.config_path_short}_{prediction_settings_name}"
    )
    display_settings_name = "display_settings"
    await user_input2(
        maker,
        evaluator,
        name=display_settings_name,
        input_type=common_enums.UserInputTypes.OBJECT.value,
        def_val=None,
        title="Display Settings",
        grid_columns=12,
        editor_options={
            common_enums.UserInputEditorOptionsTypes.COLLAPSED.value: True,
            common_enums.UserInputEditorOptionsTypes.DISABLE_COLLAPSE.value: False,
        },
    )
    display_settings_parent_input_name = (
        f"{evaluator.config_path_short}_{display_settings_name}"
    )
    prediction_side = await user_input2(
        maker,
        evaluator,
        name="prediction_side",
        input_type=common_enums.UserInputTypes.OPTIONS.value,
        def_val=SignalTypes.LONG,
        options=[SignalTypes.LONG, SignalTypes.SHORT],
        title="Prediction side",
        grid_columns=6,
        parent_input_name=prediction_settings_parent_input_name,
    )
    plot_opposite_signal_side = await user_input2(
        maker,
        evaluator,
        name="plot_opposite_signal_side",
        input_type=common_enums.UserInputTypes.BOOLEAN.value,
        def_val=False,
        title="also Plot other sides signals",
        grid_columns=6,
        parent_input_name=display_settings_parent_input_name,
    )
    enable_training = await user_input2(
        maker,
        evaluator,
        name="enable_training",
        input_type=common_enums.UserInputTypes.BOOLEAN.value,
        def_val=True,
        title="Enable neural net training in backtesting mode",
        grid_columns=6,
        parent_input_name=training_settings_parent_input_name,
    )
    prediction_threshold: float = await user_input2(
        maker,
        evaluator,
        name="prediction_threshold",
        input_type=common_enums.UserInputTypes.FLOAT.value,
        def_val=80,
        min_val=0,
        max_val=100,
        title="Prediction threshold",
        description=(
            "A prediction will have a certianty that ranges from 0 - 100. "
            "If you set this threshold to 80, the prediction must be at least 80%."
        ),
        grid_columns=6,
        parent_input_name=prediction_settings_parent_input_name,
    )
    batch_size: float = await user_input2(
        maker,
        evaluator,
        name="batch_size",
        input_type=common_enums.UserInputTypes.INT.value,
        def_val=10,
        min_val=0,
        max_val=100,
        title="Batch size",
        description=(
            "We divide the training set into batches (number of samples). The "
            "batch_size is the sample size (number of training instances "
            "each batch contains)"
        ),
        grid_columns=6,
        parent_input_name=training_settings_parent_input_name,
    )
    learning_rate_init: float = await user_input2(
        maker,
        evaluator,
        name="learning_rate_init",
        input_type=common_enums.UserInputTypes.FLOAT.value,
        def_val=0.001,
        min_val=0,
        title="Learning Rate",
        grid_columns=6,
        parent_input_name=training_settings_parent_input_name,
    )
    n_iter_no_change: float = await user_input2(
        maker,
        evaluator,
        name="n_iter_no_change",
        input_type=common_enums.UserInputTypes.INT.value,
        def_val=3,
        min_val=0,
        max_val=100,
        title="Stop training after n generations without accuracy improvement",
        grid_columns=6,
        parent_input_name=training_settings_parent_input_name,
    )
    generations: float = await user_input2(
        maker,
        evaluator,
        name="generations",
        input_type=common_enums.UserInputTypes.INT.value,
        def_val=1,
        min_val=1,
        title="Generations to train",
        description=(
            "A generation consists of multiple epochs and marks as a "
            "checkpoint for the model. If the accuracy improved, the model will "
            "get saved after each generation"
        ),
        # description="A generation takes ~1 minutes to train, depending on the amount of historical data selected",
        grid_columns=6,
        parent_input_name=training_settings_parent_input_name,
    )
    epochs: float = await user_input2(
        maker,
        evaluator,
        name="epochs",
        input_type=common_enums.UserInputTypes.INT.value,
        def_val=5,
        min_val=1,
        title="Epochs to train in each generation",
        grid_columns=6,
        parent_input_name=training_settings_parent_input_name,
    )
    save_only_improved_models = await user_input2(
        maker,
        evaluator,
        name="save_only_improved_models",
        input_type=common_enums.UserInputTypes.BOOLEAN.value,
        def_val=True,
        title="Only save models for generations that improved in accuracy",
        grid_columns=6,
        parent_input_name=training_settings_parent_input_name,
    )
    training_prediction_target_settings = utils.YTrainSettings(
        training_data_type=utils.YTrainTypes.IS_WINNING_TRADE,
        percent_for_a_win=await user_input2(
            maker,
            evaluator,
            name="percent_target_for_win",
            input_type=common_enums.UserInputTypes.FLOAT.value,
            def_val=3,
            min_val=0,
            max_val=100,
            title="Percent target to count as a win",
            grid_columns=6,
            parent_input_name=training_settings_parent_input_name,
        ),
        percent_for_a_loss=await user_input2(
            maker,
            evaluator,
            name="percent_target_for_loss",
            input_type=common_enums.UserInputTypes.FLOAT.value,
            def_val=1.5,
            min_val=0,
            max_val=100,
            title="Percent target to count as a loss",
            grid_columns=6,
            parent_input_name=training_settings_parent_input_name,
        ),
    )
    await allow_enable_plot(
        maker,
        evaluator,
        "Plot neural net signals",
        parent_input_name=display_settings_parent_input_name,
    )
    plot_training_predictions = await user_input2(
        maker,
        evaluator,
        name="plot_training_predictions",
        input_type=common_enums.UserInputTypes.BOOLEAN.value,
        def_val=False,
        title="Plot training predictions",
        grid_columns=6,
        parent_input_name=display_settings_parent_input_name,
    )
    plot_neural_net_predictions = await user_input2(
        maker,
        evaluator,
        name="plot_neural_net_predictions",
        input_type=common_enums.UserInputTypes.BOOLEAN.value,
        def_val=False,
        title="Plot neural net predictions",
        grid_columns=6,
        parent_input_name=display_settings_parent_input_name,
    )
    enable_tensorboard = await user_input2(
        maker,
        evaluator,
        name="enable_tensorboard",
        input_type=common_enums.UserInputTypes.BOOLEAN.value,
        def_val=False,
        title="Enable tensorboard logging",
        description=(
            "Execute the following to start the tensorboard dashboard: \n"
            "tensorboard --logdir user/profiles/Profile-Name/specific_config"
            "/neural_net_models/tensorflow_CNN_LSTM"
        ),
        grid_columns=6,
        parent_input_name=display_settings_parent_input_name,
    )
    (
        selected_indicator_titles,
        selected_indicator_ids,
    ) = await activate_multiple_configurable_indicators(
        maker,
        evaluator,
        data_source_name="Model Input Feature",
        def_val=["EMA"],
        indicator_group_id=1,
    )
    neural_net_settings: NeuralNetClassificationSettings = (
        NeuralNetClassificationSettings(
            selected_indicator_ids=selected_indicator_ids,
            training_prediction_target_settings=training_prediction_target_settings,
            batch_size=batch_size,
            learning_rate_init=learning_rate_init,
            n_iter_no_change=n_iter_no_change,
            enable_training=enable_training,
            generations=generations,
            epochs=epochs,
            save_only_improved_models=save_only_improved_models,
            prediction_side=prediction_side,
            prediction_threshold=prediction_threshold,
            plot_training_predictions=plot_training_predictions,
            plot_neural_net_predictions=plot_neural_net_predictions,
            feature_names=selected_indicator_titles,
            plot_opposite_signal_side=plot_opposite_signal_side,
            enable_tensorboard=enable_tensorboard,
        )
    )
    return NeuralNetwork, neural_net_settings
