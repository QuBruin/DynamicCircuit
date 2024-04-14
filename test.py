#This is the python file for testing
from Algorithm.QPE import QPhe_qiskit
from qiskit.circuit.library.standard_gates import HGate
from QEC.QECCode import QECCode
from Algorithm.noise import construct_bitflip_noise_model,construct_phaseflip_noise_model



if __name__ == '__main__':
    #qphe=QPhe_qiskit(3, 3)
    #qphe.set_unitary([(HGate(), [0])])
    #qphe.construct_circuit()
    #qphe.compute_result()
    
    #qphe.show_measure_all(1000,save=True,savepath="QPEAll.png")
    #qphe.show_noise_effect(1000,save=True,savepath="QPENoise.png")
    
    #qec_code=QECCode(5,4,2)
    
    #qec_code.set_stabilizers(["XZZXI","IXZZX","XIXZZ","ZXIXZ"])
    #qec_code.construct_syndrome_table()
    #qec_code.show_syndrome_table()
    
    #from QEC.QECCode import QECCode

    #qec_code=QECCode(2,2,5)
        
    #qec_code.set_stabilizers(["XZ","IX"])
    #qec_code.construct_syndrome_table()
    #qec_code.show_syndrome_table()
    
    #qec_code.construct_circuit_stabilizer("XZ",0)
    #qec_code.construct_correction_circuit("10")
    
    #qec_code.test_stabilizer_circuit(errorstr="XI",stabstr="XZ",stabindex=0)
    
    
    from QEC.repetition import bitfliprepetitioncode
    rep=bitfliprepetitioncode(3)
    noisemode=construct_bitflip_noise_model(0.01,0.01,0.01)
    rep.construct_syndrome_table()
    rep.show_syndrome_table()    
    rep.add_noise_model(noisemode)
    
    rep.show_noise_effect(shots=100, save=True,savepath="RepetitionNoise.png")
   
    
    
    
    
    
    
    
    
    