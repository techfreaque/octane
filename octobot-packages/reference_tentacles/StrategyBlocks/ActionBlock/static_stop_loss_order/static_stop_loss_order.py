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
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums

import tentacles.Meta.Keywords.block_factory.abstract_exit_order_block as abstract_exit_order_block


class StopLossOrder(abstract_exit_order_block.ExitOrderBlock):
    NAME = "static_stop_loss_order"
    TITLE = "Static Stop Loss Order"
    TITLE_SHORT = TITLE
    DESCRIPTION = "A static stop loss order can be helpful for semi automatic trading"
    COLOR: block_factory_enums.Colors = block_factory_enums.Colors.YELLOW
    sl_price: decimal.Decimal

    def init_block_settings(self) -> None:
        self.sl_price = decimal.Decimal(
            str(
                self.user_input(
                    "sl_based_on_static_price",
                    "float",
                    def_val=0,
                    min_val=0,
                    title="SL based on static price",
                )
            )
        )

        self.register_stop_orders_output()
        self.register_order_filled_output()

    async def execute_block(
        self,
    ) -> None:
        pass
