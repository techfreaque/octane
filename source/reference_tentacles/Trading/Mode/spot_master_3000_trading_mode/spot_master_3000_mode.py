import typing
import octobot_commons.logging as logging
import octobot_trading.enums as trading_enums
import octobot_trading.modes.script_keywords.context_management as context_management
import tentacles.Meta.Keywords.basic_tentacles.basic_modes.mode_base.abstract_mode_base as abstract_mode_base
import tentacles.Meta.Keywords.basic_tentacles.basic_modes.scripted_trading_mode.use_scripted_trading_mode as use_scripted_trading_mode
import tentacles.Meta.Keywords.basic_tentacles.basic_modes.spot_master.spot_master_3000_trading_mode as spot_master_3000_trading_mode


class SpotMaster3000Mode(abstract_mode_base.AbstractBaseMode):
    ENABLE_PRO_FEATURES = False

    def __init__(self, config, exchange_manager):
        super().__init__(config, exchange_manager)
        self.producer = SpotMaster3000ModeProducer
        if exchange_manager:
            # allow scripted trading if a
            #   profile_trading_script.py is in the current profile
            use_scripted_trading_mode.initialize_scripted_trading_mode(self)
        else:
            logging.get_logger(self.get_name()).error(
                "At least one exchange must be enabled to use SpotMaster3000Mode"
            )

    def get_mode_producer_classes(self) -> list:
        return [SpotMaster3000ModeProducer]

    @classmethod
    def get_supported_exchange_types(cls) -> list:
        """
        :return: The list of supported exchange types
        """
        return [
            trading_enums.ExchangeTypes.SPOT,
        ]


class SpotMaster3000ModeProducer(spot_master_3000_trading_mode.SpotMaster3000Making):
    async def make_strategy(
        self,
        ctx: context_management.Context,
        action: str,
        action_data: typing.Optional[dict] = None,
    ):
        self.action = action
        await self.execute_rebalancing_strategy(ctx)
