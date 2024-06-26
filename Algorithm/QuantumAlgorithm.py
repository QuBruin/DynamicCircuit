# Import from Qiskit Aer noise module
from itertools import count
from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)
from qiskit_aer import AerSimulator
import qiskit
from qiskit.visualization import plot_histogram


class QuantumAlgorithm:

    def __init__(self, num_qubits: int) -> None:
        self.num_qubits = num_qubits
        self._noise_model=None
        self._circuit=None
        self._constructed = False
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

    def compute_result(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement compute_result method.")


    def show_measure_all(self, shots: int, save=False,savepath=None):
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
        if save:
            plot_histogram(counts, filename=savepath)
            return
        plot_histogram(counts)


    def show_noise_effect(self, shots: int, save=False,savepath=None):
        if not self._constructed:
            self.construct_circuit()

        compiled_circuit = qiskit.transpile(self._circuit, self._simulator)
        # Execute the noisy circuit on the aer simulator
        job = self._simulator.run(compiled_circuit, shots=shots,noise_model=self._noise_model)
        # Grab noisy results from the job
        result_noisy = job.result()
        # Returns noisy counts
        counts_noisy = result_noisy.get_counts(compiled_circuit)
        result_noisy = list(counts_noisy.keys())[0]


        # Execute the circuit on the aer simulator without noise
        job = self._simulator.run(compiled_circuit, shots=shots,noise_model=None)
        # Grab accurate results from the job
        result = job.result()
        # Returns accurate counts
        counts = result.get_counts(compiled_circuit)
        result = list(counts.keys())[0]        
        if save:
            plot_histogram([counts_noisy, counts], legend=['Noisy result', 'Accurate result'], color=['blue', 'red'], title="Show noise effect", filename=savepath)
            return

        plot_histogram([counts_noisy, counts], legend=['Noisy result', 'Accurate result'], color=['blue', 'red'], title="Show noise effect")

    def calculate_fideility(self, shots:str, expected_states : list[str] | str):
        compiled_circuit = qiskit.transpile(self._circuit, self._simulator)
        # Execute the noisy circuit on the aer simulator
        job = self._simulator.run(compiled_circuit, shots=shots,noise_model=self._noise_model)
        # Grab noisy results from the job
        result_noisy = job.result()
        # Returns noisy counts
        counts_noisy = result_noisy.get_counts(compiled_circuit)
        result_noisy = list(counts_noisy.keys())[0]

        if type(expected_states) == str:
            return counts_noisy[expected_states]
        else:
            return sum(counts_noisy[key] for key in expected_states if key in counts_noisy)

    def add_noise_model(self,noisemodel:NoiseModel):
        self._noise_model=noisemodel


    def get_gate_nums(self):
        pass

    def get_circuit_depth(self):
        pass







