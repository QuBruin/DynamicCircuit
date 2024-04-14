# Import from Qiskit Aer noise module
from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)
from qiskit_aer import AerSimulator
import qiskit
from qiskit.visualization import plot_histogram
from typing import List



class QECCode:
    
    
    def __init__(self, num_physical_qubits: int, stabilizer_nums: int,distance:int) -> None:
        self._num_physical_qubits = num_physical_qubits
        self._stabilizer_nums = stabilizer_nums
        self._distance=distance
        self._noise_model=None
        self._constructed = False
        self._simulator = AerSimulator()
        self._circuit=qiskit.QuantumCircuit(num_physical_qubits+stabilizer_nums, stabilizer_nums)
        self._stabilizers=[]
        self._fake_noise={}
        self._symdrome_table={}
        self._error_table={}
        
           
    def construct_circuit(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement construct_circuit method.")
    
    def tanner_graph(self):
        raise NotImplementedError("Subclasses must implement tanner_graph method.")
    
    def set_stabilizers(self, stabilizers:List):
        assert len(stabilizers)==self._stabilizer_nums
        self._stabilizers=stabilizers
    
    def decode(self,syndrome):
        raise NotImplementedError("Subclasses must implement decode method.")
    
    
    #Add the syndrome measurement circuit.
    def construct_circuit_stabilizer(self,stabilizer:str):
        for index in range(0,len(stabilizer)):
            #Add Z stabilizer check
            if stabilizer[index]=="Z":
                self._circuit.cnot(index,index+len(stabilizer))
            #Add X stabilizer check    
            elif stabilizer[index]=="X":
                self._circuit.h(index+len(stabilizer))
                self._circuit.cnot(index,index+len(stabilizer))
                self._circuit.h(index+len(stabilizer))
    
        
    #Construct the circuit to correct the errors    
    def construct_correction_circuit(self, syndrome:str):
        errorstr=self._error_table[syndrome]
        for index in range(0,len(errorstr)):
            if errorstr[index]=="Z":
                self._circuit.z(index)
            elif errorstr[index]=="X":
                self._circuit.x(index)
        
        

    def construct_syndrome_table(self):
        num_errors = 3 ** self._num_physical_qubits
        for i in range(num_errors):
            errorstr = ""
            tmpdistance=0
            num = i
            for _ in range(self._num_physical_qubits):
                remainder = num % 3
                if remainder == 0:
                    errorstr = 'I' + errorstr
                elif remainder == 1:
                    tmpdistance+=1
                    errorstr = 'X' + errorstr
                else:
                    tmpdistance+=1
                    errorstr = 'Z' + errorstr
                num //= 3
            syndromestr = ""
            #The code can only detect error with distance less than or equal to self._distance 
            if tmpdistance>self._distance:
                continue
            for stbindex in range(self._stabilizer_nums):
                if self.commute(self._stabilizers[stbindex],errorstr):
                    syndromestr+="0"
                else:
                    syndromestr+="1"
            self._symdrome_table[errorstr]=syndromestr
            if syndromestr in self._error_table.keys():
                assert False
            self._error_table[syndromestr]=errorstr
             
    
    def show_syndrome_table(self):
        for errorstr in self._symdrome_table.keys():
            print(errorstr+"->"+self._symdrome_table[errorstr])
    
    
    def add_fake_noise(self,width:int,qubitindex:int,is_bitflip:True):
        if is_bitflip:
            self._fake_noise[(width,qubitindex)]="X"
        else:
            self._fake_noise[(width,qubitindex)]="Z"
            
    #The input is two string, return True if the two string commute        
    def commute(self,stabilizer:str,noise:str):
        parity=0
        for index in range(0,len(stabilizer)):
            if stabilizer[index]!="I" and noise[index]!="I":
                if stabilizer[index]!=noise[index]:
                    parity=(parity+1)%2
        if parity==0:
            return True
        else:
            return False
        
        
        
        
        
    
    
    
     

    