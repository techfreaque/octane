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


import octobot_commons.enums as commons_enums
import octobot_trading.enums as trading_enums
import octobot_services.enums as services_enum
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.abstract_action_block as abstract_action_block
import tentacles.Meta.Keywords.scripting_library.alerts.notifications as notifications


class SendAlertAction(abstract_action_block.ActionBlock):
    NAME = "send_alert"
    TITLE = "Send Alert"
    TITLE_SHORT = TITLE
    DESCRIPTION = "Send an alert to your connected notification services"
    SUPPORTED_VARIABLES_INFO = "{exchange} {symbol} {time_frame} {candle_open} {candle_high} {candle_low} {candle_close}"

    alert_title: str
    alert_content: str
    alert_level: str

    def init_block_settings(self) -> None:
        self.alert_title = self.user_input(
            "alert_title",
            commons_enums.UserInputTypes.TEXT.value,
            "Alert on {symbol} {time_frame} {candle_close}",
            title="Alert Title",
            options=[
                trading_enums.TradeOrderSide.BUY.value,
                trading_enums.TradeOrderSide.SELL.value,
            ],
            description=f"Allowed variables: {self.SUPPORTED_VARIABLES_INFO}",
        )
        self.alert_content = self.user_input(
            "alert_content",
            commons_enums.UserInputTypes.TEXT.value,
            f"Alert on {self.SUPPORTED_VARIABLES_INFO}",
            title="Alert content",
            description=f"Allowed variables: {self.SUPPORTED_VARIABLES_INFO}",
        )
        self.alert_level = self.user_input(
            "alert_level",
            commons_enums.UserInputTypes.OPTIONS.value,
            def_val=services_enum.NotificationLevel.INFO.value,
            options=[level.value for level in services_enum.NotificationLevel],
            title="Alert Level",
        )

    async def execute_block(
        self,
    ) -> None:
        if not self.block_factory.ctx.exchange_manager.is_backtesting:
            exchange = self.block_factory.ctx.exchange_name
            symbol = self.block_factory.ctx.symbol
            time_frame = self.block_factory.ctx.time_frame
            candle_open = (
                await self.get_candles(matrix_enums.PriceDataSources.OPEN.value)
            )[-1]
            candle_high = (
                await self.get_candles(matrix_enums.PriceDataSources.HIGH.value)
            )[-1]
            candle_low = (
                await self.get_candles(matrix_enums.PriceDataSources.LOW.value)
            )[-1]
            candle_close = (
                await self.get_candles(matrix_enums.PriceDataSources.CLOSE.value)
            )[-1]
            await notifications.send_alert(
                title=self.alert_title.format(
                    exchange=exchange,
                    symbol=symbol,
                    time_frame=time_frame,
                    candle_close=candle_close,
                    candle_open=candle_open,
                    candle_high=candle_high,
                    candle_low=candle_low,
                ),
                alert_content=self.alert_content.format(
                    exchange=exchange,
                    symbol=symbol,
                    time_frame=time_frame,
                    candle_close=candle_close,
                    candle_open=candle_open,
                    candle_high=candle_high,
                    candle_low=candle_low,
                ),
                level=services_enum.NotificationLevel(self.alert_level),
            )
