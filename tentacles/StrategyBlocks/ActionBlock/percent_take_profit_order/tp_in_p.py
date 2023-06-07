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

import tentacles.Meta.Keywords.block_factory.abstract_exit_order_block as abstract_exit_order_block


class TakeProfitOrder(abstract_exit_order_block.ExitOrderBlock):
    NAME = "percent_take_profit_order"
    TITLE = "Percent Take Profit Order"
    TITLE_SHORT = TITLE
    DESCRIPTION = "Take profit based on percent from the filled entry order price"
    tp_in_p: decimal.Decimal

    def init_block_settings(self) -> None:
        self.tp_in_p = decimal.Decimal(
            str(
                self.user_input(
                    "take_profit_in_percent",
                    input_type="float",
                    def_val=2,
                    title="Take profit in %",
                    min_val=0,
                )
            )
        )
        self.register_take_profit_output()
        self.register_order_filled_output()

    async def execute_block(
        self,
    ) -> None:
        pass
