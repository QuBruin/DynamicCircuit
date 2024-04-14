# Import from Qiskit Aer noise module
from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)
from qiskit_aer import AerSimulator
import qiskit
from qiskit.visualization import plot_histogram


class QuantumAlgorithmV2:

    def __init__(self, num_qubits: int) -> None:
        self.num_qubits = num_qubits
        self._circuit = None
        self._noise_model=None
        self._constructed = False
        self._compiled_circuit = None
        self._ideal_result = {}
        self._noise_result = {}
        self._simulator = AerSimulator()

    
    @property
    def circuit(self) -> qiskit.QuantumCircuit:
        return self._circuit
        
    def construct_circuit(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement construct_circuit method.")

    def clear_circuit(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement construct_circuit method.")

    def set_input(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement set_input method.")
    
    def transpile(self):
        if self._compiled_circuit != None:
            return self._compiled_circuit
        self._compiled_circuit = qiskit.transpile(self._circuit, self._simulator)


    def compute_result(self, shots:int):
        if self._ideal_result.get(shots, None) != None:
            return self._ideal_result.get(shots, None)
        
        self.transpile()
        
        # Execute the circuit on the aer simulator
        job = self._simulator.run(self._compiled_circuit, shots=shots)

        self._ideal_result[shots] = job.result()
        return self._ideal_result.get(shots, None)

    def compute_noise_result(self, shots:int):
        # Return cached results for shots, if already computed
        if self._noise_result.get(shots, None) != None:
            return self._noise_result.get(shots, None)
        
        self.transpile()
        
        # Execute the circuit on the aer simulator
        noise_job = self._simulator.run(self._compiled_circuit, shots=shots,noise_model=self._noise_model)

        self._noise_result[shots] = noise_job.result()
        return self._noise_result.get(shots, None)
    
    def show_measure_all(self, shots: int):
        self.compute_result(shots)
        counts_ideal = self._ideal_result.get(shots, None).get_counts()
        return plot_histogram(counts_ideal)
    
    def show_noise_effect(self, shots: int):       
        self.compute_result(shots)
        self.compute_noise_result(shots)

        counts_ideal = self._ideal_result.get(shots, None).get_counts()
        counts_noisy = self._noise_result.get(shots, None).get_counts()

        return plot_histogram([counts_noisy, counts_ideal], legend=['Noisy result', 'Accurate result'], color=['blue', 'red'], title="Show noise effect")
    
    def add_noise_model(self,noisemodel:NoiseModel):
        self._noise_model=noisemodel
