import typing

from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets import (
    abstract_neural_net,
)
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.tensorflow_CNN import (
    TensorflowCNN,
)
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.tensorflow_CNN_LSTM import (
    TensorflowCnnLstm,
)
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.tensorflow_LSTM import (
    TensorflowLSTM,
)
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.tensorflow_RNN import (
    TensorflowRNN,
)
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.sklearn_mlp_classifier import (
    SKLearnMLP,
)
from tentacles.Meta.Keywords.pro_tentacles.evaluators.neural_net_classification.neural_nets.tensorflow_Transformer import (
    TensorflowTransformer,
)


NEURAL_NETS: typing.Dict[str, abstract_neural_net.AbstractNeuralNetwork] = {
    TensorflowCNN.NEURAL_NET_TITLE: TensorflowCNN,
    TensorflowTransformer.NEURAL_NET_TITLE: TensorflowTransformer,
    TensorflowCnnLstm.NEURAL_NET_TITLE: TensorflowCnnLstm,
    TensorflowRNN.NEURAL_NET_TITLE: TensorflowRNN,
    TensorflowLSTM.NEURAL_NET_TITLE: TensorflowLSTM,
    SKLearnMLP.NEURAL_NET_TITLE: SKLearnMLP,
}
