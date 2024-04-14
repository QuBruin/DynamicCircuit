from .QECCode import QECCode


class bitfliprepetitioncode(QECCode):
    
    def __init__(self, physical_qubits: int):
        
        distance=(physical_qubits-1)//2
        super().__init__(physical_qubits,physical_qubits-1,distance)
        stabilizerlist=[]
        for i in range(physical_qubits-1):
            tmpstring='I'*i+'ZZ'+ 'I'*(physical_qubits-i-2)
            stabilizerlist.append(tmpstring)
        
        self.set_stabilizers(stabilizerlist)
        print(stabilizerlist)
        self._onlybitflip=True
        self._onlyphaseflip=False
        
    

class phasefliprepetitioncode(QECCode):
    
    def __init__(self, physical_qubits: int):
        super().__init__(physical_qubits,2,1)
        self.set_stabilizers(["XXI","IXX"])
        self._onlybitflip=False
        self._onlyphaseflip=True
        

    