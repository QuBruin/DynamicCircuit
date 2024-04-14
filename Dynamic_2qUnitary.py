#This is the python file for iterative QPE algorithm
import qiskit
from qiskit_aer import AerSimulator
from QuantumAlgorithmV2 import  QuantumAlgorithmV2
from typing import List
import numpy as np
from qiskit.visualization import plot_histogram

'''
Changsoo Kim

Implement a General Long-Range 2-Qubit Unitary Entanglement Using Dynamic Circuits
N_CNOT = 2n



'''
class Dynamic2Q(QuantumAlgorithmV2):

    def __init__(self, num_qubits: int, num_cbits: int, target_unitary, psi1, psi2) -> None:
        super().__init__(num_qubits)
        self.num_qubits = num_qubits
        self.num_cbits = num_cbits
        self.target_unitary = target_unitary
        self.qubits = qiskit.QuantumRegister(num_qubits)
        self.clbits = qiskit.ClassicalRegister(num_cbits)
        self._circuit = qiskit.QuantumCircuit(self.qubits, self.clbits)
        self.psi1 = psi1
        self.psi2 = psi2
        self.answer = None
        self._compiled = False
        
    @property
    def circuit(self) -> qiskit.QuantumCircuit:
        return self._circuit

    def add_circ_down(self, circuit, clbits, i):
        circuit.cx(i, i+1)
        circuit.h(i)

        circuit.measure(i, i)
        circuit.reset(i)
        circuit.z(i+1).c_if(clbits[i], 1)

    def add_circ_up(self, circuit, clbits, i):
        circuit.cx(i, i-1)
        circuit.h(i)

        circuit.measure(i, i)
        circuit.reset(i)
        circuit.z(i-1).c_if(clbits[i], 1)

    # def
    def construct_circuit(self):
        n = self.num_qubits
        ndiv2 = self.num_qubits // 2
        self.qubits = qiskit.QuantumRegister(n)
        self.clbits = qiskit.ClassicalRegister(n)
        self._circuit = qiskit.QuantumCircuit(self.qubits, self.clbits)

        self._circuit.initialize(self.psi1, 0)
        self._circuit.initialize(self.psi2, n-1)

        for i in range(ndiv2 - 1):
            self.add_circ_down(self._circuit, self.clbits, i)
            self.add_circ_up(self._circuit, self.clbits, n - i - 1)
            self._circuit.barrier()
        
        if n % 2 == 1:
            self.add_circ_up(self._circuit, self.clbits, n - (ndiv2))

        # implement unitary exception
        self._circuit.unitary(self.target_unitary, [ndiv2, ndiv2-1])

        if n % 2 == 1:
            self.add_circ_down(self._circuit, self.clbits, n - ndiv2 - 1)

        self._circuit.barrier()

        for i in range(ndiv2 - 1)[::-1]:
            self.add_circ_up(self._circuit, self.clbits, i + 1)
            self.add_circ_down(self._circuit, self.clbits, n - i - 2)
            self._circuit.barrier()
        
        self._circuit.measure([0, n-1], [0, n-1])
        # display(circuit.draw("mpl", fold=-1))
        self._circuit = self._circuit.reverse_bits()
        self._constructed = True
        return self._circuit
        

    # def
    def compute_result(self, shots):
        n = self.num_qubits
        if not self._constructed:
            self.construct_circuit()

        compiled_circuit = qiskit.transpile(self._circuit, self._simulator)
        job = self._simulator.run(compiled_circuit, shots=shots)
        result = job.result()
        counts = result.get_counts(compiled_circuit)


        st = 0
        ed = n-1
        n0 = sum(v for k,v in counts.items() if k[st] + k[ed] == '00')
        n1 = sum(v for k,v in counts.items() if k[st] + k[ed] == '01')
        n2 = sum(v for k,v in counts.items() if k[st] + k[ed] == '10')
        n3 = sum(v for k,v in counts.items() if k[st] + k[ed] == '11')

        res = self.target_unitary @ np.kron(self.psi1, self.psi2)

        self.answer = np.array([abs(res[0]) ** 2, abs(res[1]) ** 2, abs(res[2]) ** 2, abs(res[3]) ** 2])
        div = n0 + n1 + n2 + n3
        rsub = (1/div) * np.array([n0, n1, n2, n3])

        csd = np.dot(self.answer, rsub) / (np.linalg.norm(self.answer)* np.linalg.norm(rsub))
        print("Accuracy of U (|psi1> |000..0> |psi2>) is: ", csd)
        
        self._result = csd

        self._ideal_result[shots] = {'00': n0, '01': n1, '10': n2, '11': n3}
        self._compiled = True
        return self._ideal_result[shots]
    
    def compute_noise_result(self, shots:int):
        # Return cached results for shots, if already computed
        if self._noise_result.get(shots, None) != None:
            return self._noise_result.get(shots, None)
        
        self.transpile()
        
        # Execute the circuit on the aer simulator
        noise_job = self._simulator.run(self._compiled_circuit, shots=shots,noise_model=self._noise_model)
        counts = noise_job.result().get_counts(self._compiled_circuit)
        
        st = 0
        ed = self.num_qubits-1
        n0 = sum(v for k,v in counts.items() if k[st] + k[ed] == '00')
        n1 = sum(v for k,v in counts.items() if k[st] + k[ed] == '01')
        n2 = sum(v for k,v in counts.items() if k[st] + k[ed] == '10')
        n3 = sum(v for k,v in counts.items() if k[st] + k[ed] == '11')

        div = n0 + n1 + n2 + n3
        rsub = (1/div) * np.array([n0, n1, n2, n3])
        csd = np.dot(self.answer, rsub) / (np.linalg.norm(self.answer)* np.linalg.norm(rsub))
        print("Accuracy of noisy U (|psi1> |000..0> |psi2>) is: ", csd)

        self._noise_result[shots] = {'00': n0, '01': n1, '10': n2, '11': n3}
        return self._noise_result[shots]

    def show_noise_effect(self, shots: int):
        if not self._compiled:       
            self.compute_result(shots)
        self.compute_noise_result(shots)

        counts_ideal = self._ideal_result[shots]
        counts_noisy = self._noise_result[shots]

        return plot_histogram([counts_noisy, counts_ideal], legend=['Noisy result', 'Accurate result'], color=['blue', 'red'], title="Show noise effect")

# """
# test included
# """

# n = 5
# sd = SmallDynamicCircuit(n, n)

# nbin = int('{:b}'.format((2 ** n) - 1), 2)

# sd.construct_circuit(nbin)
# sd.compute_result()

# print("\n\nSmall Dynamic Circuit until measuring '1' * n.")
# print("n is", n)
# print(sd._result)
# print("\n")