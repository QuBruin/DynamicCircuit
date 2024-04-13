#This is the python file for iterative QPE algorithm
import qiskit
from qiskit_aer import AerSimulator
from QuantumAlgorithm import  QuantumAlgorithm
from typing import List
from QFFT import QFFT_qiskit
import numpy as np
from qiskit.visualization import plot_histogram


class QPhe_qiskit(QuantumAlgorithm):
    '''
    num_qubits is the qubit number of the unitary
    '''

    def __init__(self, num_qubits: int, num_counts: int) -> None:
        super().__init__(num_qubits)
        self.num_qubits = num_qubits
        self.num_counts = num_counts
        self._circuit = qiskit.QuantumCircuit(num_qubits + num_counts, num_counts)
        self._simulator = AerSimulator()
        self._unitarylist = []
        self._unitary = qiskit.QuantumCircuit(num_qubits)
        '''
        The dictionary which store the U^{2k}.
        Store the circuit to reduce time complexity 
        to construct the circuit
        '''
        self._unitaryExpDict = {}
        '''
        The inverse QFFT circuit using in the algorithm
        '''
        self._QFFT = QFFT_qiskit(self.num_counts)
        self._QFFT.inverse = True

        self._constructed = False
        self._computed = False
        self._result = []


    @property
    def circuit(self) -> qiskit.QuantumCircuit:
        return self._circuit

    '''
    Set the unitary U
    gatelist: A list of tuples:
    gatelist=[(Csdg, [0, 1, 2]),(Rgate, [0]),(Rgate, [1])]
    '''

    def set_unitary(self, gatelist: List):
        self._unitarylist = gatelist
        for (gate, indices) in gatelist:
            self._unitary.append(gate, indices)
        self._unitaryExpDict[0] = self._unitary
        self._unitaryExpDict[0].name = "U(2^0)"
    '''
    Return U^{2^k}
    '''

    def unitary_exponential(self, k: int):
        if k in self._unitaryExpDict.keys():
            return self._unitaryExpDict[k]
        else:
            '''
            Recursively calculate U^{2^k}=U^{2^(k-1)}*U^{2^(k-1)}
            '''
            tmpUnitary = self.unitary_exponential(k - 1)
            '''
            In qiskit, we can use the + operator to combine two
            circuit with the same qubit number. 
            '''
            self._unitaryExpDict[k] = tmpUnitary.compose(tmpUnitary)
            self._unitaryExpDict[k].name ="U(2^%d)"%k
        return self._unitaryExpDict[k]

    def construct_circuit(self):
        if self._constructed:
            return
        self._circuit.h(list(range(0, self.num_counts)))
        self._circuit.x(list(range(self.num_counts,self.num_counts+self.num_qubits)))
        counts_qindeices = list(range(0, self.num_counts))
        rot_unitary_qindeices = list(range(self.num_counts, self.num_counts + self.num_qubits))
        for index in range(0, self.num_counts):
            '''
            Add control U^{2^{index}}
            '''
            rot_unitary = self.unitary_exponential(index)
            rot_unitary_gate = rot_unitary.to_gate().control(1)
            self._circuit.append(rot_unitary_gate, [self.num_counts - 1 - index] + rot_unitary_qindeices)

        self._QFFT.construct_circuit()
        iqfft_circ = self._QFFT.circuit
        iqfft_circ.name="IQFFT"
        self._circuit = self._circuit.compose(iqfft_circ, counts_qindeices)
        self._circuit.measure(counts_qindeices, counts_qindeices)
        self._constructed = True
        return

    def compute_result(self,shots=1):
        if self._computed:
            return self._result
        if not self._constructed:
            self.construct_circuit()

        compiled_circuit = qiskit.transpile(self._circuit, self._simulator)
        # Execute the circuit on the aer simulator
        job = self._simulator.run(compiled_circuit, shots=shots,noise_model=self._noise_model)
        # Grab results from the job
        result = job.result()
        # Returns counts
        counts = result.get_counts(compiled_circuit)
        result = list(counts.keys())[0]
        self._result = result
        self._computed = True
        
    def show_measure_all(self, shots: int):
        if not self._constructed:
            self.construct_circuit()

        compiled_circuit = qiskit.transpile(self._circuit, self._simulator)
        # Execute the circuit on the aer simulator
        job = self._simulator.run(compiled_circuit, shots=shots,noise_model=self._noise_model)
        # Grab results from the job
        result = job.result()
        # Returns counts
        counts = result.get_counts(compiled_circuit)
        result = list(counts.keys())[0]
        return plot_histogram(counts)
    