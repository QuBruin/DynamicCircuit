from QEC.QECCode import QECCode


class fivequbitcode(QECCode):
    
    def __init__(self, physical_qubits: int):
        super().__init__(physical_qubits)
        self.set_stabilizers(["XZZXI","IXZZX","XIXZZ","ZXIXZ"])
        #Store the current depth of the circuit during construction
        #This should be stored to add facknoise.
        self._corrent_depth=0
        

        
    def construct_circuit(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement construct_circuit method.")
    
    
    
    #Add the syndrome measurement circuit.
    def construct_circuit_stabilizer(self,stabilizer:str):
        for index in range(0,len(stabilizer)):
            if stabilizer[index]=="Z":
                self._circuit.cnot(index,index+len(stabilizer))
            elif stabilizer[index]=="X":
                self._circuit.h(index+len(stabilizer))
                self._circuit.cnot(index,index+len(stabilizer))
                self._circuit.h(index+len(stabilizer))
        
        
    def construct_correct_circuit(self, syndrome:str):
        
        pass
    
    
    def tanner_graph(self):
        raise NotImplementedError("Subclasses must implement tanner_graph method.")
    
    
    def decode(self,syndrome:str):
        pass
    
    
    def syndrome_table(self):
        return super().syndrome_table()
    