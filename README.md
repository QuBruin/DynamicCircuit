# Our problem: DynamicCircuit
This is the repository of 2024 Yale quantum hackthon. We are a team formed by all UCLA student.

We choose the problem provided by IBM, which is one of the leading Company of quantum computing. We are asked to find and implement some application with 
dynamic quantum circuit with potential advantage over static ones. In dynamic circuit, we can measure and read the qubit before the next quantum instruction. Such
flexibility can be used to optimize quantum algorithm design, circuit compilation, as well as error correction. 

During the Hackthon, we mainly focus on quantum remote dynamic CNOT and 2 qubit gates and developing a general quantum error correction class based on qiskit under the support of dynamic circuit.
We have not only demonstrated the power of dynamic circuit under different types of noise, but also make future QEC development with qiskit easier by designing and implementing a quantum error correction package. 



# Team: QuBruin

<img src="Figures/Logo.png" alt="alt text" width="200"> 
This is the logo for our team.

We are three Master students from UCLA MQST project looking for internship right now.

Please contact us if you are interested.


[UCLA MQST program webpage](https://qst.ucla.edu/)

**Zhuoyang Ye, Qiyu Liu, Changsoo Kim, Manvi Agrawal, Haocheng wang**



# Initialize a virtual environment

You can replicate all our results in this Hackathon on your own computer. Please create a virtual python environment, which we call yalehack, and install the required package 
by running the following commands.


## For Windows users

```console
cd path\to\your\project
py -m venv yalehack
yalehack\Scripts\activate
pip install -r requirements.txt
```

## For Linux/Mac users

```console
cd path/to/your/project
python3 -m venv yalehack
source yalehack/bin/activate
pip install -r requirements.txt
```


# Quantum Error correction

Quantum error correction is essential in developming a scalabale quantum computer. Although there already exists many candidate for the practical QEC code such as torus code, surface code, qldpc code, we lack a software support for understanding, simulating, and compiling different QEC code. The support of dynamic circuit in qiskit promise a bright future of developing all QEC code by qiskit, because all QEC cycle need dynamical instructions such as syndrome measurement and error correction. 

We follow the seperate three stages of developing a unified quantum error corretion package with dynamic circuit:

1. Develop the support of different noise model using qiskit
2. Use stabilizer format to unify the representation of different error correction code.
3. Design the interface carefully and implement the QECCode class, which can be initlized by stabilizer string format.
4. Implement look up table method to do the syndrome decoding.
5. Implement the scalable circuit construction for all syndrome measurement.
6. Implement the scalable circuit construction for all error correction steps.
7. Test the correctness of implementation by add fake noise.
8. Add noise model to the QECcode class
9. Compare the fidelity with and without noise, to demonstrate the effect of QECcode.
10. Inherit the base QECcode class, we impelement the repetition code class and five qubit code class. 


## Noise model  
We have used the following noise models. For more details, please see the [API Documentation](https://docs.quantum.ibm.com/api/qiskit/0.24/qiskit.providers.aer.noise.NoiseModel)
- Bit Flip noise model
- Phase Flip noise model
- Depolarizing noise model
- Thermal noise model


## QECCode class

(Statbilizer, noise simulation, benchmark, error thershold simulation, syndrome table(Decoding) )

Following is the example of how to create a 5 qubit code QEC instance by the stabilizers:

```python
from QEC.QECCode import QECCode

#(5,4,2) means there are 5 physical qubit, 4 stabilizers and the code distance is 2
qec_code=QECCode(5,4,2)
# Initialize the stabilizer
qec_code.set_stabilizers(["XZZXI","IXZZX","XIXZZ","ZXIXZ"])
# Construct the syndrome table for error decoding
qec_code.construct_syndrome_table()
qec_code.show_syndrome_table()
# Construct the syndrome measurement circuit and error correction circuit automatically
qec_code.construct_circuit()
```



## Repetition code

We implement the general repetition quantum error correction code and verify it under different types of quantum noise.


```python
from QEC.repetition import bitfliprepetitioncode
from Algorithm.noise import construct_bitflip_noise_model

#Initialize a repetiton 
rep=bitfliprepetitioncode(3)
#We can add a noise model to the QECcode class 
noisemode=construct_bitflip_noise_model(0.01,0.01,0.01)
rep.construct_syndrome_table()
rep.show_syndrome_table()    
rep.add_noise_model(noisemode)

#Simulate and show the result with and without quantum noise
rep.show_noise_effect(shots=100, save=True,savepath="RepetitionNoise.png")
```

Tthe output of show_syndrome_table() for the above three qubit repetition code is shown as follows:

<img src="Figures/syndromeoutput.png" alt="alt text" width="200"> 


# Quantum remote dynamic CNOT



# Reference





