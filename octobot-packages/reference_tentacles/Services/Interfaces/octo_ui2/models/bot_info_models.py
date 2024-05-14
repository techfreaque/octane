import typing
import octobot_services.interfaces as interfaces
import tentacles.Services.Interfaces.web_interface.models as models


def get_multi_exchange_info() -> (
    typing.Tuple[bool, typing.List[str], typing.List[str], typing.Dict[str, str]]
):
    exchange_managers = interfaces.AbstractInterface.get_exchange_managers()
    any_exchange_is_futures: bool = False
    exchange_names: typing.List[str] = []
    exchange_ids: typing.List[str] = []
    ids_by_exchange_name: typing.Dict[str, str] = {}
    for exchange_manager in exchange_managers:
        any_exchange_is_futures = any_exchange_is_futures or exchange_manager.is_future
        exchange_names.append(exchange_manager.exchange_name)
        exchange_ids.append(exchange_manager.id)
        ids_by_exchange_name[exchange_manager.exchange_name] = exchange_manager.id
    return (any_exchange_is_futures, exchange_names, exchange_ids, ids_by_exchange_name)


def get_current_exchange_info(
    exchange_name: str, exchange_names: typing.List[str]
) -> typing.Tuple[str, str, typing.List[str], typing.List[str] | None, typing.Any]:
    try:
        (
            exchange_manager,
            _exchange_name,
            exchange_id,
        ) = models.get_first_exchange_data(exchange_name or exchange_names[0])
    except Exception as e:
        raise NoSingleExchangeDataException
    traded_time_frames: typing.List[str] = [
        tf.value for tf in models.get_traded_time_frames(exchange_manager)
    ]
    trigger_time_frames: typing.List[str] | None = None
    if (
        len(exchange_manager.trading_modes)
        and len(exchange_manager.trading_modes[0].producers)
        and hasattr(
            exchange_manager.trading_modes[0].producers[0],
            "trigger_time_frames",
        )
    ):
        trigger_time_frames = (
            exchange_manager.trading_modes[0].producers[0].trigger_time_frames
        )
    # config_candles_count = models.get_config_required_candles_count(
    #     exchange_manager
    # )
    return (
        _exchange_name,
        exchange_id,
        traded_time_frames,
        trigger_time_frames,
        exchange_manager,
    )


class NoSingleExchangeDataException(Exception):
    pass


def get_trading_mode_info(
    exchange_manager,
) -> typing.Tuple[
    typing.Dict[str, typing.Dict[str, str]] | None, typing.List[str] | None, bool, str
]:
    installed_blocks_info: typing.Dict[str, typing.Dict[str, str]] | None = None
    available_api_actions: typing.List[str] | None = None
    real_time_strategies_active: bool = False

    exchange_manager.trading_modes
    trading_mode = exchange_manager.trading_modes[0]

    if hasattr(trading_mode, "block_factory"):
        installed_blocks_info = trading_mode.block_factory.installed_blocks_info
    if hasattr(trading_mode, "AVAILABLE_API_ACTIONS"):
        available_api_actions = trading_mode.AVAILABLE_API_ACTIONS
    if hasattr(trading_mode, "real_time_strategy_data"):
        real_time_strategy_data = trading_mode.real_time_strategy_data
        if real_time_strategy_data:
            real_time_strategies_active = real_time_strategy_data.activated
        # enabled_time_frames = models.get_strategy_required_time_frames(
        #     strategies[0]
        # )

    # enabled_time_frames = (
    #     models.get_strategy_required_time_frames(activated_strategy)
    #     if activated_strategy
    #     else []
    # )
    return (
        installed_blocks_info,
        available_api_actions,
        real_time_strategies_active,
    )
