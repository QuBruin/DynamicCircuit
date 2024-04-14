# Import from Qiskit Aer noise module
from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)
from qiskit_aer import AerSimulator
import qiskit
from qiskit.visualization import plot_histogram
from typing import List
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit


class QECCode:
    
    
    def __init__(self, num_physical_qubits: int, stabilizer_nums: int,distance:int) -> None:
        self._num_physical_qubits = num_physical_qubits
        self._stabilizer_nums = stabilizer_nums
        self._distance=distance
        self._noise_model=None
        self._constructed = False
        self._simulator = AerSimulator()
        self._onlybitflip=False
        self._onlyphaseflip=False
        self._mutecorrection=False
        
        
        self._benchmarkwidth=10
        #self._circuit=qiskit.QuantumCircuit(num_physical_qubits+stabilizer_nums, stabilizer_nums)
        
        self._dataqubits= QuantumRegister(num_physical_qubits, 'Data qubit')
        self._syndromequbits=QuantumRegister(stabilizer_nums, 'Syndrome qubit')
        self._syndromebits= ClassicalRegister(stabilizer_nums, 'Syndrome bit')
        self._databits= ClassicalRegister(num_physical_qubits, 'Data bit')
        self._circuit=QuantumCircuit(self._dataqubits, self._syndromequbits, self._syndromebits,self._databits)
                
        self._stabilizers=[]
        self._fake_noise={}
        self._symdrome_table={}
        self._error_table={}
        
    # Construct the circuit for a full QEC cycle 
    # Including syndrome measurement and error correction      
    def construct_circuit(self):
        if(self._constructed):
            return    
        #print("Constructing!")
        #self._circuit.x(0)
        self.construct_encoding_circuit()
        self.construct_benchmark_circuit()
        for index in range(0,self._stabilizer_nums):
            self.construct_circuit_stabilizer(self._stabilizers[index],index)
        if not self._mutecorrection:    
            for errorsyndrome in self._error_table.keys():
                self.construct_correction_circuit(errorsyndrome)
        for index in range(0,self._stabilizer_nums):
            self._circuit.reset(self._num_physical_qubits+index)
        self.construct_decoding_circuit()
        
        self._circuit.measure(list(range(0, self._num_physical_qubits)), list(range(self._stabilizer_nums, self._num_physical_qubits+self._stabilizer_nums)))
        self._constructed=True
        
        
    def construct_fake_noise_circuit(self):
        for key in self._fake_noise.keys():
            if self._fake_noise[key]=="X":
                self._circuit.x(key[1],label="Fake X noise")
            elif self._fake_noise[key]=="Z":
                self._circuit.z(key[1],label="Fake Z noise")    
        
        
    def set_benchmarkwidth(self,width:int):
        self._benchmarkwidth=width    
       
    def set_mutecorrection(self,mutecorrection:bool):
        self._mutecorrection=mutecorrection    
        
        
    def construct_benchmark_circuit(self):
        for i in range(0,self._benchmarkwidth):
            for qindex in range(self._num_physical_qubits):
                self._circuit.t(qindex)
                self._circuit.barrier(qindex)
                self._circuit.tdg(qindex)
                self._circuit.barrier(qindex)

        
        
    @property
    def circuit(self) -> qiskit.QuantumCircuit:
        return self._circuit
    
    def tanner_graph(self):
        raise NotImplementedError("Subclasses must implement tanner_graph method.")
    
    
    def construct_encoding_circuit(self):
        return
 
    def construct_decoding_circuit(self):
        return
    
    
    def set_stabilizers(self, stabilizers:List):
        assert len(stabilizers)==self._stabilizer_nums
        self._stabilizers=stabilizers
    
    def decode(self,syndrome):
        raise NotImplementedError("Subclasses must implement decode method.")
    
    
    #Add the syndrome measurement circuit.
    def construct_circuit_stabilizer(self,stabilizer:str,stabilizer_index:int):
        
        qreglist = list(range(0, self._num_physical_qubits+self._stabilizer_nums))
        self._circuit.barrier(qreglist)
        
        for index in range(0,len(stabilizer)):
            #Add Z stabilizer check
            #print("Add index {} , {}".format(index,index+len(stabilizer)))
            if stabilizer[index]=="Z":
                self._circuit.cnot(index,self._num_physical_qubits+stabilizer_index)
            #Add X stabilizer check    
            elif stabilizer[index]=="X":
                self._circuit.h(self._num_physical_qubits+stabilizer_index)
                self._circuit.cnot(self._num_physical_qubits+stabilizer_index,index)
                self._circuit.h(self._num_physical_qubits+stabilizer_index)
        #Measure the symdrome qubits    
        self._circuit.barrier(qreglist)
        self._circuit.measure(self._num_physical_qubits+stabilizer_index,stabilizer_index)
        
    #Construct the circuit to correct the errors    
    def construct_correction_circuit(self, syndrome:str):
        #The preconstructed error table should be used here
        #This is actually the decoding step 
        errorstr=self._error_table[syndrome]
        
        for index in range(0,len(errorstr)):
            #If there is an Z error, flip it back with Z
            if errorstr[index]=="Z":
                with self._circuit.if_test((self._syndromebits, int(syndrome, 2))):
                    self._circuit.z(self._num_physical_qubits-1-index)
            #If there is a X error, flip it back with X
            elif errorstr[index]=="X":
                with self._circuit.if_test((self._syndromebits, int(syndrome, 2))):
                    self._circuit.x(self._num_physical_qubits-1-index)
                #self._circuit.x(index)
        
        
    def construct_syndrome_table(self):
        num_errors = 3 ** self._num_physical_qubits
        for i in range(num_errors):
            errorstr = ""
            tmpdistance=0
            num = i
            
            bitflipflag=False
            phaseflipflag=False
            
            for _ in range(self._num_physical_qubits):
                remainder = num % 3
                if remainder == 0:
                    errorstr = 'I' + errorstr
                elif remainder == 1:
                    tmpdistance+=1
                    if self._onlyphaseflip:
                        phaseflipflag=True
                        break 
                    errorstr = 'X' + errorstr
                else:
                    tmpdistance+=1
                    if self._onlybitflip:
                        bitflipflag=True
                        break 
                    errorstr = 'Z' + errorstr
                num //= 3
            if bitflipflag:
                continue
            if phaseflipflag:
                continue            
            syndromestr = ""
            #The code can only detect error with distance less than or equal to self._distance 
            #print("Error: "+errorstr+" distance is "+str(tmpdistance)+" self._distance is "+str(self._distance))            
            
            if tmpdistance>self._distance:
                continue
            for stbindex in range(self._stabilizer_nums):
                if self.commute(self._stabilizers[stbindex],errorstr):
                    syndromestr+="0"
                else:
                    syndromestr+="1"
            self._symdrome_table[errorstr]=syndromestr
            if syndromestr in self._error_table.keys():
                #assert False
                print("Error: "+syndromestr+"->"+errorstr+" is not unique")
            else:
                self._error_table[syndromestr]=errorstr
             
    
    def show_syndrome_table(self):
        print("The syndrome table is:")
        for errorstr in self._symdrome_table.keys():
            print(errorstr+"->"+self._symdrome_table[errorstr])
        print("The error table is:")
        for syndromestr in self._error_table.keys():
            print(syndromestr+"->"+self._error_table[syndromestr])
    
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
        
    
    
    def test_fidelity(self,errorstrlist:List[str],shots:int):
        for errorstr in errorstrlist:
            for i in range(0,len(errorstr)):
                if errorstr[i]=="X":
                    self._circuit.x(i,label="Fake X noise")
                elif errorstr[i]=="Z":
                    self._circuit.z(i,label="Fake Z noise")
        
        self.construct_circuit()
        
        self._circuit.measure(list(range(0, self._num_physical_qubits)), list(range(self._stabilizer_nums, self._num_physical_qubits+self._stabilizer_nums)))
        
        
        compiled_circuit = qiskit.transpile(self._circuit, self._simulator)
        # Execute the circuit on the aer simulator
        job = self._simulator.run(compiled_circuit, shots=shots,noise_model=self._noise_model)
        # Grab results from the job
        result = job.result()
        # Returns counts
        counts = result.get_counts(compiled_circuit)
        result = list(counts.keys())[0]
        result=result[::-1]
        print("The result is: "+result)
        print(counts)
        plot_histogram(counts)  
        
        return counts     
        
        
        
    
    def test_stabilizer_circuit(self,errorstr:str):
        self._circuit.clear()       
        for i in range(0,len(errorstr)):
            if errorstr[i]=="X":
                self._circuit.x(i,label="Fake X noise")
            elif errorstr[i]=="Z":
                self._circuit.z(i,label="Fake Z noise")

        '''
        for index in range(0,self._stabilizer_nums):
            self.construct_circuit_stabilizer(self._stabilizers[index],index)
        '''
        self.construct_circuit()
        
        
        compiled_circuit = qiskit.transpile(self._circuit, self._simulator)
        # Execute the circuit on the aer simulator
        job = self._simulator.run(compiled_circuit, shots=1,noise_model=self._noise_model)
        # Grab results from the job
        result = job.result()
        # Returns counts
        counts = result.get_counts(compiled_circuit)
        result = list(counts.keys())[0]
        result=result[::-1]
        print("The result is: "+result)
        
        
        print("The expected rsult is "+self._symdrome_table[errorstr])
        
        plot_histogram(counts)
    
    
        
    def add_noise_model(self,noisemodel:NoiseModel):
        self._noise_model=noisemodel
        
        
    #Demonstrate the result with and without error correction
    #Should also return the fidelity    
    def show_noise_effect(self, shots: int,plot=False, save=False,savepath=None):
        if not self._constructed:
            self.construct_circuit()
            

        compiled_circuit = qiskit.transpile(self._circuit, self._simulator)
        # Execute the noisy circuit on the aer simulator
        job = self._simulator.run(compiled_circuit, shots=shots,noise_model=self._noise_model)
        # Grab noisy results from the job
        result_noisy = job.result()
        # Returns noisy counts
        counts_noisy = result_noisy.get_counts(compiled_circuit)
        result_noisy = list(counts_noisy.keys())[0]
        
        
        # Execute the circuit on the aer simulator without noise
        job = self._simulator.run(compiled_circuit, shots=shots,noise_model=None)
        # Grab accurate results from the job
        result = job.result()
        # Returns accurate counts
        counts = result.get_counts(compiled_circuit)
        result = list(counts.keys())[0]        
        print(counts_noisy)
        
        success=0
        for key in counts_noisy.keys():
            if key[:self._num_physical_qubits]=='0'*self._num_physical_qubits:
                success+=counts_noisy[key]
        fidelity=success/shots
        #print(fidelity)
        if plot:
            if save:
                plot_histogram([counts_noisy, counts], legend=['Noisy result', 'Accurate result'], color=['blue', 'red'], figsize=(12, 8),title="Show noise effect", filename=savepath)
            else:
                plot_histogram([counts_noisy, counts], legend=['Noisy result', 'Accurate result'], color=['blue', 'red'], figsize=(12, 8),title="Show noise effect")
        return fidelity
        
        
        


        
        
        
        
        
        
        
        
        
    
    
    
     

    