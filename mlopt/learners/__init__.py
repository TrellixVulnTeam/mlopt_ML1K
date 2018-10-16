from mlopt.learners.pytorch_neural_net import PyTorchNeuralNet
from mlopt.learners.tensorflow_neural_net import TensorFlowNeuralNet
from mlopt.learners.optimal_tree import OptimalTree
import mlopt.settings as s

LEARNER_MAP = {s.PYTORCH: PyTorchNeuralNet,
               s.TENSORFLOW: TensorFlowNeuralNet,
               s.OPTIMAL_TREE: OptimalTree}
