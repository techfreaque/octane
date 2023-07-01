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


def get_supported_evaluators():
    return sorted(
        [
            "divergence",
            "dollar_cost_average",
            "dual_trend",
            "is_crossing",
            "is_oversold",
            "is_overbought",
            "is_rising",
            "is_falling",
            "is_above",
            "is_below",
            "in_manual_range",
            "SFP",
            "triple_trend",
            "three_peaks",
            "wasnt_below",
            "was_below",
            "was_above",
            "lorentzian_classification",
            "data_is_aligned",
            "neural_net_classification",
        ]
    )
