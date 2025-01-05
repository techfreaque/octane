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


import decimal
from typing import Literal
import octobot_commons.enums as commons_enums
import octobot_trading.enums as trading_enums
import octobot_services.enums as services_enum
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.block_factory.abstract_action_block as abstract_action_block
import tentacles.Meta.Keywords.scripting_library.alerts.notifications as notifications


WITHDRAWAL = "Withdrawal"
DEPOSIT = "Deposit"


class SimulatedDepositWithdrawalAction(abstract_action_block.ActionBlock):
    NAME = "simulated_deposit_withdrawal"
    TITLE = "Simulate Deposit or Withdrawal"
    TITLE_SHORT = TITLE
    DESCRIPTION = "Simulate a deposit or withdrawal of funds"

    transaction_type: Literal["Withdrawal", "Deposit"]
    transaction_amount: float
    transaction_currency: str

    def init_block_settings(self) -> None:
        self.transaction_type = self.user_input(
            "transaction_type",
            commons_enums.UserInputTypes.OPTIONS.value,
            def_val=DEPOSIT,
            options=[WITHDRAWAL, DEPOSIT],
            title="Transaction Type",
        )
        self.transaction_amount = self.user_input(
            "transaction_amount",
            commons_enums.UserInputTypes.FLOAT.value,
            def_val=0,
            min_val=0,
            title="Transaction Amount",
        )
        all_currencies = self.get_available_currencies()
        self.transaction_currency = self.user_input(
            "transaction_currency",
            commons_enums.UserInputTypes.OPTIONS.value,
            def_val=all_currencies[0],
            options=all_currencies,
            title="Transaction Currency",
        )

    async def execute_block(
        self,
    ) -> None:
        exchange_personal_data = (
            self.block_factory.ctx.exchange_manager.exchange_personal_data
        )
        if self.transaction_amount:
            transaction_amount: decimal.Decimal = decimal.Decimal(
                self.transaction_amount
            )
            if self.transaction_type == DEPOSIT:
                await exchange_personal_data.handle_portfolio_update_from_deposit(
                    amount=transaction_amount,
                    currency=self.transaction_currency,
                    should_notify=True,
                )
            else:
                await exchange_personal_data.handle_portfolio_update_from_withdrawal(
                    amount=transaction_amount,
                    currency=self.transaction_currency,
                    should_notify=True,
                )
