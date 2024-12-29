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


import typing

import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.abstract_neural_net as abstract_neural_net
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.tensorflow_CNN as tensorflow_CNN
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.tensorflow_CNN_LSTM as tensorflow_CNN_LSTM
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.tensorflow_LSTM as tensorflow_LSTM
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.tensorflow_RNN as tensorflow_RNN
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.tensorflow_Transformer as tensorflow_Transformer
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.tensorflow_CNN_LSTM2 as tensorflow_CNN_LSTM2


NEURAL_NETS: typing.Dict[str, abstract_neural_net.AbstractNeuralNetwork] = {
    tensorflow_CNN.TensorflowCNN.NEURAL_NET_TITLE: tensorflow_CNN.TensorflowCNN,
    tensorflow_Transformer.TensorflowTransformer.NEURAL_NET_TITLE: tensorflow_Transformer.TensorflowTransformer,
    tensorflow_CNN_LSTM.TensorflowCnnLstm.NEURAL_NET_TITLE: tensorflow_CNN_LSTM.TensorflowCnnLstm,
    tensorflow_CNN_LSTM2.TensorflowCnnLstm2.NEURAL_NET_TITLE: tensorflow_CNN_LSTM2.TensorflowCnnLstm2,
    tensorflow_RNN.TensorflowRNN.NEURAL_NET_TITLE: tensorflow_RNN.TensorflowRNN,
    tensorflow_LSTM.TensorflowLSTM.NEURAL_NET_TITLE: tensorflow_LSTM.TensorflowLSTM,
}
