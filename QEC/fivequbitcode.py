from .QECCode import QECCode


class fivequbitcode(QECCode):
    
    def __init__(self, physical_qubits: int):
        super().__init__(physical_qubits)
        self.set_stabilizers(["XZZXI","IXZZX","XIXZZ","ZXIXZ"])
        #Store the current depth of the circuit during construction
        #This should be stored to add facknoise.
        self._corrent_depth=0
        

        
    def construct_circuit(self):
        self.construct_syndrome_table()
        
    
    def tanner_graph(self):
        raise NotImplementedError("Subclasses must implement tanner_graph method.")
    
    
    def decode(self,syndrome:str):
        pass
    
    
    def syndrome_table(self):
        return super().syndrome_table()
    