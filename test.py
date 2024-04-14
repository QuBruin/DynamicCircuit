#This is the python file for testing
from Algorithm.QPE import QPhe_qiskit
from qiskit.circuit.library.standard_gates import HGate
from QEC.QECCode import QECCode





if __name__ == '__main__':
    qphe=QPhe_qiskit(3, 3)
    qphe.set_unitary([(HGate(), [0])])
    qphe.construct_circuit()
    qphe.compute_result()
    qphe.show_measure_all(1000,save=True,savepath="QPE.png")
    
    #qec_code=QECCode(5,4,2)
    
    #qec_code.set_stabilizers(["XZZXI","IXZZX","XIXZZ","ZXIXZ"])
    #qec_code.construct_syndrome_table()
    #qec_code.show_syndrome_table()
    
    
    
    
    
    
    
    
    
    