import os
import typing

import octobot_commons.os_util as os_util
import octobot_commons.logging as logging
import octobot_commons.databases as databases
import octobot_commons.display as commons_display
import octobot_commons.errors as commons_errors
import octobot_trading.api as trading_api
import octobot_services.interfaces.util as interfaces_util
import tentacles.Services.Interfaces.web_interface.plugins as plugins
import tentacles.Services.Interfaces.web_interface.models.trading as trading_model
import tentacles.Meta.Keywords.RunAnalysis.AnalysisModes.default_run_analysis_mode.run_analysis_mode_default as run_analysis_mode_default
import tentacles.Meta.Keywords.RunAnalysis.RunAnalysisFactory.analysis_errors as analysis_errors


class RunAnalysisModePlugin(plugins.AbstractWebInterfacePlugin):
    NAME = "run_analysis_modes"
    PLUGIN_ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))
    DEBUG_PLOTS = os_util.parse_boolean_environment_var("DEBUG_PLOTS", "False")
    RUN_ANALYSIS_MODE: run_analysis_mode_default.DefaultRunAnalysisMode = (
        run_analysis_mode_default.DefaultRunAnalysisMode
    )
    logger: logging.BotLogger = logging.get_logger("RunAnalysisModePlugin")

    def register_routes(self):
        pass
        # plotted_data.register_plot_routes(self)

    @classmethod
    def is_configureable(cls):
        return True

    @classmethod
    def init_user_inputs_from_class(cls, inputs: dict) -> None:
        cls.RUN_ANALYSIS_MODE.init_user_inputs(
            cls=cls.RUN_ANALYSIS_MODE, analysis_mode_plugin=cls, inputs=inputs
        )

    @classmethod
    def get_and_execute_run_analysis_mode(
        cls,
        trading_mode_class,
        exchange_name: str,
        exchange_id: str,
        symbol: str,
        time_frame: str,
        backtesting_id: typing.Optional[int] = None,
        optimizer_id: typing.Optional[int] = None,
        live_id: typing.Optional[int] = None,
        optimization_campaign: typing.Optional[str] = None,
    ):
        config: dict = cls.get_tentacle_config()  # use bt or live settings
        try:
            return interfaces_util.run_in_bot_async_executor(
                cls.RUN_ANALYSIS_MODE.get_and_execute_run_analysis_mode(
                    trading_mode_class=trading_mode_class,
                    config=config,
                    exchange_name=exchange_name,
                    exchange_id=exchange_id,
                    symbol=symbol,
                    time_frame=time_frame,
                    backtesting_id=backtesting_id,
                    optimizer_id=optimizer_id,
                    live_id=live_id,
                    optimization_campaign=optimization_campaign,
                )
            )
        except analysis_errors.LiveMetaDataNotInitializedError as error:
            if cls.DEBUG_PLOTS:
                cls.log_exception(error)
        except Exception as error:
            if cls.DEBUG_PLOTS:
                cls.log_exception(error)
                # TODO remove at some point
            try:
                return interfaces_util.run_in_bot_async_executor(
                    cls.get_old_version_plot_data(
                        exchange_id=exchange_id,
                        trading_mode=trading_mode_class,
                        exchange_name=exchange_name,
                        symbol=symbol,
                        time_frame=time_frame,
                        optimization_campaign_name=optimization_campaign,
                        backtesting_id=backtesting_id,
                        live_id=live_id,
                        optimizer_id=optimizer_id,
                    )
                )
            except Exception:
                pass
        return {}

    def get_tabs(self):
        return []

    @classmethod
    def log_exception(
        cls,
        exception,
        message="Failed to load run analysis plots",
    ):
        cls.logger.exception(exception, True, message + f" - error: {exception}")

    @classmethod
    async def get_old_version_plot_data(
        cls,
        exchange_id,
        trading_mode,
        exchange_name,
        symbol,
        time_frame,
        optimization_campaign_name,
        backtesting_id,
        live_id,
        optimizer_id,
    ):
        try:
            trading_model.ensure_valid_exchange_id(exchange_id)
        except KeyError:
            # frontend will handle this
            return {}
        try:
            elements = commons_display.display_translator_factory()
            database_manager = databases.RunDatabasesIdentifier(
                trading_mode,
                optimization_campaign_name=optimization_campaign_name,
                backtesting_id=backtesting_id,
                live_id=live_id,
                optimizer_id=optimizer_id,
            )
            exchange_manager = trading_api.get_exchange_manager_from_exchange_id(
                exchange_id
            )
            if not exchange_manager.storage_manager.candles_storage.enabled:
                exchange_manager.storage_manager.candles_storage.enabled = True
                await exchange_manager.storage_manager.candles_storage.start()
            await elements.fill_from_database(
                trading_mode,
                database_manager,
                exchange_name,
                symbol,
                time_frame,
                exchange_id,
                with_inputs=backtesting_id is None,
            )
        except commons_errors.DatabaseNotFoundError as error:
            cls.logger.exception(error, True, f"Error when opening database: {error}")
            return {}
        except commons_errors.MissingExchangeDataError as error:
            cls.logger.exception(error, True, f"Error when opening database: {error}")
            return {}
        return elements.to_json()
