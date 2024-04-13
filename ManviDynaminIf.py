import qiskit
from qiskit_aer import AerSimulator
from QuantumAlgorithm import  QuantumAlgorithm
from typing import List
from QFFT import QFFT_qiskit

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
 
class DyanamicIf(QuantumAlgorithm):
    def __init__(self, num_qubits: int) -> None:
        super().__init__(num_qubits)


    def construct_circuit(self) -> NotImplementedError:
        qubits = QuantumRegister(self.num_qubits)
        clbits = ClassicalRegister(self.num_qubits)
        self._circuit = QuantumCircuit(qubits, clbits)
        q0 = qubits[0]
        c0 = clbits[0]
        
        self._circuit.h(q0)
        self._circuit.measure(q0, c0)
        with self._circuit.if_test((c0, 1)):
            self._circuit.x(q0)

        self._constructed = True
        


