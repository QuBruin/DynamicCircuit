#This is the python file for testing
from QPE import QPhe_qiskit
from qiskit.circuit.library.standard_gates import HGate

if __name__ == '__main__':
    qphe=QPhe_qiskit(3, 3)
    qphe.set_unitary([(HGate(), [0])])
    qphe.construct_circuit()
    qphe.compute_result()
    
    
    
    