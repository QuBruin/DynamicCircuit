from .repetition import bitfliprepetitioncode
from ..noise import construct_bitflip_noise_model,construct_phaseflip_noise_model
import matplotlib.pyplot as plt



def plot_bitflip_threshold():
    number_qubits=[3,5,7]
    physical_errorrates=[0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008]
    three_fidelity=[]
    five_fidelity=[]
    seven_fidelity=[]
    for num in number_qubits:
        for errorrate in physical_errorrates:
            rep=bitfliprepetitioncode(num)
            noisemode=construct_bitflip_noise_model(errorrate,errorrate,errorrate)
            rep.construct_syndrome_table()
            rep.show_syndrome_table()    
            rep.add_noise_model(noisemode)
            
            fidelity=rep.show_noise_effect(shots=100)    
            if num==3:
                three_fidelity.append(fidelity)
            if num==5:
                five_fidelity.append(fidelity)
            if num==7:
                seven_fidelity.append(fidelity)
                
    plt.plot(physical_errorrates,three_fidelity,label="Three")
    plt.plot(physical_errorrates,five_fidelity,label="Five")
    plt.plot(physical_errorrates,seven_fidelity,label="Seven")
    plt.legend()
            
