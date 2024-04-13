#This is the python file for iterative QPE algorithm
import qiskit
from qiskit_aer import AerSimulator
from QuantumAlgorithm import  QuantumAlgorithm
from typing import List

class SmallDynamicCircuit(QuantumAlgorithm):
    '''
    num_qubits is the qubit number of the unitary
    '''

    def __init__(self, num_qubits: int, num_cbits: int) -> None:
        super().__init__(num_qubits)
        # self.num_qubits = num_qubits
        self.num_cbits = num_cbits
        self.qreg = qiskit.QuantumRegister(num_qubits)
        self.creg = qiskit.ClassicalRegister(num_cbits)
        self._circuit = qiskit.QuantumCircuit(self.qreg, self.creg)
        
        self._result = []


    @property
    def circuit(self) -> qiskit.QuantumCircuit:
        return self._circuit


    # def
    def construct_circuit(self, target_str):
        self.target_str = target_str
        
        list_q = list(range(self.num_qubits))
        list_c = list(range(self.num_cbits))
        # clist = self._circuit.clbits
        # clist = 
        # print(clist)

        self.circuit.h(list_q)
        self.circuit.measure(list_q, list_c)
        

        with self.circuit.while_loop((self.creg, self.target_str)):
            self.circuit.h(list_q)
            self.circuit.measure(list_q, list_c)
        
        self.constructed = True
        # circuit.draw("mpl")
        return

    # def
    def compute_result(self):
        if not self.constructed:
            self.construct_circuit()

        compiled_circuit = qiskit.transpile(self._circuit, self._simulator)
        job = self._simulator.run(compiled_circuit, shots=100)
        result = job.result()

        counts = result.get_counts(compiled_circuit)
        try:
            counts[bin(self.target_str)]
        except:
            print("no " + bin(self.target_str)[2:])
        
        self._result = counts
    
    

"""
test included
"""

n = 5
sd = SmallDynamicCircuit(n, n)

nbin = int('{:b}'.format((2 ** n) - 1), 2)

sd.construct_circuit(nbin)
sd.compute_result()

print("\n\nSmall Dynamic Circuit until measuring '1' * n.")
print("n is", n)
print(sd._result)
print("\n")