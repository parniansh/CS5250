import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit_machine_learning.algorithms import NeuralNetworkClassifier
from qiskit_machine_learning.neural_networks import EstimatorQNN
from qiskit.algorithms.optimizers import SPSA


np.random.seed(1000)

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 1, 1, 0])

input_params = list(ParameterVector("x", 2))   # x[0], x[1]
weight_params = list(ParameterVector("θ", 6))  # θ[0] ... θ[5]

qc = QuantumCircuit(2)
qc.ry(input_params[0], 0)
qc.ry(input_params[1], 1)

qc.cx(0, 1)

qc.ry(weight_params[0], 0)
qc.ry(weight_params[1], 1)

qc.cx(1, 0)

qc.ry(weight_params[2], 0)
qc.ry(weight_params[3], 1)

qc.cx(0, 1)

qc.ry(weight_params[4], 0)
qc.ry(weight_params[5], 1)

qnn = EstimatorQNN(
    circuit=qc,
    input_params=input_params,
    weight_params=weight_params
)


classifier = NeuralNetworkClassifier(
    neural_network=qnn,
    optimizer=SPSA(maxiter=300),
    initial_point=np.random.rand(len(weight_params))
)

classifier.fit(X, y)

for i in range(len(X)):
    output = qnn.forward(X[i], classifier._fit_result.x)
    predicted = int(output[0] > 0.5)
    print(f"{X[i]} -> Raw output: {output[0].item():.3f}, Predicted: {predicted}, Actual: {y[i]}")
