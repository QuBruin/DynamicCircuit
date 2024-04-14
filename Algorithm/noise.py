"""
Reference: https://qiskit.github.io/qiskit-aer/tutorials/3_building_noise_models.html
"""

# Import from Qiskit Aer noise module
from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)




def construct_bitflip_noise_model(p_reset, p_meas, p_gate1):
    # Example error probabilities
    p_reset = p_reset
    p_meas = p_meas
    p_gate1 = p_gate1

    # QuantumError objects
    error_reset = pauli_error([('X', p_reset), ('I', 1 - p_reset)])
    error_meas = pauli_error([('X',p_meas), ('I', 1 - p_meas)])
    error_gate1 = pauli_error([('X',p_gate1), ('I', 1 - p_gate1)])
    error_gate2 = error_gate1.tensor(error_gate1)

    # Add errors to noise model
    noise_bit_flip = NoiseModel()
    noise_bit_flip.add_all_qubit_quantum_error(error_reset, "reset")
    noise_bit_flip.add_all_qubit_quantum_error(error_meas, "measure")
    noise_bit_flip.add_all_qubit_quantum_error(error_gate1, ["u1", "u2", "u3"])
    noise_bit_flip.add_all_qubit_quantum_error(error_gate2, ["cx"])

    return noise_bit_flip



def construct_phaseflip_noise_model(p_reset, p_meas, p_gate1):
    # Example error probabilities
    p_reset = p_reset
    p_meas = p_meas
    p_gate1 = p_gate1

    # QuantumError objects
    error_reset = pauli_error([('Z', p_reset), ('I', 1 - p_reset)])
    error_meas = pauli_error([('Z',p_meas), ('I', 1 - p_meas)])
    error_gate1 = pauli_error([('Z',p_gate1), ('I', 1 - p_gate1)])
    error_gate2 = error_gate1.tensor(error_gate1)

    # Add errors to noise model
    noise_phase_flip = NoiseModel()
    noise_phase_flip.add_all_qubit_quantum_error(error_reset, "reset")
    noise_phase_flip.add_all_qubit_quantum_error(error_meas, "measure")
    noise_phase_flip.add_all_qubit_quantum_error(error_gate1, ["u1", "u2", "u3"])
    noise_phase_flip.add_all_qubit_quantum_error(error_gate2, ["cz"])

    return noise_phase_flip


def construct_depolarizing_noise_model(p_single, p_twoq):
    #Sample : https://docs.quantum.ibm.com/api/qiskit/0.37/aer_noise

    # Depolarizing quantum errors
    error_1 = noise.depolarizing_error(p_single, 1)
    error_2 = noise.depolarizing_error(p_twoq, 2)
    
    # Add errors to noise model
    noise_model = noise.NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_1, ['u1', 'u2', 'u3'])
    noise_model.add_all_qubit_quantum_error(error_2, ['cx'])

    return noise_model


def construct_thermal_noise_model(T1, T2):
    # Doc: https://qiskit.github.io/qiskit-aer/tutorials/3_building_noise_models.html

    T1s = np.random.normal(T1, 10e3, 4) # Sampled from normal distribution mean 50 microsec
    T2s = np.random.normal(T2, 10e3, 4)  # Sampled from normal distribution mean 50 microsec

    # Truncate random T2s <= T1s
    T2s = np.array([min(T2s[j], 2 * T1s[j]) for j in range(4)])

    # Instruction times (in nanoseconds)
    time_u1 = 0   # virtual gate
    time_u2 = 50  # (single X90 pulse)
    time_u3 = 100 # (two X90 pulses)
    time_cx = 300
    time_reset = 1000  # 1 microsecond
    time_measure = 1000 # 1 microsecond

    # QuantumError objects
    errors_reset = [thermal_relaxation_error(t1, t2, time_reset)
                    for t1, t2 in zip(T1s, T2s)]
    errors_measure = [thermal_relaxation_error(t1, t2, time_measure)
                    for t1, t2 in zip(T1s, T2s)]
    errors_u1  = [thermal_relaxation_error(t1, t2, time_u1)
                for t1, t2 in zip(T1s, T2s)]
    errors_u2  = [thermal_relaxation_error(t1, t2, time_u2)
                for t1, t2 in zip(T1s, T2s)]
    errors_u3  = [thermal_relaxation_error(t1, t2, time_u3)
                for t1, t2 in zip(T1s, T2s)]
    errors_cx = [[thermal_relaxation_error(t1a, t2a, time_cx).expand(
                thermal_relaxation_error(t1b, t2b, time_cx))
                for t1a, t2a in zip(T1s, T2s)]
                for t1b, t2b in zip(T1s, T2s)]

    # Add errors to noise model
    noise_thermal = NoiseModel()
    for j in range(4):
        noise_thermal.add_quantum_error(errors_reset[j], "reset", [j])
        noise_thermal.add_quantum_error(errors_measure[j], "measure", [j])
        noise_thermal.add_quantum_error(errors_u1[j], "u1", [j])
        noise_thermal.add_quantum_error(errors_u2[j], "u2", [j])
        noise_thermal.add_quantum_error(errors_u3[j], "u3", [j])
        for k in range(4):
            noise_thermal.add_quantum_error(errors_cx[j][k], "cx", [j, k])

    return noise_thermal

