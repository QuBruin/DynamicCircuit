from .QECCode import QECCode


class fivequbitcode(QECCode):
    
    def __init__(self, physical_qubits=5):
        super().__init__(physical_qubits,4,2)
        self.set_stabilizers(["XZZXI","IXZZX","XIXZZ","ZXIXZ"])

     #https://quantumcomputing.stackexchange.com/questions/14264/nielsenchuang-5-qubit-quantum-error-correction-encoding-gate 
    def construct_encoding_circuit(self):
        self._circuit.h(0)
        self._circuit.h(1)
        self._circuit.h(2)
        self._circuit.h(3)
        self._circuit.z(4)
        
        self._circuit.cx(0,4)
        self._circuit.cx(1,4)
        self._circuit.cx(2,4)
        self._circuit.cx(3,4)
        
        self._circuit.cz(0,4)
        self._circuit.cz(0,1)
        self._circuit.cz(2,3)
        self._circuit.cz(1,2)
        self._circuit.cz(3,4)
        
        qreglist = list(range(0, self._num_physical_qubits+self._stabilizer_nums))
        self._circuit.barrier(qreglist)
        
        
        
        
    def construct_decoding_circuit(self):
        qreglist = list(range(0, self._num_physical_qubits+self._stabilizer_nums))
        self._circuit.barrier(qreglist)
        self._circuit.cz(3,4)
        self._circuit.cz(1,2)
        self._circuit.cz(2,3)
        self._circuit.cz(0,1)
        self._circuit.cz(0,4)
        
        self._circuit.cx(3,4)
        self._circuit.cx(2,4)
        self._circuit.cx(1,4)
        self._circuit.cx(0,4)
        
        self._circuit.z(4)
        self._circuit.h(3)
        self._circuit.h(2)
        self._circuit.h(1)
        self._circuit.h(0)
        
        