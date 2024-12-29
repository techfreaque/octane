import asyncio
import threading
import decimal

import octobot.enums as enums
import octobot.constants as constants
import octobot.api as octobot_api
import octobot_services.interfaces.util as interfaces_util
import octobot_commons.logging as bot_logging
import octobot_backtesting.api as backtesting_api
import octobot.strategy_optimizer.optimizer_settings as optimizer_settings
import octobot.strategy_optimizer as octobot_strategy_optimizer
import tentacles.Services.Interfaces.web_interface.constants as web_interface_constants
import tentacles.Services.Interfaces.web_interface as web_interface_root
import tentacles.Services.Interfaces.web_interface.models.backtesting as backtesting_model
import tentacles.Services.Interfaces.web_interface.models.trading as trading_model

import tentacles.Services.Interfaces.octo_ui2.utils.basic_utils as basic_utils
import tentacles.Services.Interfaces.octo_ui2_pro.octo_ui2_pro_plugin as octo_ui2_pro_plugin


def get_optimizer_queue(trading_mode):
    return basic_utils.get_response(
        data=_get_optimizer_queue(trading_mode),
        message="Successfully fetched optimizer queue",
    )


def _get_optimizer_queue(trading_mode):
    return interfaces_util.run_in_bot_async_executor(
        octobot_api.get_design_strategy_optimizer_queue(trading_mode)
    )


def handle_queue_update_fail(error):
    octo_ui2_pro_plugin.O_UI_Pro.logger.exception(
        error, True, "Failed to update the optimizer queue"
    )
    return basic_utils.get_response(
        success=False, message=f"Failed to update optimizer queue, error: {error}"
    )


def handle_start_fail(error):
    octo_ui2_pro_plugin.O_UI_Pro.logger.exception(
        error, True, "Failed to start the optimizer"
    )
    return basic_utils.get_response(
        success=False, message=f"Failed to start the optimizer, error: {error}"
    )


def start_strategy_design_optimizer(
    trading_mode,
    request_data: dict,
    collector_start_callback=None,
    start_callback=None,
):
    _optimizer_settings = CustomOptimizerSettings(request_data)
    for exchange_id in _optimizer_settings.exchange_ids:
        trading_model.ensure_valid_exchange_id(exchange_id)
    tools = web_interface_root.WebInterface.tools
    optimizer = tools[web_interface_constants.BOT_TOOLS_STRATEGY_OPTIMIZER]
    if optimizer is not None and octobot_api.is_optimizer_computing(optimizer):
        return basic_utils.get_response(
            success=False, message="Optimizer is already running"
        )
    current_collectors = tools[web_interface_constants.BOT_TOOLS_DATA_COLLECTOR]
    if current_collectors:
        return basic_utils.get_response(
            success=False, message="A data collector is already running"
        )
    previous_independent_backtesting = tools[
        web_interface_constants.BOT_TOOLS_BACKTESTING
    ]
    has_backtesting = (
        previous_independent_backtesting
        and octobot_api.is_independent_backtesting_in_progress(
            previous_independent_backtesting
        )
    )
    if _optimizer_settings.data_files == [CONFIG_CURRENT_BOT_DATA]:
        if has_backtesting:
            _optimizer_settings.data_files = []
        else:
            web_interface_root.WebInterface.tools[
                web_interface_constants.BOT_TOOLS_DATA_COLLECTOR
            ] = []
            _optimizer_settings.data_files = None
        for exchange_id in _optimizer_settings.exchange_ids:
            if has_backtesting:
                _optimizer_settings.data_files.append(
                    backtesting_model.get_data_files_from_current_bot(
                        exchange_id,
                        _optimizer_settings.start_timestamp,
                        _optimizer_settings.end_timestamp,
                        collect=False,
                    )
                )
            else:
                web_interface_root.WebInterface.tools[
                    web_interface_constants.BOT_TOOLS_DATA_COLLECTOR
                ].append(
                    backtesting_model.create_snapshot_data_collector(
                        exchange_id,
                        _optimizer_settings.start_timestamp,
                        _optimizer_settings.end_timestamp,
                    )
                )
    else:
        _optimizer_settings.data_files = _optimizer_settings.data_files
    thread = threading.Thread(
        target=asyncio.run,
        args=(
            _collect_initialize_and_run_strategy_design_optimizer(
                trading_mode,
                _optimizer_settings,
                collector_start_callback,
                start_callback,
            ),
        ),
        name=f"{octobot_strategy_optimizer.StrategyDesignOptimizer.__name__}-WebInterface-runner",
    )
    thread.start()
    return basic_utils.get_response(message="Strategy optimizer is starting")


