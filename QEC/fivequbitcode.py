from .QECCode import QECCode


class fivequbitcode(QECCode):
    
    def __init__(self, physical_qubits=5):
        super().__init__(physical_qubits,4,2)
        self.set_stabilizers(["XZZXI","IXZZX","XIXZZ","ZXIXZ"])

      
    def construct_encoding_circuit(self):
        self._circuit.z(0)
        self._circuit.h(2)
        self._circuit.h(3)
        self._circuit.sdg(0)
        self._circuit.cx(2,4)
        self._circuit.cx(3,1)
        self._circuit.h(1)
        self._circuit.cx(3,4)
        self._circuit.cx(1,0)
        self._circuit.sdg(2)
        self._circuit.s(3)
        self._circuit.sdg(4)
        self._circuit.s(0)
        self._circuit.s(1)
        self._circuit.z(2)
        self._circuit.cx(4,0)
        self._circuit.h(4)
        
        
    def construct_decoding_circuit(self):
        self._circuit.h(4)
        self._circuit.cx(4,0)
        self._circuit.z(2)
        self._circuit.s(1)
        self._circuit.sdg(0)
        self._circuit.s(4)
        self._circuit.sdg(3)
        self._circuit.s(2)
        self._circuit.cx(1,0)
        self._circuit.cx(3,4)
        self._circuit.h(1)
        self._circuit.cx(3,1)
        self._circuit.cx(2,4)
        self._circuit.s(0)
        self._circuit.h(3)
        self._circuit.h(2)
        self._circuit.z(0)
        
        