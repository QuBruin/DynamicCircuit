# Import from Qiskit Aer noise module
from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)
from qiskit_aer import AerSimulator
import qiskit
from qiskit.visualization import plot_histogram


class QuantumAlgorithm:

    def __init__(self, num_qubits: int) -> None:
        self.num_qubits = num_qubits
        self._noise_model=None
        self._constructed = False
        self._simulator = AerSimulator()
        
        
    def construct_circuit(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement construct_circuit method.")

    def clear_circuit(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement construct_circuit method.")

    def set_input(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement set_input method.")
    
    
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
    
    
    def show_noise_effect(self, shots: int):
        if not self._constructed:
            self.construct_circuit()
        self._compiled_circuit = qiskit.transpile(self._circuit, self._simulator)

    def compute_result(self, shots:int):
        if self._ideal_result!=None:
            return self._ideal_result
        
        self.transpile()
        
        # Execute the circuit on the aer simulator
        job = self._simulator.run(self._compiled_circuit, shots=shots)

        self._ideal_result = job.result()

    def compute_noise_result(self, shots:int):
        if self._noise_result != None:
            return self._noise_result
        
        self.transpile()
        
        # Execute the circuit on the aer simulator
        noise_job = self._simulator.run(self._compiled_circuit, shots=shots,noise_model=self._noise_model)

        self._noise_result = noise_job.result()
    
    def show_measure_all(self, shots: int):
        self.compute_result(shots)
        counts = self._ideal_result.get_counts()
        return plot_histogram(counts)
    
    def show_noise_effect(self, shots: int):       
        self.compute_result(shots)
        self.compute_noise_result(shots)

        counts_ideal = self._ideal_result.get_counts()
        counts_noisy = self._noise_result.get_counts()

        return plot_histogram([counts_noisy, counts_ideal], legend=['Noisy result', 'Accurate result'], color=['blue', 'red'], title="Show noise effect")
    
    def add_noise_model(self,noisemodel:NoiseModel):
        self._noise_model=noisemodel