async def _collect_initialize_and_run_strategy_design_optimizer(
    trading_mode, _optimizer_settings, collector_start_callback, start_callback
):
    try:
        # run in bot main loop to use the existing exchange connection
        if not _optimizer_settings.data_files:
            collector_start_callback()
            _optimizer_settings.data_files = []
            for data_collector in web_interface_root.WebInterface.tools[
                web_interface_constants.BOT_TOOLS_DATA_COLLECTOR
            ]:
                _optimizer_settings.data_files.append(
                    interfaces_util.run_in_bot_main_loop(
                        backtesting_api.initialize_and_run_data_collector(
                            data_collector,
                        ),
                        timeout=backtesting_model.DATA_COLLECTOR_TIMEOUT,
                    )
                )
        try:
            temp_independent_backtesting = octobot_api.create_independent_backtesting(
                interfaces_util.get_edited_config(), None, []
            )
            temp_independent_backtesting.backtesting_config = (
                temp_independent_backtesting.backtesting_config
            )
            optimizer_config = (
                await octobot_api.initialize_independent_backtesting_config(
                    temp_independent_backtesting
                )
            )
            optimizer = octobot_api.create_design_strategy_optimizer(
                trading_mode=trading_mode,
                optimizer_settings=_optimizer_settings,
                config=optimizer_config,
                tentacles_setup_config=interfaces_util.get_bot_api().get_edited_tentacles_config(),
            )
            web_interface_root.WebInterface.tools[
                web_interface_constants.BOT_TOOLS_STRATEGY_OPTIMIZER
            ] = optimizer
            # release data collector
            web_interface_root.WebInterface.tools[
                web_interface_constants.BOT_TOOLS_DATA_COLLECTOR
            ] = None
            _optimizer_settings.start_timestamp = (
                _optimizer_settings.start_timestamp / 1000
                if _optimizer_settings.start_timestamp
                else None
            )
            _optimizer_settings.end_timestamp = (
                _optimizer_settings.end_timestamp / 1000
                if _optimizer_settings.end_timestamp
                else None
            )
            if start_callback:
                start_callback()
            await octobot_api.resume_design_strategy_optimizer(
                optimizer,
                _optimizer_settings,
            )
        except Exception as e:
            bot_logging.get_logger("StartStrategyOptimizerModel").exception(
                e, True, f"Error when initializing strategy optimizer: {e}"
            )
        finally:
            web_interface_root.WebInterface.tools[
                web_interface_constants.BOT_TOOLS_STRATEGY_OPTIMIZER
            ] = None
    except Exception as e:
        bot_logging.get_logger("DataCollectorModel").exception(
            e, True, f"Error when collecting historical data: {e}"
        )
        return
    finally:
        web_interface_root.WebInterface.tools[
            web_interface_constants.BOT_TOOLS_DATA_COLLECTOR
        ] = None


def update_optimizer_queue(request_data, trading_mode):
    interfaces_util.run_in_bot_async_executor(
        octobot_api.update_design_strategy_optimizer_queue(
            trading_mode, request_data["updatedQueue"]
        )
    )
    return basic_utils.get_response(
        message="Successfully updated the optimizer queue",
    )


