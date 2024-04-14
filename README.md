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

Please contack us if you are interested.


[UCLA MQST program webpage](https://qst.ucla.edu/)

**Zhuoyang Ye, Qiyu Liu, Changsoo Kim, Manvi, Haocheng wang**



# Initialize a virtual environment

You can replicate all our results in this Hackthon on your own computer. Please create a virtual python environment, which we call yalehack, and intall the required package 
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

Quantum error correction 



## Noise model


## QECCode class

(Statbilizer, noise simulation, benchmark, error thershold simulation, syndrome table(Decoding) )


## Repetition code

We implement the general repetition quantum error correction code and verify it under different types of quantum noise.



# Quantum remote dynamic CNOT



# Reference





