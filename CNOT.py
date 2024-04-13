from qiskit.pulse import num_qubits
import matplotlib.pyplot as plt
from QuantumAlgorithm import QuantumAlgorithm
import qiskit as qs

class CNOTCircuit(QuantumAlgorithm):
    def __init__(self, num_qubits: int) -> None:
        super().__init__(num_qubits)

    def construct_circuit(self, mode : str) :
        qc = qs.QuantumCircuit(self.num_qubits)
        middle = int(self.num_qubits/2)
        qc.x(0)
        qc.barrier()
        # simple cx on the first and last qubit
        if mode == 'simple':
            qc.cx(0, self.num_qubits-1)
            # unitary swap to implement cx on first and last qubit
        elif mode == 'unitary':
            for i in range(int(self.num_qubits/2-1)):
                qc.cx(i, i+1)
                qc.cx(i+1, i)
                qc.cx(self.num_qubits-i-1, self.num_qubits-i-2)
                qc.cx(self.num_qubits-i-2, self.num_qubits-i-1)
            qc.barrier()
            qc.cx(middle-1, middle)
            qc.barrier()
            for i in range(int(self.num_qubits/2-1)):
                qc.cx(middle - i - 1, middle - i - 2)
                qc.cx(middle - i - 2, middle - i - 1)
                qc.cx(middle + i, middle + i + 1 )
                qc.cx(middle + i + 1, middle + i)
        # elif mode == 'dynamic': 
        self.qc = qc

    def compute_result(self):
        return 0