def add_to_optimizer_queue(request_data, trading_mode):
    runs = interfaces_util.run_in_bot_async_executor(
        octobot_api.generate_and_save_strategy_optimizer_runs(
            trading_mode,
            interfaces_util.get_bot_api().get_edited_tentacles_config(),
            CustomOptimizerSettings(request_data),
        )
    )
    if (
        optimizer := get_optimizer()
    ) is not None and octobot_api.is_optimizer_computing(optimizer):
        octobot_api.update_strategy_optimizer_total_runs(optimizer, runs)
    return basic_utils.get_response(
        message=f"Successfully added {len(runs) if runs else ''} runs"
    )


def get_optimizer():
    return web_interface_root.WebInterface.tools[
        web_interface_constants.BOT_TOOLS_STRATEGY_OPTIMIZER
    ]


# TODO remove when merged

EXCHANGE_IDS = "exchange_ids"
EXCHANGE_ID = "exchange_id"
CONFIG_CURRENT_BOT_DATA = "current_bot_data"
OPTIMIZER_DEFAULT_RANDOMLY_CHOSE_RUNS = True
OPTIMIZER_DEFAULT_QUEUE_SIZE = 10000
OPTIMIZER_DEFAULT_DB_UPDATE_PERIOD = 15
OPTIMIZER_DEFAULT_TARGET_FITNESS_SCORE = None


