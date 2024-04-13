class QuantumAlgorithm:

    def __init__(self, num_qubits: int) -> None:
        self.num_qubits = num_qubits

    def construct_circuit(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement construct_circuit method.")

    def clear_circuit(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement construct_circuit method.")


    def set_input(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement set_input method.")

    def compute_result(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement compute_result method.")