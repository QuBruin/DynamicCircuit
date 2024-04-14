from .QuantumAlgorithm import  QuantumAlgorithm
import qiskit
from qiskit_aer import AerSimulator
from qiskit.circuit.library.standard_gates import HGate, U1Gate
import numpy as np

class QFFT_qiskit(QuantumAlgorithm):

    def __init__(self, num_qubits: int) -> None:
        super().__init__(num_qubits)
        self.num_qubits = num_qubits
        self._circuit = qiskit.QuantumCircuit(num_qubits, num_qubits)
        self._simulator = AerSimulator()
        self.num_qubits = num_qubits
        self._inverse = False
        self._constructed = False

    @property
    def inverse(self):
        return self._inverse

    @inverse.setter
    def inverse(self, value: bool):
        self._inverse = value

    '''    
           1    0
    Rz(k)=
           0    e^{i 2pi/2^{k}} 
    '''

    def construct_circuit(self):
        if self._constructed:
            return
        if not self._inverse:
            for row in range(0, self.num_qubits):
                self._circuit.append(HGate(), [row])
                for k in range(2, self.num_qubits + 1 - row):
                    self._circuit.append(U1Gate(2 * np.pi / (2 ** k)).control(1), [row + k - 1, row])
        else:
            for row in range(self.num_qubits - 1, -1, -1):
                for k in range(self.num_qubits - row, 1, -1):
                    self._circuit.append(U1Gate(2 * np.pi / (2 ** k)).control(1), [row + k - 1, row])
                self._circuit.append(HGate(), [row])
        self._constructed = True
        return