class CustomOptimizerSettings(optimizer_settings.OptimizerSettings):
    def __init__(self, settings_dict=None):
        if settings_dict is None:
            settings_dict = {}
        # generic
        self.exchange_ids = settings_dict.get(
            EXCHANGE_IDS,
        )
        if not self.exchange_ids:
            self.exchange_ids = [settings_dict.get(EXCHANGE_ID)]

        self.exchange_type = settings_dict.get(
            enums.OptimizerConfig.EXCHANGE_TYPE.value
        )
        self.optimizer_config = (
            settings_dict.get(enums.OptimizerConfig.OPTIMIZER_CONFIG.value) or None
        )
        self.randomly_chose_runs = (
            settings_dict.get(enums.OptimizerConfig.RANDOMLY_CHOSE_RUNS.value)
            or OPTIMIZER_DEFAULT_RANDOMLY_CHOSE_RUNS
        )

        self.data_files = settings_dict.get(
            enums.OptimizerConfig.DATA_FILES.value,
            [CONFIG_CURRENT_BOT_DATA],
        )
        if not isinstance(self.data_files, list):
            self.data_files = [self.data_files]
        if CONFIG_CURRENT_BOT_DATA in self.data_files:
            self.data_files = [CONFIG_CURRENT_BOT_DATA]
        self.start_timestamp = settings_dict.get(
            enums.OptimizerConfig.START_TIMESTAMP.value, None
        )
        self.end_timestamp = settings_dict.get(
            enums.OptimizerConfig.END_TIMESTAMP.value, None
        )
        self.required_idle_cores = int(
            settings_dict.get(enums.OptimizerConfig.IDLE_CORES.value)
            or constants.OPTIMIZER_DEFAULT_REQUIRED_IDLE_CORES
        )
        self.notify_when_complete = (
            settings_dict.get(enums.OptimizerConfig.NOTIFY_WHEN_COMPLETE.value)
            or constants.OPTIMIZER_DEFAULT_NOTIFY_WHEN_COMPLETE
        )
        self.optimizer_mode = settings_dict.get(
            enums.OptimizerConfig.MODE.value, enums.OptimizerModes.NORMAL.value
        )
        optimizer_id = settings_dict.get(enums.OptimizerConfig.OPTIMIZER_ID.value, 1)
        self.optimizer_id = optimizer_id if optimizer_id is None else int(optimizer_id)
        self.optimizer_ids = settings_dict.get(
            enums.OptimizerConfig.OPTIMIZER_IDS.value
        )
        self.optimizer_mode = settings_dict.get(
            enums.OptimizerConfig.MODE.value, enums.OptimizerModes.NORMAL.value
        )
        self.queue_size = int(
            settings_dict.get(
                enums.OptimizerConfig.QUEUE_SIZE.value,
                OPTIMIZER_DEFAULT_QUEUE_SIZE,
            )
        )
        self.empty_the_queue = settings_dict.get(
            enums.OptimizerConfig.EMPTY_THE_QUEUE.value, False
        )
        # update run database at the end of each period
        self.db_update_period = int(
            settings_dict.get(enums.OptimizerConfig.DB_UPDATE_PERIOD.value)
            or OPTIMIZER_DEFAULT_DB_UPDATE_PERIOD
        )
        # AI / genetic
        self.max_optimizer_runs = (
            settings_dict.get(enums.OptimizerConfig.MAX_OPTIMIZER_RUNS.value)
            or constants.OPTIMIZER_DEFAULT_MAX_OPTIMIZER_RUNS
        )
        self.generations_count = (
            settings_dict.get(enums.OptimizerConfig.DEFAULT_GENERATIONS_COUNT.value)
            or constants.OPTIMIZER_DEFAULT_GENERATIONS_COUNT
        )
        self.initial_generation_count = (
            settings_dict.get(enums.OptimizerConfig.INITIAL_GENERATION_COUNT.value)
            or constants.OPTIMIZER_DEFAULT_INITIAL_GENERATION_COUNT
        )
        self.run_per_generation = (
            settings_dict.get(enums.OptimizerConfig.DEFAULT_RUN_PER_GENERATION.value)
            or constants.OPTIMIZER_DEFAULT_RUN_PER_GENERATION
        )
        self.fitness_parameters = self.parse_fitness_parameters(
            settings_dict.get(enums.OptimizerConfig.DEFAULT_SCORING_PARAMETERS.value)
            or self.get_default_fitness_parameters()
        )

        self.exclude_filters = self.parse_optimizer_filter(
            settings_dict.get(enums.OptimizerConfig.DEFAULT_OPTIMIZER_FILTERS.value)
            or self.get_default_optimizer_filters()
        )

        self.constraints_by_key = self.parse_optimizer_constraint(
            settings_dict.get(enums.OptimizerConfig.DEFAULT_OPTIMIZER_CONSTRAINTS.value)
            or self.get_default_optimizer_constraints()
        )

        self.mutation_percent = float(
            settings_dict.get(enums.OptimizerConfig.DEFAULT_MUTATION_PERCENT.value)
            or constants.OPTIMIZER_DEFAULT_MUTATION_PERCENT
        )
        self.max_mutation_probability_percent = decimal.Decimal(
            settings_dict.get(
                enums.OptimizerConfig.MAX_MUTATION_PROBABILITY_PERCENT.value
            )
            or constants.OPTIMIZER_DEFAULT_MAX_MUTATION_PROBABILITY_PERCENT
        )
        self.min_mutation_probability_percent = decimal.Decimal(
            settings_dict.get(
                enums.OptimizerConfig.MIN_MUTATION_PROBABILITY_PERCENT.value
            )
            or constants.OPTIMIZER_DEFAULT_MIN_MUTATION_PROBABILITY_PERCENT
        )
        self.max_mutation_number_multiplier = decimal.Decimal(
            settings_dict.get(
                enums.OptimizerConfig.DEFAULT_MAX_MUTATION_NUMBER_MULTIPLIER.value
            )
            or constants.OPTIMIZER_DEFAULT_MAX_MUTATION_NUMBER_MULTIPLIER
        )
        self.target_fitness_score = (
            settings_dict.get(enums.OptimizerConfig.TARGET_FITNESS_SCORE.value)
            or OPTIMIZER_DEFAULT_TARGET_FITNESS_SCORE
        )
        self.stay_within_boundaries = (
            settings_dict.get(enums.OptimizerConfig.STAY_WITHIN_BOUNDARIES.value)
            or False
        )
