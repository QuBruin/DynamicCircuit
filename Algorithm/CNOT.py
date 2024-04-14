from qiskit.pulse import num_qubits
import matplotlib.pyplot as plt
from QuantumAlgorithm import QuantumAlgorithm
import qiskit as qs
from noise import construct_bitflip_noise_model


class CNOTCircuit(QuantumAlgorithm):
    def __init__(self, num_qubits: int, mode:str) -> None:
        super().__init__(num_qubits)
        self._mode = mode
    # construct the quantum _circuit
    # three cases:
    # case 1: simple cx gate assuming connectivity is not an issue
    # case 2: using swap gate to implement CNOT (only work for even qubits currently)
    # case 3: using dynamic circuits to implement remote CNOT (only work for 7 qubit currently)
    # next step is to generalize to N qubits
    def construct_circuit(self) :
        qubits = qs.QuantumRegister(self.num_qubits)
        cbits = qs.ClassicalRegister(2)
        qc = qs.QuantumCircuit(qubits, cbits)
        middle = int(self.num_qubits/2)
        qc.x(0)
        qc.barrier()
        # simple cx on the first and last qubit
        if self._mode == 'simple':
            qc.cx(0, self.num_qubits-1)
            # unitary swap to implement cx on first and last qubit
            qc.measure([0, self.num_qubits-1], [0, 1])
        elif self._mode == 'unitary':
            for i in range(self.num_qubits-1):
                qc.cx(i, i+1)
            for i in range(self.num_qubits-2):
                qc.cx(self.num_qubits-i - 3, self.num_qubits-i-2)
            qc.barrier()
            qc.measure([0, self.num_qubits-1], [0, 1])
            # for i in range(int(self.num_qubits/2-1)):
            #     qc.cx(i, i+1)
            #     qc.cx(i+1, i)
            #     qc.cx(self.num_qubits-i-1, self.num_qubits-i-2)
            #     qc.cx(self.num_qubits-i-2, self.num_qubits-i-1)
            # qc.barrier()
            # qc.cx(middle-1, middle)
            # qc.barrier()
            # for i in range(int(self.num_qubits/2-1)):
            #     qc.cx(middle - i - 1, middle - i - 2)
            #     qc.cx(middle - i - 2, middle - i - 1)
            #     qc.cx(middle + i, middle + i + 1 )
            #     qc.cx(middle + i + 1, middle + i)
            # qc.measure([0, self.num_qubits-1], [0, 1])
        elif self._mode == 'dynamic': 
            qc.h(2)
            qc.h(4)
            qc.barrier()
            qc.cx(0,1)
            qc.cx(2,3)
            qc.cx(4,5)
            qc.cx(1,2)
            qc.cx(3,4)
            qc.cx(5,6)
            qc.barrier()
            qc.h([1,3,5])
            qc.measure(4,0)
            with qc.if_test((cbits[0], 1)):
                qc.x(6)
            qc.measure(2,1)
            with qc.if_test((cbits[1], 1)):
                qc.x(6)
            qc.measure(5,0)
            with qc.if_test((cbits[0], 1)):
                qc.x(3)
            qc.measure(3,0)
            with qc.if_test((cbits[0], 1)):
                qc.x(1)
            qc.measure(1,0)
            with qc.if_test((cbits[0], 1)):
                qc.z(0)
            qc.measure([0, self.num_qubits-1], [0,1])
        self._circuit = qc



cnot = CNOTCircuit(7, 'unitary')
cnot.construct_circuit()
# cnot._circuit.draw(output='mpl')
noise_model = construct_bitflip_noise_model(0.01,0.01,0.01)
cnot.add_noise_model(noise_model)
cnot.show_noise_effect(1000)
plt.show()
