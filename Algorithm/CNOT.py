from qiskit.pulse import num_qubits
import matplotlib.pyplot as plt
from QuantumAlgorithm import QuantumAlgorithm
import qiskit as qs
from noise import construct_bitflip_noise_model

def generate_evens(n):
    return [i for i in range(2, n-2) if i % 2 == 0]

def generate_odds(n):
    return [i for i in range(1, n, 2)]

def generate_cx_first(n):
    return [[i, i+1] for i in range(0, n-1, 2)]

def generate_cx_second(n):
    return [[i, i+1] for i in range(1, n, 2)]

def is_even(number):
    return number % 2 == 0


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
        qc.h(0)
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
        elif self._mode == 'dynamic_general' and not is_even(self.num_qubits):
            H_locs_even = generate_evens(self.num_qubits)
            qc.h(H_locs_even)
            qc.barrier()

            cx_first_locs = generate_cx_first(self.num_qubits)
            for pair in cx_first_locs:
                qc.cx(pair[0], pair[1])

            cx_first_locs = generate_cx_second(self.num_qubits)
            for pair in cx_first_locs:
                qc.cx(pair[0], pair[1])
            qc.barrier()

            H_locs_odd = generate_odds(self.num_qubits)
            qc.h(H_locs_odd)

            for qubit in reversed(H_locs_even):
                qc.measure(qubit, 0)
                with qc.if_test((cbits[0], 1)):
                    qc.x(self.num_qubits-1)

            for index in reversed(range(len(H_locs_odd))):
                qc.measure(qubits[H_locs_odd[index]], 0)
                with qc.if_test((cbits[0], 1)):
                    if H_locs_odd[index] == 1:
                        qc.z(0)
                    else:
                        qc.x(H_locs_odd[index-1])

            qc.measure([0, self.num_qubits-1], [0,1])
        elif self._mode == 'dynamic_general' and is_even(self.num_qubits):
            self.num_qubits = self.num_qubits-1
            H_locs_even = generate_evens(self.num_qubits)
            qc.h(H_locs_even)
            qc.barrier()

            cx_first_locs = generate_cx_first(self.num_qubits)
            for pair in cx_first_locs:
                qc.cx(pair[0], pair[1])

            cx_first_locs = generate_cx_second(self.num_qubits)
            for pair in cx_first_locs:
                qc.cx(pair[0], pair[1])
            qc.barrier()

            H_locs_odd = generate_odds(self.num_qubits)
            qc.h(H_locs_odd)

            for qubit in reversed(H_locs_even):
                qc.measure(qubit, 0)
                with qc.if_test((cbits[0], 1)):
                    qc.x(self.num_qubits-1)

            for index in reversed(range(len(H_locs_odd))):
                qc.measure(qubits[H_locs_odd[index]], 0)
                with qc.if_test((cbits[0], 1)):
                    if H_locs_odd[index] == 1:
                        qc.z(0)
                    else:
                        qc.x(H_locs_odd[index-1])
            self.num_qubits = self.num_qubits+1
            qc.cx(self.num_qubits-2, self.num_qubits-1)
            qc.measure([0, self.num_qubits-1], [0,1])



        self._circuit = qc


#
cnot = CNOTCircuit(18, 'dynamic_general')
# cnot_dynamic = CNOTCircuit(7, 'dynamic')
# cnot_dynamic.construct_circuit()
cnot.construct_circuit()
# cnot._circuit.draw(output='mpl')
# plt.show()
# cnot._circuit.draw(output='mpl')
# noise_model = construct_bitflip_noise_model(0.01,0.01,0.01)
# cnot.add_noise_model(noise_model)
# cnot.show_noise_effect(10000)
# cnot_dynamic.add_noise_model(noise_model)
# cnot_dynamic.show_noise_effect(10000)
cnot.show_measure_all(1000)
plt.show()
